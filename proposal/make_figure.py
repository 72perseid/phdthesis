#!/usr/bin/env python3
"""
make_figure.py - Draw the BX oven of Yumuktepe as a static figure.

  ../.venv/bin/python make_figure.py

Reads ../v2/out/yumuktepe-2024.ttl and writes bx_oven.dot and bx_oven.png.
Nothing is drawn that is not a statement in the graph: the nodes are chosen
here, every edge between them is read from the file.
"""

from __future__ import annotations

import logging
import subprocess
import textwrap
from pathlib import Path

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS

logging.getLogger("rdflib.term").setLevel(logging.ERROR)

HERE = Path(__file__).parent
TTL = HERE.parent / "v2" / "out" / "yumuktepe-2024.ttl"
BASE = "urn:fieldwork:entity:yumuktepe-2024%2F"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"

# entities of the oven, its hearth level, the two pottery groups and the dated sample
SEEDS = [
    "bx-oven", "bx-oven:use", "bx-hearth-level",
    "brittle-ware-bx", "brittle-ware-bx:making",
    "port-st-simeon-bx", "port-st-simeon-bx:making",
    "c13", "c14-bx", "s-barley-bx",
]

# class -> fill colour, as in v1/cidoc/visualize_graph.py
COLOURS = {
    "E25_Human-Made_Feature": "#aed6f1", "E22_Human-Made_Object": "#aed6f1",
    "A2_Stratigraphic_Volume_Unit": "#d7bfa6", "A7_Embedding": "#ead9c6",
    "E12_Production": "#fad7a0", "E7_Activity": "#fad7a0", "S2_Sample_Taking": "#fad7a0",
    "S4_Single_Observation": "#f5b7b1", "S13_Sample": "#f5cba7",
    "E4_Period": "#d7bde2", "E52_Time-Span": "#d7bde2",
}


def local(uri) -> str:
    return str(uri).rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def main() -> None:
    g = Graph()
    g.parse(TTL)

    nodes = {URIRef(BASE + s) for s in SEEDS}
    missing = [n for n in nodes if (n, None, None) not in g]
    if missing:
        raise SystemExit(f"not in the graph: {missing}")

    # nodes that tie two chosen entities together: embeddings, sample taking
    for cls in ("A7_Embedding", "S2_Sample_Taking"):
        for s in g.subjects(RDF.type, None):
            if local(g.value(s, RDF.type)) != cls:
                continue
            if sum(1 for o in g.objects(s) if o in nodes) >= 2:
                nodes.add(s)
    # time-spans of the chosen events
    for n in list(nodes):
        for o in g.objects(n, URIRef(CRM + "P4_has_time-span")):
            nodes.add(o)

    ids = {n: f"n{i}" for i, n in enumerate(sorted(nodes))}
    lines = [
        "digraph bx {", "  rankdir=LR; dpi=200; nodesep=0.25; ranksep=0.7;",
        '  node [shape=box, style="filled,rounded", fontname="DejaVu Sans", fontsize=10, margin="0.12,0.06"];',
        '  edge [fontname="DejaVu Sans", fontsize=8, color="#555555"];',
    ]
    for n, i in ids.items():
        classes = sorted(local(c) for c in g.objects(n, RDF.type))
        label = g.value(n, RDFS.label)
        if label is None:   # time-spans and generated events carry no label
            lits = [f"{local(p)}: {o}" for p, o in g.predicate_objects(n) if isinstance(o, Literal)]
            name = str(n).split("%2F")[-1] if "%2F" in str(n) else str(n).rsplit(":", 1)[-1]
            label = "\n".join(sorted(lits)) or name
        text = "\n".join(textwrap.wrap(str(label), 30)) if "\n" not in str(label) else str(label)
        text = text.replace('"', "'") + "\n" + " / ".join(classes)
        colour = next((COLOURS[c] for c in classes if c in COLOURS), "#eeeeee")
        lines.append(f'  {i} [label="{text}", fillcolor="{colour}"];')

    edges = 0
    for s, p, o in sorted(g):
        if s in nodes and o in nodes and p != RDF.type:
            lines.append(f'  {ids[s]} -> {ids[o]} [label="{local(p)}"];')
            edges += 1
    lines.append("}")

    dot = HERE / "bx_oven.dot"
    dot.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["dot", "-Tpng", str(dot), "-o", str(HERE / "bx_oven.png")], check=True)
    print(f"{len(nodes)} nodes, {edges} edges -> bx_oven.png")


if __name__ == "__main__":
    main()
