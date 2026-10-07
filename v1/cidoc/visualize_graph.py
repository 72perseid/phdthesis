#!/usr/bin/env python3
"""
visualize_graph.py - Render a CIDOC CRM Turtle graph as an interactive
pyvis network (HTML you open in a browser).

  python visualize_graph.py out/seleukeia_sidera_2024.ttl -o out/seleukeia_sidera_2024.html
  python visualize_graph.py out/... --helpers          # also show types, time-spans, dimensions, identifiers
  python visualize_graph.py out/... --focus find/coins-1993-fill --hops 2   # neighbourhood of one node

Nodes are coloured by CRM family, labelled with rdfs:label, and hovering shows
the class, note and source page.  Edges are labelled with the CRM property.
Inverse properties (P9i, P70i, ...) are dropped so each link is drawn once.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from collections import deque
from pathlib import Path

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from pyvis.network import Network

logging.getLogger("rdflib.term").setLevel(logging.ERROR)   # BC dateTimes are valid XSD but not Python datetimes

CRM = "http://www.cidoc-crm.org/cidoc-crm/"
ARCH = "http://www.cidoc-crm.org/extensions/crmarchaeo/"
SCI = "http://www.cidoc-crm.org/extensions/crmsci/"

# class -> (family, colour, shape)
FAMILIES = {
    "E7_Activity": ("activity", "#f39c12", "box"),
    "A9_Archaeological_Excavation": ("activity", "#e67e22", "box"),
    "A1_Excavation_Processing_Unit": ("activity", "#f5b041", "box"),
    "S19_Encounter_Event": ("event", "#f9e79f", "ellipse"),
    "E12_Production": ("event", "#fad7a0", "ellipse"),
    "E65_Creation": ("event", "#fad7a0", "ellipse"),
    "E13_Attribute_Assignment": ("interpretation", "#e74c3c", "diamond"),
    "E22_Human-Made_Object": ("thing", "#3498db", "dot"),
    "E25_Human-Made_Feature": ("thing", "#5dade2", "dot"),
    "E27_Site": ("thing", "#1f618d", "star"),
    "E20_Biological_Object": ("thing", "#85c1e9", "dot"),
    "A2_Stratigraphic_Volume_Unit": ("stratum", "#8e6e53", "triangle"),
    "A7_Embedding": ("stratum", "#c8a27a", "triangleDown"),
    "E21_Person": ("actor", "#27ae60", "dot"),
    "E74_Group": ("actor", "#1e8449", "square"),
    "E53_Place": ("place", "#16a085", "hexagon"),
    "E4_Period": ("period", "#8e44ad", "dot"),
    "E31_Document": ("document", "#7f8c8d", "box"),
    "E36_Visual_Item": ("document", "#bdc3c7", "square"),
    "E34_Inscription": ("document", "#bdc3c7", "square"),
    "E3_Condition_State": ("helper", "#d5dbdb", "dot"),
    "S13_Sample": ("sample", "#d35400", "dot"),
    "S2_Sample_Taking": ("event", "#f9e79f", "ellipse"),
    "S4_Single_Observation": ("analysis", "#c0392b", "box"),
    "E5_Event": ("event", "#fad7a0", "ellipse"),
    "E29_Design_or_Procedure": ("plan", "#95a5a6", "box"),
    # helpers (hidden unless --helpers)
    "E55_Type": ("helper", "#ecf0f1", "dot"),
    "E52_Time-Span": ("helper", "#d7bde2", "dot"),
    "E54_Dimension": ("helper", "#d5dbdb", "dot"),
    "E42_Identifier": ("helper", "#d5dbdb", "dot"),
    "PC14_carried_out_by": ("helper", "#abebc6", "dot"),
}
HELPER_CLASSES = {"E55_Type", "E52_Time-Span", "E54_Dimension", "E42_Identifier", "PC14_carried_out_by", "E3_Condition_State"}
# properties whose object is a helper we fold into the subject's tooltip when helpers are hidden
FOLDED = {"P2_has_type": "type", "P4_has_time_span": "time-span", "P43_has_dimension": "dimension",
          "P1_is_identified_by": "identifier", "P45_consists_of": "material", "P72_has_language": "language",
          "P91_has_unit": "unit", "P141_assigned": "assigned", "P177_assigned_property_of_type": "property"}


def local(u) -> str:
    return re.sub(r".*[/#]", "", str(u))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("graph", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--helpers", action="store_true", help="show E55 types, E52 time-spans, E54 dimensions, identifiers and PC14 nodes")
    ap.add_argument("--focus", help="draw only the neighbourhood of this node (path after the base URI, e.g. find/coins-1993-fill)")
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--inline-css", action="store_true",
                    help="download the CSS pyvis links from CDNs and embed it, so the page also works where external stylesheets are blocked")
    args = ap.parse_args(argv)

    g = Graph().parse(args.graph)
    out = args.out or args.graph.with_suffix(".html")

    # --- classify every subject ------------------------------------------------
    info: dict[URIRef, dict] = {}
    for s in set(g.subjects()):
        if not isinstance(s, URIRef):
            continue
        classes = [local(c) for c in g.objects(s, RDF.type)]
        # pick the most specific / most informative class for colouring
        cls = next((c for c in classes if c in FAMILIES and c not in ("E7_Activity",)), None) or \
              next((c for c in classes if c in FAMILIES), None) or (classes[0] if classes else "?")
        fam, colour, shape = FAMILIES.get(cls, ("other", "#95a5a6", "dot"))
        label = str(g.value(s, RDFS.label) or local(s))
        info[s] = {"cls": cls, "classes": classes, "fam": fam, "colour": colour, "shape": shape, "label": label}

    INTERPRETATION = "type/interpretation"

    def is_helper(n) -> bool:
        if n not in info:
            return False
        if info[n]["cls"] in HELPER_CLASSES:
            return True
        # E13 nodes that only document a dating, identification or stratigraphic relation
        # are bookkeeping: the relation itself is already drawn as a direct edge
        if info[n]["cls"] == "E13_Attribute_Assignment":
            kinds = [str(o) for o in g.objects(n, URIRef(CRM + "P2_has_type"))]
            return not any(k.endswith(INTERPRETATION) for k in kinds)
        return False

    # --- optional focus --------------------------------------------------------
    keep = None
    if args.focus:
        base = next((str(s) for s in info if str(s).endswith("/" + args.focus)), None)
        if not base:
            sys.exit(f"focus node not found: {args.focus}")
        start = URIRef(base)
        keep = {start}
        frontier = deque([(start, 0)])
        while frontier:
            n, d = frontier.popleft()
            if d >= args.hops:
                continue
            # walk both directions, but never through the report node (P70 links it to everything)
            nbrs = [(pp, oo) for pp, oo in g.predicate_objects(n)] + [(pp, ss) for ss, pp in g.subject_predicates(n)]
            for pp, nb in nbrs:
                if local(pp).startswith("P70") or local(pp) == "type":
                    continue
                if isinstance(nb, URIRef) and nb in info and nb not in keep and not (is_helper(nb) and not args.helpers):
                    keep.add(nb)
                    frontier.append((nb, d + 1))

    # --- build network ---------------------------------------------------------
    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff", font_color="#222222",
                  select_menu=True, filter_menu=True, cdn_resources="remote")
    net.set_options("""
    {
      "physics": {"solver": "forceAtlas2Based",
                  "forceAtlas2Based": {"gravitationalConstant": -60, "springLength": 120, "springConstant": 0.04},
                  "stabilization": {"iterations": 200}},
      "edges": {"arrows": {"to": {"enabled": true, "scaleFactor": 0.6}}, "smooth": {"type": "dynamic"},
                "font": {"size": 9, "color": "#666666", "align": "middle"}, "color": {"color": "#b0b0b0"}},
      "nodes": {"font": {"size": 12}},
      "interaction": {"hover": true, "tooltipDelay": 100, "navigationButtons": true}
    }""")

    def tooltip(n: URIRef) -> str:
        i = info[n]
        lines = [f"<b>{i['label']}</b>", "class: " + ", ".join(i["classes"]), f"uri: {local(n)}"]
        for p, o in g.predicate_objects(n):
            pl = local(p)
            if isinstance(o, Literal) and pl not in ("label",):
                lines.append(f"{pl.replace('_', ' ')}: {o}")
            elif pl in FOLDED and o in info:
                lines.append(f"{FOLDED[pl]}: {info[o]['label']}")
        return "\n".join(lines)

    added = set()

    def add_node(n: URIRef):
        if n in added:
            return
        i = info[n]
        size = {"activity": 22, "thing": 16, "actor": 16, "place": 16, "period": 16, "document": 18,
                "interpretation": 18, "stratum": 16, "event": 10, "helper": 8,
                "sample": 12, "analysis": 18, "plan": 14}.get(i["fam"], 12)
        net.add_node(str(n), label=i["label"][:40] + ("…" if len(i["label"]) > 40 else ""),
                     title=tooltip(n), color=i["colour"], shape=i["shape"], size=size, group=i["fam"])
        added.add(n)

    edges = 0
    for s, p, o in g:
        if not (isinstance(s, URIRef) and isinstance(o, URIRef)) or s not in info or o not in info:
            continue
        pl = local(p)
        if pl in ("type",) or re.match(r"^(P|AP|O)\d+i_", pl):   # skip rdf:type and inverse properties
            continue
        if not args.helpers and (is_helper(s) or is_helper(o)):
            continue
        if keep is not None and (s not in keep or o not in keep):
            continue
        add_node(s); add_node(o)
        net.add_edge(str(s), str(o), label=pl.replace("_", " "), title=pl)
        edges += 1

    out.parent.mkdir(parents=True, exist_ok=True)
    net.write_html(str(out), open_browser=False, notebook=False)
    html = out.read_text(encoding="utf-8")
    # pyvis leaves two dead references to a local node_modules copy of vis; drop them
    html = re.sub(r'\s*<script[^>]*node_modules/vis[^>]*></script>', "", html)
    html = re.sub(r'\s*<link[^>]*node_modules/vis[^>]*>', "", html)
    if args.inline_css:
        import urllib.request
        def inline(m):
            href = m.group(1)
            try:
                css = urllib.request.urlopen(href, timeout=20).read().decode("utf-8")
            except Exception as e:  # keep the link if the download fails
                print(f"could not inline {href}: {e}", file=sys.stderr)
                return m.group(0)
            return f"<style>/* inlined from {href} */\n{css}\n</style>"
        html = re.sub(r'<link[^>]*href="(https://[^"]+\.css)"[^>]*>', inline, html)
    out.write_text(html, encoding="utf-8")

    legend = ", ".join(f"{fam}" for fam in sorted({i['fam'] for i in info.values()}))
    print(f"{out}: {len(added)} nodes, {edges} edges (families: {legend})")
    print("open it in a browser; hover a node for its properties, use the filter menu to show one family")
    return 0


if __name__ == "__main__":
    sys.exit(main())
