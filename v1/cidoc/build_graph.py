#!/usr/bin/env python3
"""
build_graph.py - Turn a structured excavation-report record (JSON) into a
CIDOC CRM knowledge graph (Turtle).

Record format: schema.md (version 3).  Version 1 and 2 records still build.
Examples: data/seleukeia_sidera_2024.json (v1), data/yumuktepe_2024.json (v2).

Ontologies used
  crm        CIDOC CRM 7.1.x      http://www.cidoc-crm.org/cidoc-crm/
  crmarchaeo CRMarchaeo 2.1.1     http://www.cidoc-crm.org/extensions/crmarchaeo/
             A1, A2, A4, A7, A8, A9, AP1, AP3, AP5, AP7, AP11, AP18, AP19
  crmsci     CRMsci 3.2           http://www.cidoc-crm.org/extensions/crmsci/
             S2, S4, S11, S13, S19, O3, O5, O8, O9, O16, O19
  kst        project vocabulary   <shared_uri>vocab/
             annotation properties only: sourcePage, printedPages, beginYear,
             endYear, plannedFor, and one relation CRM lacks: contemporaryWith

Namespaces
  <base_uri>    per paper: entities of that report
  <shared_uri>  shared by all papers: vocab/ and type/ (E55 Types), so that
                "coin" or "ORCID" is the same node in every graph

Usage
  python build_graph.py data/yumuktepe_2024.json -o out/yumuktepe_2024.ttl
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import unicodedata
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, SKOS

logging.getLogger("rdflib.term").setLevel(logging.ERROR)   # BC dateTimes: valid XSD, not Python datetimes

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
ARCH = Namespace("http://www.cidoc-crm.org/extensions/crmarchaeo/")
SCI = Namespace("http://www.cidoc-crm.org/extensions/crmsci/")

# relation types that are physical relations between stratigraphic units (AP11)
PHYSICAL_RELATIONS = {"cuts", "destroys", "overlies", "fills", "abuts", "is cut by", "underlies"}


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def slug(text: str) -> str:
    text = text.translate(str.maketrans({"ı": "i", "İ": "I", "ş": "s", "Ş": "S", "ğ": "g", "Ğ": "G",
                                         "ç": "c", "Ç": "C", "ö": "o", "Ö": "O", "ü": "u", "Ü": "U"}))
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()


def iso_datetime(year, start: bool) -> str:
    """Historical year (negative = BC, no year 0) -> ISO 8601 / XSD dateTime.

    ISO uses astronomical numbering: 1 BC = year 0000, 2580 BC = -2579.
    Years are zero-padded to four digits, so 900 becomes 0900.
    """
    y = int(year)
    if y == 0:
        raise ValueError("there is no year 0 in historical numbering")
    astro = y if y > 0 else y + 1
    text = f"{'-' if astro < 0 else ''}{abs(astro):04d}"
    return f"{text}-01-01T00:00:00" if start else f"{text}-12-31T23:59:59"


def year_label(year) -> str:
    y = int(year)
    return f"MÖ {abs(y)}" if y < 0 else f"MS {y}"


class Builder:
    def __init__(self, record: dict):
        self.rec = record
        self.base = record["base_uri"]
        self.shared = record.get("shared_uri") or re.sub(r"[^/]+/$", "", self.base)
        self.g = Graph()
        for prefix, ns in (("crm", CRM), ("crmarchaeo", ARCH), ("crmsci", SCI), ("dcterms", DCTERMS), ("skos", SKOS)):
            self.g.bind(prefix, ns)
        self.KST = Namespace(self.shared + "vocab/")
        self.g.bind("kst", self.KST)
        self.g.bind("type", Namespace(self.shared + "type/"))
        self.types: dict[str, URIRef] = {}
        self.report = self.uri("document", record["document"]["id"])
        self.authors = list(record["document"].get("authors", []))
        # index: entity id -> uri kind, for cross references of any sort
        self.kinds: dict[str, str] = {}
        for kind, key in (("feature", "features"), ("find", "finds"), ("stratum", "strata"),
                          ("activity", "activities"), ("sample", "samples"), ("place", "places"),
                          ("plan", "plans"), ("actor", "actors"), ("record", "records")):
            for item in record.get(key, []):
                self.kinds.setdefault(item["id"], kind)

    # --- uris ---------------------------------------------------------------
    def uri(self, kind: str, ident: str) -> URIRef:
        return URIRef(f"{self.base}{kind}/{ident}")

    def resolve(self, ident: str) -> URIRef:
        if ident not in self.kinds:
            raise KeyError(f"unknown entity id '{ident}'")
        return self.uri(self.kinds[ident], ident)

    def figure_id(self, ref) -> str:
        """v1 records reference figures by number; v2 by id ('resim-3', 'sekil-1')."""
        return f"resim-{ref}" if isinstance(ref, int) or str(ref).isdigit() else str(ref)

    def place_of(self, ident: str) -> URIRef:
        """The E53 Place a physical thing occupies (created on demand)."""
        if self.kinds.get(ident) == "place":
            return self.uri("place", ident)
        p = self.uri("place", f"of-{ident}")
        if (p, RDF.type, CRM.E53_Place) not in self.g:
            thing = self.resolve(ident)
            label = self.g.value(thing, RDFS.label) or ident
            self.add(p, CRM.E53_Place, f"{label} (konum)")
            self.g.add((thing, CRM.P53_has_former_or_current_location, p))
            self.g.add((p, CRM.P53i_is_former_or_current_location_of, thing))
        return p

    # --- generic statements ---------------------------------------------------
    def add(self, s: URIRef, cls: URIRef, label: str, lang: str = "tr") -> URIRef:
        self.g.add((s, RDF.type, cls))
        self.g.add((s, RDFS.label, Literal(label, lang=lang)))
        return s

    def note(self, s: URIRef, text):
        if text:
            self.g.add((s, CRM.P3_has_note, Literal(text, lang="tr")))

    def provenance(self, s: URIRef, pages=None, figures=None):
        """Every entity is documented by the report (P70) and, if known, by pages."""
        self.g.add((self.report, CRM.P70_documents, s))
        self.g.add((s, CRM.P70i_is_documented_in, self.report))
        for p in pages or []:
            self.g.add((s, self.KST.sourcePage, Literal(int(p), datatype=XSD.integer)))
        for n in figures or []:
            self.g.add((s, CRM.P138i_has_representation, self.uri("figure", self.figure_id(n))))

    def typ(self, label: str, broader: str | None = None, lang: str = "en") -> URIRef:
        """E55 Type in the shared namespace (one node per distinct label, across papers)."""
        key = slug(label)
        if key not in self.types:
            t = URIRef(f"{self.shared}type/{key}")
            self.add(t, CRM.E55_Type, label, lang=lang)
            if broader:
                self.g.add((t, CRM.P127_has_broader_term, self.typ(broader)))
            self.types[key] = t
        return self.types[key]

    def timespan(self, subject: URIRef | None, ts: dict, ident: str, prop=None) -> URIRef:
        t = self.uri("timespan", ident)
        begin, end = ts.get("begin"), ts.get("end")
        label = ts.get("label") or f"{year_label(begin) if begin else '?'} – {year_label(end) if end else '?'}"
        self.add(t, CRM["E52_Time-Span"], label)
        if subject is not None:
            self.g.add((subject, prop or CRM.P4_has_time_span, t))
        if begin:
            self.g.add((t, CRM.P82a_begin_of_the_begin, Literal(iso_datetime(begin, True), datatype=XSD.dateTime)))
            self.g.add((t, self.KST.beginYear, Literal(int(begin), datatype=XSD.integer)))
        if end:
            self.g.add((t, CRM.P82b_end_of_the_end, Literal(iso_datetime(end, False), datatype=XSD.dateTime)))
            self.g.add((t, self.KST.endYear, Literal(int(end), datatype=XSD.integer)))
        if ts.get("approx"):
            self.g.add((t, CRM.P2_has_type, self.typ("approximate")))
        return t

    def dimension(self, subject: URIRef, dim: dict, ident: str):
        d = self.uri("dimension", ident)
        if "value" in dim:
            text = f"{dim['value']}"
        else:
            text = f"{dim.get('min', '?')}–{dim.get('max', '?')}"
        self.add(d, CRM.E54_Dimension, f"{dim['type']} {text} {dim['unit']}", lang="en")
        self.g.add((subject, CRM.P43_has_dimension, d))
        self.g.add((d, CRM.P2_has_type, self.typ(dim["type"])))
        if "value" in dim:
            self.g.add((d, CRM.P90_has_value, Literal(dim["value"], datatype=XSD.decimal)))
        if "min" in dim:
            self.g.add((d, CRM.P90a_has_lower_value_limit, Literal(dim["min"], datatype=XSD.decimal)))
        if "max" in dim:
            self.g.add((d, CRM.P90b_has_upper_value_limit, Literal(dim["max"], datatype=XSD.decimal)))
        if dim.get("approx"):
            self.g.add((d, CRM.P2_has_type, self.typ("approximate")))
        self.g.add((d, CRM.P91_has_unit, self.typ(dim["unit"])))

    def identifier(self, subject: URIRef, value: str, kind: str, scope: str = ""):
        i = self.uri("identifier", slug(f"{kind}-{scope}-{value}" if scope else f"{kind}-{value}"))
        self.add(i, CRM.E42_Identifier, value, lang="en")
        self.g.add((i, CRM.P2_has_type, self.typ(kind)))
        self.g.add((subject, CRM.P1_is_identified_by, i))

    def carried_out_by(self, activity: URIRef, act_id: str, entries: list[dict]):
        """P14 plus the PC14 property-class pattern so the role (P14.1) survives in RDF."""
        for i, e in enumerate(entries):
            actor = self.uri("actor", e["actor"])
            self.g.add((activity, CRM.P14_carried_out_by, actor))
            self.g.add((actor, CRM.P14i_performed, activity))
            if e.get("role"):
                pc = self.uri("pc14", f"{act_id}-{i}")
                self.g.add((pc, RDF.type, CRM.PC14_carried_out_by))
                self.g.add((pc, CRM.P01_has_domain, activity))
                self.g.add((pc, CRM.P02_has_range, actor))
                self.g.add((pc, CRM["P14.1_in_the_role_of"], self.typ(e["role"])))

    def assignment(self, ident: str, label: str, kind: str, target: URIRef, value, prop: URIRef,
                   by: list[str] | None = None, via: str | None = None, note: str | None = None,
                   pages=None) -> URIRef:
        """E13 Attribute Assignment: who said that <target> <prop> <value>, and how they know."""
        s = self.uri("assignment", ident)
        self.add(s, CRM.E13_Attribute_Assignment, label)
        self.g.add((s, CRM.P2_has_type, self.typ(kind)))
        if via:
            self.g.add((s, CRM.P2_has_type, self.typ(via, broader="source of knowledge")))
        self.g.add((s, CRM.P140_assigned_attribute_to, target))
        self.g.add((s, CRM.P141_assigned, value))
        self.g.add((s, CRM.P177_assigned_property_of_type, prop))
        for a in (by or self.authors):
            self.g.add((s, CRM.P14_carried_out_by, self.uri("actor", a)))
        self.note(s, note)
        self.provenance(s, pages)
        return s

    # --- sections ---------------------------------------------------------------
    def build(self) -> Graph:
        self.document()
        self.actors()
        self.places()
        self.periods()
        self.references()
        self.features()
        self.strata()
        self.activities()
        self.finds()
        self.samples()
        self.analyses()
        self.relations()
        self.plans()
        self.records()
        self.interpretations()
        self.figures()
        return self.g

    def document(self):
        d = self.rec["document"]
        r = self.report
        self.add(r, CRM.E31_Document, d["title"])
        self.g.add((r, RDF.type, CRM.E33_Linguistic_Object))
        self.g.add((r, CRM.P72_has_language, self.typ(d.get("language", "tr"))))
        self.g.add((r, CRM.P2_has_type, self.typ("excavation report")))
        self.g.add((r, DCTERMS.source, Literal(d["source_file"])))
        self.g.add((r, self.KST.printedPages, Literal(d["pages"])))
        if d.get("documents"):
            # the campaign the report is about; queries start from here
            self.g.add((r, CRM.P129_is_about, self.uri("activity", d["documents"])))
        c = self.uri("event", f"creation-{d['id']}")
        self.add(c, CRM.E65_Creation, f"{d['title']} – yazım")
        self.g.add((c, CRM.P94_has_created, r))
        self.g.add((r, CRM.P94i_was_created_by, c))
        for a in d["authors"]:
            self.g.add((c, CRM.P14_carried_out_by, self.uri("actor", a)))
        if d.get("published"):
            self.timespan(c, {"begin": d["published"], "end": d["published"]}, f"creation-{d['id']}")
        v = d.get("volume")
        if v:
            vol = URIRef(f"{self.shared}document/{v['id']}")      # the volume is shared by all papers
            self.add(vol, CRM.E31_Document, v["title"])
            self.g.add((vol, CRM.P106_is_composed_of, r))
            self.g.add((r, CRM.P106i_forms_part_of, vol))
            if v.get("isbn"):
                self.identifier(vol, v["isbn"], "ISBN")
            if v.get("editor"):
                self.g.add((vol, DCTERMS.contributor, self.uri("actor", v["editor"])))
            if v.get("publisher"):
                self.g.add((vol, DCTERMS.publisher, self.uri("actor", v["publisher"])))

    def actors(self):
        for a in self.rec["actors"]:
            s = self.uri("actor", a["id"])
            self.add(s, CRM[a["class"]], a["label"])
            if a.get("orcid"):
                self.identifier(s, a["orcid"], "ORCID")
            if a.get("member_of"):
                grp = self.uri("actor", a["member_of"])
                self.g.add((s, CRM.P107i_is_current_or_former_member_of, grp))
                self.g.add((grp, CRM.P107_has_current_or_former_member, s))
            self.note(s, a.get("note"))
            self.provenance(s, a.get("pages"))

    def places(self):
        for p in self.rec["places"]:
            s = self.uri("place", p["id"])
            self.add(s, CRM.E53_Place, p["label"])
            if p.get("type"):
                self.g.add((s, CRM.P2_has_type, self.typ(p["type"])))
            if p.get("within"):
                self.g.add((s, CRM.P89_falls_within, self.uri("place", p["within"])))
            self.note(s, p.get("note"))
            self.provenance(s, p.get("pages"))

    def periods(self):
        for p in self.rec["periods"]:
            s = self.uri("period", p["id"])
            self.add(s, CRM.E4_Period, p["label"])
            if p.get("begin") or p.get("end"):
                self.timespan(s, p | {"label": None}, p["id"])
            if p.get("within"):
                whole = self.uri("period", p["within"])
                self.g.add((s, CRM.P9i_forms_part_of, whole))
                self.g.add((whole, CRM.P9_consists_of, s))
            self.provenance(s, p.get("pages"))

    def _period_links(self, subject: URIRef, item: dict):
        """A dated thing: E12 Production falling within the E4 Period(s).

        With 'dating_by', each period link is also stated as an E13 Attribute
        Assignment naming who dated it and how they know (e.g. personal
        communication), so attributed datings can be told from the authors' own.
        """
        periods = item.get("periods") or ([item["period"]] if item.get("period") else [])
        if not periods:
            return
        prod = self.uri("event", f"production-{item['id']}")
        self.add(prod, CRM.E12_Production, f"{item['label']} – üretim")
        self.g.add((prod, CRM.P108_has_produced, subject))
        self.g.add((subject, CRM.P108i_was_produced_by, prod))
        certainty = item.get("dating_certainty")
        for per in periods:
            period = self.uri("period", per)
            db = item.get("dating_by")
            if certainty:
                # v3: a hedged dating is never a plain statement.  It exists only as
                # the claim (E13), typed with how sure the authors are:
                # 'uncertain' = perhaps this period, 'one of' = one of the periods listed.
                a = self.assignment(f"dating-{item['id']}-{per}", f"{item['label']} – tarihleme: {self.g.value(period, RDFS.label)}",
                                    "dating", prod, period, CRM.P10_falls_within,
                                    by=(db or {}).get("by"), via=(db or {}).get("via"), pages=item.get("pages"))
                self.g.add((a, CRM.P2_has_type, self.typ(certainty, broader="certainty")))
                continue
            self.g.add((prod, CRM.P10_falls_within, period))
            if db:
                self.assignment(f"dating-{item['id']}-{per}", f"{item['label']} – tarihleme: {self.g.value(period, RDFS.label)}",
                                "dating", prod, period, CRM.P10_falls_within,
                                by=db.get("by"), via=db.get("via"), pages=item.get("pages"))

    def _physical(self, kind: str, item: dict, default_class: str | None = None) -> URIRef:
        s = self.uri(kind, item["id"])
        cname = item.get("class") or default_class
        cls = SCI[cname] if cname.startswith("S") else ARCH[cname] if cname.startswith("A") else CRM[cname]
        self.add(s, cls, item["label"])
        if item.get("type"):
            self.g.add((s, CRM.P2_has_type, self.typ(item["type"])))
        if item.get("material_type"):
            self.g.add((s, CRM.P2_has_type, self.typ(item["material_type"])))
        for taxon in item.get("taxa", []):
            self.g.add((s, CRM.P2_has_type, self.typ(taxon, broader="taxon", lang="la")))
        if item.get("material"):
            self.g.add((s, CRM.P45_consists_of, self.typ(item["material"])))
        if item.get("identifier"):
            self.identifier(s, item["identifier"], "context code", scope=slug(self.base.rstrip("/").rsplit("/", 1)[-1]))
        self.note(s, item.get("note"))
        for i, dim in enumerate(item.get("dimensions", [])):
            self.dimension(s, dim, f"{item['id']}-{i}")
        if item.get("count"):
            self.dimension(s, {"type": "count", "value": item["count"], "unit": "piece"}, f"{item['id']}-count")
        for c in item.get("comparanda", []):
            self.g.add((s, CRM.P130_shows_features_of, self.typ(c["label"], broader="comparandum", lang="tr")))
            self.note(s, f"Benzer: {c['label']}" + (f" ({c['refs']})" if c.get("refs") else ""))
        self._period_links(s, item)
        self.provenance(s, item.get("pages"), item.get("figures"))
        self.cite(s, item)
        if kind != "feature" and item.get("part_of"):
            # v3: a unit inside a layer, a single find inside a counted assemblage
            whole = self.uri(kind, item["part_of"])
            self.g.add((s, CRM.P46i_forms_part_of, whole))
            self.g.add((whole, CRM.P46_is_composed_of, s))
        return s

    def cite(self, s: URIRef, item: dict):
        """v3: literature the paper cites for this entity; with pages, the cited passage."""
        for i, c in enumerate(item.get("sources", [])):
            doc = self.uri("reference", c["ref"])
            if c.get("pages"):
                passage = self.uri("reference", f"{c['ref']}-{slug(str(c['pages']))}")
                self.add(passage, CRM.E31_Document, f"{c['ref']}, s. {c['pages']}")
                self.g.add((passage, CRM.P2_has_type, self.typ("cited passage")))
                self.g.add((passage, CRM.P106i_forms_part_of, doc))
                self.g.add((doc, CRM.P106_is_composed_of, passage))
                doc = passage
            self.g.add((doc, CRM.P70_documents, s))
            self.g.add((s, CRM.P70i_is_documented_in, doc))

    def references(self):
        for r in self.rec.get("references", []):
            s = self.uri("reference", r["id"])
            self.add(s, CRM.E31_Document, r["citation"])
            self.g.add((s, CRM.P2_has_type, self.typ("cited publication")))
            if r.get("year"):
                c = self.uri("event", f"creation-{r['id']}")
                self.add(c, CRM.E65_Creation, f"{r['id']} – yayın")
                self.g.add((c, CRM.P94_has_created, s))
                self.timespan(c, {"begin": r["year"], "end": r["year"]}, f"creation-{r['id']}")
            self.note(s, r.get("note"))
            self.provenance(s, r.get("pages"))

    def records(self):
        """v3: documentation made during the work (3D model, plan, drawing): what an archive holds."""
        for r in self.rec.get("records", []):
            s = self.uri("record", r["id"])
            self.add(s, CRM.E73_Information_Object, r["label"])
            self.g.add((s, CRM.P2_has_type, self.typ(r["type"], broader="documentation")))
            if r.get("scale"):
                self.g.add((s, CRM.P2_has_type, self.typ(f"scale {r['scale']}", broader="scale")))
            for target in r.get("depicts", []):
                self.g.add((s, CRM.P67_refers_to, self.resolve(target)))
            if r.get("made_by"):
                c = self.uri("event", f"creation-{r['id']}")
                act = self.uri("activity", r["made_by"])
                self.add(c, CRM.E65_Creation, f"{r['label']} – hazırlama")
                self.g.add((c, CRM.P94_has_created, s))
                self.g.add((s, CRM.P94i_was_created_by, c))
                self.g.add((c, CRM.P9i_forms_part_of, act))
                self.g.add((act, CRM.P9_consists_of, c))
            self.note(s, r.get("note"))
            self.provenance(s, r.get("pages"), r.get("figures"))

    def features(self):
        for f in self.rec["features"]:
            s = self._physical("feature", f)
            if f.get("part_of"):
                whole = self.uri("feature", f["part_of"])
                self.g.add((s, CRM.P46i_forms_part_of, whole))
                self.g.add((whole, CRM.P46_is_composed_of, s))
            if f.get("location"):
                loc = self.uri("place", f["location"])
                self.g.add((s, CRM.P53_has_former_or_current_location, loc))
                self.g.add((loc, CRM.P53i_is_former_or_current_location_of, s))

    def strata(self):
        for st in self.rec.get("strata", []):
            s = self._physical("stratum", st, default_class="A2_Stratigraphic_Volume_Unit")
            if st.get("at_feature"):
                self.g.add((s, CRM.P53_has_former_or_current_location, self.place_of(st["at_feature"])))

    def activities(self):
        for a in self.rec["activities"]:
            s = self.uri("activity", a["id"])
            cls = ARCH[a["class"]] if a["class"].startswith("A") else CRM[a["class"]]
            self.add(s, cls, a["label"])
            if a["class"].startswith("A"):
                self.g.add((s, RDF.type, CRM.E7_Activity))
            if a.get("type"):
                self.g.add((s, CRM.P2_has_type, self.typ(a["type"])))
            if a.get("timespan"):
                self.timespan(s, a["timespan"], a["id"])
            self.note(s, a.get("note"))
            if a.get("identifier"):
                self.identifier(s, a["identifier"], "project number")
            self.carried_out_by(s, a["id"], a.get("carried_out_by", []))
            for pl in a.get("took_place_at", []):
                self.g.add((s, CRM.P7_took_place_at, self.uri("place", pl)))
            for feat in [a.get("at_feature")] + a.get("also_at", []):
                if feat:
                    self.g.add((s, CRM.P7_took_place_at, self.place_of(feat)))
            if a.get("part_of"):
                whole = self.uri("activity", a["part_of"])
                self.g.add((s, CRM.P9i_forms_part_of, whole))
                self.g.add((whole, CRM.P9_consists_of, s))
            for prev in a.get("continued", []):
                self.g.add((s, CRM.P134_continued, self.uri("activity", prev)))
            for obj in a.get("used", []):
                self.g.add((s, CRM.P16_used_specific_object, self.resolve(obj)))
            if a.get("purpose_of"):
                self.g.add((s, CRM.P20_had_specific_purpose, self.uri("activity", a["purpose_of"])))
            if a.get("investigated"):
                # CRMarchaeo: A9 Archaeological Excavation AP3 investigated E27 Site
                self.g.add((s, ARCH.AP3_investigated, self.uri("feature", a["investigated"])))
            for st in a.get("produced", []):
                # v3: an activity that created a deposit (spoil heap, backfill):
                # CRMarchaeo A4 Stratigraphic Genesis AP7 produced A8 Stratigraphic Unit
                unit = self.uri("stratum", st)
                self.g.add((s, RDF.type, ARCH.A4_Stratigraphic_Genesis))
                self.g.add((s, ARCH.AP7_produced, unit))
                self.g.add((unit, RDF.type, ARCH.A8_Stratigraphic_Unit))
            if a.get("excavated"):
                # v3: how much was dug: A1 AP1 produced S11 Amount of Matter, which has the dimensions
                m = self.uri("matter", a["id"])
                self.add(m, SCI.S11_Amount_of_Matter, f"{a['label']} – kazılan toprak")
                self.g.add((s, ARCH.AP1_produced, m))
                for i, dim in enumerate(a["excavated"]):
                    self.dimension(m, dim, f"{a['id']}-excavated-{i}")
                self.provenance(m, a.get("pages"))
            self.cite(s, a)
            for st in a.get("removed", []):
                # CRMarchaeo: A1 Excavation Processing Unit AP5 removed part or all of A8 Stratigraphic Unit
                self.g.add((s, ARCH.AP5_removed_part_or_all_of, self.uri("stratum", st)))
            self.provenance(s, a.get("pages"), a.get("figures"))
        # second pass: a sub-activity without dates inherits the nearest dated ancestor's time-span
        by_id = {a["id"]: a for a in self.rec["activities"]}
        for a in self.rec["activities"]:
            if a.get("timespan"):
                continue
            parent = a.get("part_of")
            while parent and not by_id[parent].get("timespan"):
                parent = by_id[parent].get("part_of")
            if parent:
                self.g.add((self.uri("activity", a["id"]), CRM.P4_has_time_span, self.uri("timespan", parent)))

    def _activity_timespan(self, act_id: str):
        return self.g.value(self.uri("activity", act_id), CRM.P4_has_time_span)

    def finds(self):
        for f in self.rec["finds"]:
            s = self._physical("find", f)
            if f.get("condition"):
                cs = self.uri("condition", f["id"])
                self.add(cs, CRM.E3_Condition_State, f["condition"], lang="en")
                self.g.add((cs, CRM.P2_has_type, self.typ(f["condition"])))
                self.g.add((s, CRM.P44_has_condition, cs))
            if f.get("depicts"):
                self.g.add((s, CRM.P62_depicts, self.typ(f["depicts"])))
            if f.get("inscribed"):
                self.g.add((s, CRM.P128_carries, self.uri("inscription", f["id"])))
                self.add(self.uri("inscription", f["id"]), CRM.E34_Inscription, f"{f['label']} – yazıt")
            ib = f.get("identified_by")
            if ib:
                for taxon in f.get("taxa", []):
                    self.assignment(f"identification-{f['id']}-{slug(taxon)}", f"{f['label']} – tanımlama: {taxon}",
                                    "identification", s, self.typ(taxon, broader="taxon", lang="la"), CRM.P2_has_type,
                                    by=ib.get("by"), via=ib.get("via"), pages=f.get("pages"))
            # the discovery: an S19 Encounter Event inside the excavation activity
            enc = self.uri("event", f"encounter-{f['id']}")
            self.add(enc, SCI.S19_Encounter_Event, f"{f['label']} – buluntu olayı")
            self.g.add((enc, RDF.type, CRM.E7_Activity))
            self.g.add((enc, SCI.O19_encountered_object, s))
            self.g.add((s, SCI.O19i_was_object_encountered_at, enc))
            act = self.uri("activity", f["found_by"])
            self.g.add((enc, CRM.P9i_forms_part_of, act))
            self.g.add((act, CRM.P9_consists_of, enc))
            ts = self._activity_timespan(f["found_by"])
            if ts is not None:
                self.g.add((enc, CRM.P4_has_time_span, ts))
            if f.get("at_feature"):
                place = self.place_of(f["at_feature"])
                self.g.add((enc, CRM.P7_took_place_at, place))
                self.g.add((s, CRM.P53_has_former_or_current_location, place))
            if f.get("from_stratum"):
                # CRMarchaeo: find -AP18i-> A7 Embedding -AP19-> A2 Stratigraphic Volume Unit
                stratum = self.uri("stratum", f["from_stratum"])
                emb = self.uri("embedding", f["id"])
                self.add(emb, ARCH.A7_Embedding, f"{f['label']} – gömülü olma durumu")
                self.g.add((emb, ARCH.AP18_is_embedding_of, s))
                self.g.add((s, ARCH.AP18i_is_embedded, emb))
                self.g.add((emb, ARCH.AP19_is_embedding_in, stratum))
                self.g.add((stratum, ARCH.AP19i_contains_embedding, emb))
            self.provenance(enc, f.get("pages"))

    def samples(self):
        """CRMsci: S2 Sample Taking -O3-> source, -O5-> S13 Sample."""
        for sm in self.rec.get("samples", []):
            s = self._physical("sample", sm, default_class="S13_Sample")
            taking = self.uri("event", f"sampling-{sm['id']}")
            self.add(taking, SCI.S2_Sample_Taking, f"{sm['label']} – örnek alma")
            self.g.add((taking, RDF.type, CRM.E7_Activity))
            self.g.add((taking, SCI.O5_removed, s))
            self.g.add((s, SCI.O5i_was_removed_by, taking))
            if sm.get("taken_from"):
                self.g.add((taking, SCI.O3_sampled_from, self.resolve(sm["taken_from"])))
                self.g.add((taking, CRM.P7_took_place_at, self.place_of(sm["taken_from"])))
            if sm.get("taken_during"):
                act = self.uri("activity", sm["taken_during"])
                self.g.add((taking, CRM.P9i_forms_part_of, act))
                self.g.add((act, CRM.P9_consists_of, taking))
                ts = self._activity_timespan(sm["taken_during"])
                if ts is not None:
                    self.g.add((taking, CRM.P4_has_time_span, ts))
            self.provenance(taking, sm.get("pages"))

    def analyses(self):
        """A laboratory result and the dating inferred from it, kept apart.

        S4 Single Observation: observed the sample(s), property type = the
        analysis type, observed value = an E52 Time-Span (the calibrated range).
        E13 Attribute Assignment: the authors conclude that the use of the
        dated context has that time-span, motivated by the observation.
        """
        for an in self.rec.get("analyses", []):
            obs = self.uri("analysis", an["id"])
            self.add(obs, SCI.S4_Single_Observation, an["label"])
            self.g.add((obs, CRM.P2_has_type, self.typ(an["type"])))
            self.g.add((obs, SCI.O9_observed_property_type, self.typ(an["type"])))
            for sm in an.get("samples", []):
                self.g.add((obs, SCI.O8_observed, self.uri("sample", sm)))
            for a in an.get("by", []):
                self.g.add((obs, CRM.P14_carried_out_by, self.uri("actor", a)))
            res = an["result"]
            ts = self.timespan(None, res | {"label": f"{year_label(res['begin'])} – {year_label(res['end'])} cal."}, f"result-{an['id']}")
            self.g.add((ts, CRM.P2_has_type, self.typ("calibrated radiocarbon range")))
            self.g.add((obs, SCI.O16_observed_value, ts))
            self.note(obs, an.get("note"))
            self.provenance(obs, an.get("pages"))
            if an.get("dates"):
                target = self.resolve(an["dates"])
                use = self.uri("event", f"use-{an['dates']}")
                self.add(use, CRM.E5_Event, f"{self.g.value(target, RDFS.label)} – kullanım evresi")
                self.g.add((use, CRM.P2_has_type, self.typ("use phase")))
                self.g.add((use, CRM.P12_occurred_in_the_presence_of, target))
                self.g.add((use, CRM.P4_has_time_span, ts))
                self.provenance(use, an.get("pages"))
                a = self.assignment(f"c14-dating-{an['id']}", f"{self.g.value(target, RDFS.label)} – karbon 14 ile tarihleme",
                                    "radiocarbon dating", use, ts, CRM.P4_has_time_span,
                                    by=an.get("concluded_by"), via="laboratory analysis", pages=an.get("pages"))
                self.g.add((a, CRM.P17_was_motivated_by, obs))

    def relations(self):
        """Stratigraphic statements between contexts.

        Physical relations (cuts, destroys, overlies ...) use CRMarchaeo AP11
        between A8 Stratigraphic Units; both ends are therefore also typed A8.
        The relation type (AP11.1) cannot hang on a plain triple, so every
        relation is also an E13 Attribute Assignment carrying the type, the
        certainty and the page.  'contemporary with' has no CRMarchaeo property
        between units; it uses the project property kst:contemporaryWith.
        """
        for r in self.rec.get("relations", []):
            a, b = self.resolve(r["from"]), self.resolve(r["to"])
            if r["type"] in PHYSICAL_RELATIONS:
                prop = ARCH.AP11_has_physical_relation_to
                for end in (a, b):
                    self.g.add((end, RDF.type, ARCH.A8_Stratigraphic_Unit))
            else:
                prop = self.KST[re.sub(r"\s+(\w)", lambda m: m.group(1).upper(), r["type"])]
            self.g.add((a, prop, b))
            label = f"{self.g.value(a, RDFS.label)} → {r['type']} → {self.g.value(b, RDFS.label)}"
            s = self.assignment(r["id"], label, "stratigraphic relation", a, b, prop,
                                by=r.get("by"), note=r.get("note"), pages=r.get("pages"))
            self.g.add((s, CRM.P2_has_type, self.typ(r["type"], broader="stratigraphic relation type")))
            if r.get("certainty"):
                self.g.add((s, CRM.P2_has_type, self.typ(r["certainty"], broader="certainty")))

    def plans(self):
        """Work announced for the future is a plan (E29), never an activity."""
        for p in self.rec.get("plans", []):
            s = self.uri("plan", p["id"])
            self.add(s, CRM.E29_Design_or_Procedure, p["label"])
            self.g.add((s, CRM.P2_has_type, self.typ("planned work")))
            for target in p.get("about", []):
                self.g.add((s, CRM.P67_refers_to, self.resolve(target)))
            if p.get("place"):
                self.g.add((s, CRM.P67_refers_to, self.uri("place", p["place"])))
            if p.get("planned_for"):
                self.g.add((s, self.KST.plannedFor, Literal(int(p["planned_for"]), datatype=XSD.integer)))
            self.note(s, p.get("note"))
            self.provenance(s, p.get("pages"))

    def interpretations(self):
        for i in self.rec.get("interpretations", []):
            s = self.uri("interpretation", i["id"])
            self.add(s, CRM.E13_Attribute_Assignment, i["assigned"])
            self.g.add((s, CRM.P2_has_type, self.typ("interpretation")))
            self.g.add((s, CRM.P140_assigned_attribute_to, self.resolve(i["about"])))
            self.g.add((s, CRM.P141_assigned, self.typ(i["assigned"], lang="tr")))
            self.g.add((s, CRM.P177_assigned_property_of_type, CRM.P2_has_type))
            for by in i.get("by", []):
                self.g.add((s, CRM.P14_carried_out_by, self.uri("actor", by)))
            if i.get("basis"):
                self.note(s, "Gerekçe: " + i["basis"])
            self.provenance(s, i.get("pages"))

    def figures(self):
        for fig in self.rec.get("figures", []):
            fid = fig.get("id") or f"resim-{fig['number']}"
            kind = fig.get("kind", "Resim")
            s = self.uri("figure", fid)
            self.add(s, CRM.E36_Visual_Item, f"{kind} {fig['number']}: {fig['caption']}")
            self.g.add((s, CRM.P2_has_type, self.typ("figure")))
            self.g.add((s, CRM.P2_has_type, self.typ(kind, broader="figure", lang="tr")))
            self.g.add((self.report, CRM.P106_is_composed_of, s))
            self.g.add((s, CRM.P106i_forms_part_of, self.report))
            self.g.add((s, self.KST.sourcePage, Literal(fig["page"], datatype=XSD.integer)))
            for target in fig.get("depicts", []):
                t = self.resolve(target)
                self.g.add((s, CRM.P138_represents, t))
                self.g.add((t, CRM.P138i_has_representation, s))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("record", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--format", default="turtle")
    args = ap.parse_args(argv)
    record = json.loads(args.record.read_text(encoding="utf-8"))
    g = Builder(record).build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(args.out), format=args.format)
    print(f"{args.out}: {len(g)} triples, {len(set(g.subjects()))} subjects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
