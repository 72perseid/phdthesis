#!/usr/bin/env python3
"""
excavation_db.py - The relational step between a report and its CIDOC CRM graph.

    record (JSON)  ->  tables (SQLite, schema.sql)  ->  graph (Turtle)

The tables only accept classes that exist in the official ontology files
(ontology/*.rdf), every reference must point at an existing row, and every
column has one fixed CRM path (crm_mapping.csv).  The graph is generated from
the tables by build_graph.py, never chosen by a model.

Usage
  python db/excavation_db.py init   out/excavations.sqlite
  python db/excavation_db.py load   out/excavations.sqlite data/yumuktepe_2024.json
  python db/excavation_db.py graph  out/excavations.sqlite yumuktepe-2024 -o out/yumuktepe_2024.ttl
  python db/excavation_db.py check  out/excavations.sqlite yumuktepe-2024 data/yumuktepe_2024.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from build_graph import PHYSICAL_RELATIONS, Builder  # noqa: E402

ONTOLOGIES = (
    ("CIDOC CRM 7.1.3", "CIDOC_CRM_v7.1.3.rdf"),
    ("CRMarchaeo 2.1.1", "CRMarchaeo_v2.1.1.rdf"),
    ("CRMsci 3.2", "CRMsci_v3.2.rdf"),
)

# order in which build_graph.py resolves a bare id to a kind of thing
RESOLVE_ORDER = (("feature", "features"), ("find", "finds"), ("stratum", "strata"),
                 ("activity", "activities"), ("sample", "samples"), ("place", "places"),
                 ("plan", "plans"), ("actor", "actors"))
OTHER_KINDS = (("period", "periods"), ("analysis", "analyses"), ("relation", "relations"),
               ("interpretation", "interpretations"), ("figure", "figures"),
               ("reference", "references"), ("documentation", "records"))


class UnknownField(ValueError):
    """The record holds something the tables have no column for."""


# ----------------------------------------------------------------------------
# init
# ----------------------------------------------------------------------------

def init(path: Path) -> sqlite3.Connection:
    from rdflib import OWL, RDF, RDFS, Graph

    if path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = connect(path)
    con.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))

    def name(uri) -> str:
        return str(uri).rstrip("/").rsplit("/", 1)[-1]

    for label, filename in ONTOLOGIES:
        g = Graph().parse(ROOT / "ontology" / filename)
        classes = set(g.subjects(RDF.type, RDFS.Class)) | set(g.subjects(RDF.type, OWL.Class))
        props = set(g.subjects(RDF.type, RDF.Property)) | set(g.subjects(RDF.type, OWL.ObjectProperty)) \
            | set(g.subjects(RDF.type, OWL.DatatypeProperty))
        for c in classes:
            con.execute("INSERT OR IGNORE INTO ontology_term VALUES (?,?,?,?,NULL,NULL)",
                        (name(c), "class", label, str(c)))
        for p in props:
            d, r = g.value(p, RDFS.domain), g.value(p, RDFS.range)
            con.execute("INSERT OR IGNORE INTO ontology_term VALUES (?,?,?,?,?,?)",
                        (name(p), "property", label, str(p), name(d) if d else None, name(r) if r else None))
    for label, filename in ONTOLOGIES:       # parents may live in another file: second pass
        g = Graph().parse(ROOT / "ontology" / filename)
        known = {row[0] for row in con.execute("SELECT name FROM ontology_term")}
        for c, parent in g.subject_objects(RDFS.subClassOf):
            if name(c) in known and name(parent) in known:
                con.execute("INSERT OR IGNORE INTO ontology_subclass VALUES (?,?)", (name(c), name(parent)))

    for rel in sorted(PHYSICAL_RELATIONS):
        con.execute("INSERT INTO relation_type VALUES (?,1)", (rel,))
    con.execute("INSERT INTO relation_type VALUES ('contemporary with',0)")

    with open(HERE / "crm_mapping.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            con.execute("INSERT INTO crm_mapping VALUES (?,?,?,?)",
                        (row["table_name"], row["column_name"], row["meaning"], row["crm_path"]))
    missing = unmapped_columns(con)
    if missing:
        raise SystemExit("columns without a CRM path in crm_mapping.csv: " + ", ".join(missing))
    con.commit()
    return con


def connect(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


STRUCTURAL = {"report", "id", "position", "activity", "analysis", "plan", "figure", "interpretation", "documentation"}
SYSTEM_TABLES = {"ontology_term", "ontology_subclass", "crm_mapping", "relation_type", "entity"}


def data_tables(con) -> list[str]:
    rows = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [r[0] for r in rows if r[0] not in SYSTEM_TABLES]


def unmapped_columns(con) -> list[str]:
    """Every column that carries content must have a row in crm_mapping."""
    mapped = {(r[0], r[1]) for r in con.execute("SELECT table_name, column_name FROM crm_mapping")}
    missing = []
    for table in data_tables(con):
        keys = {"report": {"base_uri", "shared_uri", "schema_version", "comment", "document_id"},
                "illustrated_by": {"report", "id", "position"},
                "figure_depicts": {"report", "figure", "position"}}.get(table, set())
        for col in con.execute(f'PRAGMA table_info("{table}")'):
            c = col["name"]
            if c in keys or (table, c) in mapped:
                continue
            if c in STRUCTURAL and not (table in ("illustrated_by",) and c == "figure"):
                continue
            missing.append(f"{table}.{c}")
    return missing


# ----------------------------------------------------------------------------
# load: record -> tables
# ----------------------------------------------------------------------------

class Loader:
    def __init__(self, con: sqlite3.Connection, record: dict):
        self.con, self.rec = con, record
        self.report = record["base_uri"].rstrip("/").rsplit("/", 1)[-1]

    def take(self, item: dict, where: str, *keys: str) -> dict:
        """Return the known keys; refuse anything the tables cannot hold."""
        unknown = set(item) - set(keys)
        if unknown:
            raise UnknownField(f"{where}: no column for {sorted(unknown)}")
        return {k: item.get(k) for k in keys}

    def insert(self, table: str, **values):
        cols = ", ".join(f'"{c}"' for c in values)
        marks = ", ".join("?" for _ in values)
        self.con.execute(f'INSERT INTO "{table}" ({cols}) VALUES ({marks})', tuple(values.values()))

    def entity(self, ident: str, kind: str, pages=None, figures=None):
        self.insert("entity", report=self.report, id=ident, kind=kind)
        for p in pages or []:
            self.insert("source_page", report=self.report, id=ident, page=int(p))
        for i, f in enumerate(figures or []):
            self.insert("illustrated_by", report=self.report, id=ident, position=i, figure=figure_id(f))

    def many(self, table: str, ident: str, column: str, values, **fixed):
        for i, v in enumerate(values or []):
            self.insert(table, report=self.report, position=i, **fixed, **{column: v})

    def shared(self, item: dict, where: str):
        """dating, dimensions, taxa, comparanda, attributions: the same for contexts, finds and samples."""
        ident = item["id"]
        periods = item.get("periods") or ([item["period"]] if item.get("period") else [])
        for i, p in enumerate(periods):
            self.insert("dating", report=self.report, id=ident, position=i, period=p,
                        certainty=item.get("dating_certainty"))
        self.sources(item, where)
        for i, d in enumerate(item.get("dimensions") or []):
            d = self.take(d, f"{where}.dimensions", "type", "value", "min", "max", "unit", "approx")
            self.insert("dimension", report=self.report, id=ident, position=i, **d)
        for i, t in enumerate(item.get("taxa") or []):
            self.insert("taxon", report=self.report, id=ident, position=i, name=t)
        for i, c in enumerate(item.get("comparanda") or []):
            c = self.take(c, f"{where}.comparanda", "label", "refs")
            self.insert("comparandum", report=self.report, id=ident, position=i, **c)
        for key, about in (("dating_by", "dating"), ("identified_by", "identification")):
            if item.get(key):
                a = self.take(item[key], f"{where}.{key}", "by", "via")
                self.insert("attribution", report=self.report, id=ident, about=about, via=a["via"])
                for i, actor in enumerate(a["by"] or []):
                    self.insert("attribution_actor", report=self.report, id=ident, about=about, position=i, actor=actor)

    def sources(self, item: dict, where: str):
        for i, c in enumerate(item.get("sources") or []):
            c = self.take(c, f"{where}.sources", "ref", "pages")
            self.insert("cited_for", report=self.report, id=item["id"], position=i, reference=c["ref"], pages=c["pages"])

    SHARED = ("period", "periods", "dating_certainty", "dimensions", "taxa", "comparanda", "dating_by", "identified_by",
              "sources")

    def load(self):
        rec, rep = self.rec, self.report
        self.take(rec, "record", "$comment", "base_uri", "shared_uri", "schema_version", "document",
                  *(k for _, k in RESOLVE_ORDER + OTHER_KINDS))
        self.con.execute("BEGIN")
        self.con.execute("PRAGMA defer_foreign_keys = ON")   # rows may refer to rows loaded later

        d = self.take(rec["document"], "document", "id", "title", "language", "authors", "pages",
                      "published", "documents", "source_file", "volume")
        v = d["volume"]
        if v:
            v = self.take(v, "document.volume", "id", "title", "editor", "publisher", "isbn", "place", "published")
            self.con.execute("INSERT OR IGNORE INTO volume VALUES (?,?,?,?,?,?,?)",
                             (v["id"], v["title"], v["editor"], v["publisher"], v["isbn"], v["place"], v["published"]))
        self.insert("report", id=rep, base_uri=rec["base_uri"], shared_uri=rec.get("shared_uri"),
                    schema_version=rec.get("schema_version"), comment=rec.get("$comment"),
                    document_id=d["id"], title=d["title"], language=d["language"] or "tr",
                    printed_pages=d["pages"], published=d["published"], source_file=d["source_file"],
                    reports_on=d["documents"], volume_id=v["id"] if v else None)

        for a in rec.get("actors", []):
            x = self.take(a, f"actors/{a.get('id')}", "id", "class", "label", "orcid", "member_of", "note", "pages")
            self.entity(x["id"], "actor", x.pop("pages"))
            self.insert("actor", report=rep, **x)
        self.many("report_author", rep, "actor", d["authors"])

        for p in rec.get("places", []):
            x = self.take(p, f"places/{p.get('id')}", "id", "label", "type", "within", "note", "pages")
            self.entity(x["id"], "place", x.pop("pages"))
            self.insert("place", report=rep, **x)

        for p in rec.get("periods", []):
            x = self.take(p, f"periods/{p.get('id')}", "id", "label", "begin", "end", "approx", "within", "pages")
            self.entity(x["id"], "period", x.pop("pages"))
            self.insert("period", report=rep, id=x["id"], label=x["label"], begin_year=x["begin"],
                        end_year=x["end"], approx=x["approx"], within=x["within"])

        for kind, key in (("feature", "features"), ("stratum", "strata")):
            for c in rec.get(key, []):
                where = f"{key}/{c.get('id')}"
                x = self.take(c, where, "id", "class", "label", "identifier", "type", "part_of", "location",
                              "at_feature", "count", "note", "pages", "figures", *self.SHARED)
                self.entity(x["id"], kind, x["pages"], x["figures"])
                self.insert("context", report=rep, kind=kind, id=x["id"],
                            **{"class": x["class"] or "A2_Stratigraphic_Volume_Unit"},
                            label=x["label"], identifier=x["identifier"], type=x["type"], part_of=x["part_of"],
                            location=x["location"], at_feature=x["at_feature"], count=x["count"], note=x["note"])
                self.shared(c, where)

        for a in rec.get("activities", []):
            where = f"activities/{a.get('id')}"
            x = self.take(a, where, "id", "class", "type", "label", "timespan", "carried_out_by", "took_place_at",
                          "at_feature", "also_at", "part_of", "continued", "investigated", "removed", "used",
                          "purpose_of", "identifier", "note", "pages", "figures", "produced", "excavated", "sources")
            ts = self.take(x["timespan"] or {}, f"{where}.timespan", "begin", "end", "approx")
            self.entity(x["id"], "activity", x["pages"], x["figures"])
            self.insert("activity", report=rep, id=x["id"], **{"class": x["class"]}, type=x["type"], label=x["label"],
                        begin_year=ts["begin"], end_year=ts["end"], approx=ts["approx"], part_of=x["part_of"],
                        at_feature=x["at_feature"], investigated=x["investigated"], purpose_of=x["purpose_of"],
                        identifier=x["identifier"], note=x["note"])
            for i, e in enumerate(x["carried_out_by"] or []):
                e = self.take(e, f"{where}.carried_out_by", "actor", "role")
                self.insert("activity_actor", report=rep, activity=x["id"], position=i, **e)
            for link in ("took_place_at", "also_at", "continued", "removed", "used", "produced"):
                self.many("activity_link", rep, "target", x[link], activity=x["id"], link=link)
            for i, dim in enumerate(x["excavated"] or []):
                dim = self.take(dim, f"{where}.excavated", "type", "value", "min", "max", "unit", "approx")
                self.insert("dimension", report=rep, id=x["id"], position=i, **dim)
            self.sources(a, where)

        for p in rec.get("plans", []):
            x = self.take(p, f"plans/{p.get('id')}", "id", "label", "planned_for", "about", "place", "note", "pages")
            self.entity(x["id"], "plan", x["pages"])
            self.insert("plan", report=rep, id=x["id"], label=x["label"], planned_for=x["planned_for"],
                        place=x["place"], note=x["note"])
            self.many("plan_about", rep, "target", x["about"], plan=x["id"])

        for f in rec.get("finds", []):
            where = f"finds/{f.get('id')}"
            x = self.take(f, where, "id", "class", "label", "type", "count", "material", "found_by", "at_feature",
                          "from_stratum", "condition", "depicts", "inscribed", "part_of", "note", "pages", "figures",
                          *self.SHARED)
            self.entity(x["id"], "find", x["pages"], x["figures"])
            self.insert("find", report=rep, **{k: x[k] for k in ("id", "class", "label", "type", "count", "material",
                                                                "found_by", "at_feature", "from_stratum", "condition",
                                                                "depicts", "inscribed", "part_of", "note")})
            self.shared(f, where)

        for s in rec.get("samples", []):
            where = f"samples/{s.get('id')}"
            x = self.take(s, where, "id", "class", "label", "material_type", "taken_from", "taken_during", "note",
                          "pages", "figures", *self.SHARED)
            self.entity(x["id"], "sample", x["pages"], x["figures"])
            self.insert("sample", report=rep, id=x["id"], **{"class": x["class"] or "S13_Sample"}, label=x["label"],
                        material_type=x["material_type"], taken_from=x["taken_from"],
                        taken_during=x["taken_during"], note=x["note"])
            self.shared(s, where)

        for a in rec.get("analyses", []):
            where = f"analyses/{a.get('id')}"
            x = self.take(a, where, "id", "type", "label", "samples", "result", "dates", "by", "concluded_by",
                          "note", "pages")
            res = self.take(x["result"], f"{where}.result", "begin", "end")
            self.entity(x["id"], "analysis", x["pages"])
            self.insert("analysis", report=rep, id=x["id"], type=x["type"], label=x["label"],
                        result_begin=res["begin"], result_end=res["end"], dates=x["dates"], note=x["note"])
            self.many("analysis_sample", rep, "sample", x["samples"], analysis=x["id"])
            for part in ("by", "concluded_by"):
                self.many("analysis_actor", rep, "actor", x[part], analysis=x["id"], part=part)

        for r in rec.get("relations", []):
            x = self.take(r, f"relations/{r.get('id')}", "id", "from", "to", "type", "certainty", "by", "note", "pages")
            if x["by"]:
                raise UnknownField(f"relations/{x['id']}: no column for 'by' yet")
            self.entity(x["id"], "relation", x["pages"])
            self.insert("relation", report=rep, id=x["id"], from_context=x["from"], type=x["type"],
                        to_context=x["to"], certainty=x["certainty"], note=x["note"])

        for i in rec.get("interpretations", []):
            x = self.take(i, f"interpretations/{i.get('id')}", "id", "about", "assigned", "by", "basis", "pages")
            self.entity(x["id"], "interpretation", x["pages"])
            self.insert("interpretation", report=rep, id=x["id"], about=x["about"], assigned=x["assigned"],
                        basis=x["basis"])
            self.many("interpretation_actor", rep, "actor", x["by"], interpretation=x["id"])

        for r in rec.get("references", []):
            x = self.take(r, f"references/{r.get('id')}", "id", "citation", "year", "note", "pages")
            self.entity(x["id"], "reference", x.pop("pages"))
            self.insert("reference", report=rep, **x)

        for r in rec.get("records", []):
            x = self.take(r, f"records/{r.get('id')}", "id", "type", "label", "scale", "made_by", "depicts", "note",
                          "pages", "figures")
            self.entity(x["id"], "documentation", x["pages"], x["figures"])
            self.insert("documentation", report=rep, id=x["id"], type=x["type"], label=x["label"], scale=x["scale"],
                        made_by=x["made_by"], note=x["note"])
            self.many("documentation_depicts", rep, "target", x["depicts"], documentation=x["id"])

        for f in rec.get("figures", []):
            x = self.take(f, f"figures/{f.get('number')}", "id", "kind", "number", "caption", "depicts", "page")
            fid = x["id"] or f"resim-{x['number']}"
            self.entity(fid, "figure")
            self.insert("figure", report=rep, id=fid, kind=x["kind"] or "Resim", number=x["number"],
                        caption=x["caption"], page=x["page"])
            self.many("figure_depicts", rep, "target", x["depicts"], figure=fid)

        self.con.commit()           # deferred foreign keys are checked here
        return rep


def figure_id(ref) -> str:
    return f"resim-{ref}" if isinstance(ref, int) or str(ref).isdigit() else str(ref)


# ----------------------------------------------------------------------------
# export: tables -> record -> graph
# ----------------------------------------------------------------------------

def clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and v != [] and v != {}}


def year(v):
    return None if v is None else str(v)


class Exporter:
    def __init__(self, con: sqlite3.Connection, report: str):
        self.con, self.report = con, report

    def rows(self, sql: str, *args):
        return self.con.execute(sql, (self.report, *args)).fetchall()

    def col(self, sql: str, *args) -> list:
        return [r[0] for r in self.rows(sql, *args)]

    def pages(self, ident):
        return self.col("SELECT page FROM source_page WHERE report=? AND id=? ORDER BY page", ident)

    def figures(self, ident):
        return self.col("SELECT figure FROM illustrated_by WHERE report=? AND id=? ORDER BY position", ident)

    def sources(self, ident) -> list:
        return [clean({"ref": r["reference"], "pages": r["pages"]}) for r in self.rows(
            "SELECT * FROM cited_for WHERE report=? AND id=? ORDER BY position", ident)]

    def dimensions(self, ident) -> list:
        return [clean({"type": r["type"], "value": r["value"], "min": r["min"], "max": r["max"],
                       "unit": r["unit"], "approx": bool(r["approx"]) if r["approx"] is not None else None})
                for r in self.rows("SELECT * FROM dimension WHERE report=? AND id=? ORDER BY position", ident)]

    def shared(self, ident) -> dict:
        certainty = self.col("SELECT DISTINCT certainty FROM dating WHERE report=? AND id=? AND certainty IS NOT NULL", ident)
        out = {
            "sources": self.sources(ident),
            "dating_certainty": certainty[0] if certainty else None,
            "periods": self.col("SELECT period FROM dating WHERE report=? AND id=? ORDER BY position", ident),
            "dimensions": [clean({"type": r["type"], "value": r["value"], "min": r["min"], "max": r["max"],
                                  "unit": r["unit"], "approx": bool(r["approx"]) if r["approx"] is not None else None})
                           for r in self.rows("SELECT * FROM dimension WHERE report=? AND id=? ORDER BY position", ident)],
            "taxa": self.col("SELECT name FROM taxon WHERE report=? AND id=? ORDER BY position", ident),
            "comparanda": [clean({"label": r["label"], "refs": r["refs"]})
                           for r in self.rows("SELECT * FROM comparandum WHERE report=? AND id=? ORDER BY position", ident)],
        }
        for key, about in (("dating_by", "dating"), ("identified_by", "identification")):
            for r in self.rows("SELECT via FROM attribution WHERE report=? AND id=? AND about=?", ident, about):
                out[key] = clean({"by": self.col("SELECT actor FROM attribution_actor WHERE report=? AND id=? AND about=? "
                                                 "ORDER BY position", ident, about), "via": r["via"]})
        return out

    def item(self, row, *skip, shared=False, figures=True) -> dict:
        d = {k: row[k] for k in row.keys() if k not in ("report", "kind", *skip)}
        for flag in ("approx", "inscribed"):
            if d.get(flag) is not None:
                d[flag] = bool(d[flag])
        d["pages"] = self.pages(row["id"])
        if figures:
            d["figures"] = self.figures(row["id"])
        if shared:
            d |= self.shared(row["id"])
        return d

    def record(self) -> dict:
        rep = self.con.execute("SELECT * FROM report WHERE id=?", (self.report,)).fetchone()
        if rep is None:
            raise SystemExit(f"no report '{self.report}' in the database")
        vol = self.con.execute("SELECT * FROM volume WHERE id=?", (rep["volume_id"],)).fetchone()
        rec = clean({
            "$comment": rep["comment"], "schema_version": rep["schema_version"],
            "base_uri": rep["base_uri"], "shared_uri": rep["shared_uri"],
            "document": clean({
                "id": rep["document_id"], "title": rep["title"], "language": rep["language"],
                "authors": self.col("SELECT actor FROM report_author WHERE report=? ORDER BY position"),
                "pages": rep["printed_pages"], "published": year(rep["published"]),
                "documents": rep["reports_on"], "source_file": rep["source_file"],
                "volume": clean({**dict(vol), "published": year(vol["published"])}) if vol else None,
            }),
        })
        order = "ORDER BY rowid"
        rec["actors"] = [clean(self.item(r, figures=False)) for r in self.rows(f"SELECT * FROM actor WHERE report=? {order}")]
        rec["places"] = [clean(self.item(r, figures=False)) for r in self.rows(f"SELECT * FROM place WHERE report=? {order}")]
        rec["periods"] = []
        for r in self.rows(f"SELECT * FROM period WHERE report=? {order}"):
            d = self.item(r, "begin_year", "end_year", figures=False)
            rec["periods"].append(clean(d | {"begin": year(r["begin_year"]), "end": year(r["end_year"])}))
        for kind, key in (("feature", "features"), ("stratum", "strata")):
            rec[key] = [clean(self.item(r, shared=True))
                        for r in self.rows(f"SELECT * FROM context WHERE report=? AND kind=? {order}", kind)]
        rec["activities"] = []
        for r in self.rows(f"SELECT * FROM activity WHERE report=? {order}"):
            d = self.item(r, "begin_year", "end_year", "approx")
            d["timespan"] = clean({"begin": year(r["begin_year"]), "end": year(r["end_year"]),
                                   "approx": bool(r["approx"]) if r["approx"] is not None else None})
            d["carried_out_by"] = [clean({"actor": a["actor"], "role": a["role"]}) for a in self.rows(
                "SELECT * FROM activity_actor WHERE report=? AND activity=? ORDER BY position", r["id"])]
            d["excavated"] = self.dimensions(r["id"])
            d["sources"] = self.sources(r["id"])
            for link in ("took_place_at", "also_at", "continued", "removed", "used", "produced"):
                d[link] = self.col("SELECT target FROM activity_link WHERE report=? AND activity=? AND link=? "
                                   "ORDER BY position", r["id"], link)
            rec["activities"].append(clean(d))
        rec["plans"] = []
        for r in self.rows(f"SELECT * FROM plan WHERE report=? {order}"):
            d = self.item(r, figures=False)
            d["planned_for"] = year(r["planned_for"])
            d["about"] = self.col("SELECT target FROM plan_about WHERE report=? AND plan=? ORDER BY position", r["id"])
            rec["plans"].append(clean(d))
        rec["finds"] = [clean(self.item(r, shared=True)) for r in self.rows(f"SELECT * FROM find WHERE report=? {order}")]
        rec["samples"] = [clean(self.item(r, shared=True)) for r in self.rows(f"SELECT * FROM sample WHERE report=? {order}")]
        rec["analyses"] = []
        for r in self.rows(f"SELECT * FROM analysis WHERE report=? {order}"):
            d = self.item(r, "result_begin", "result_end", figures=False)
            d["result"] = {"begin": year(r["result_begin"]), "end": year(r["result_end"])}
            d["samples"] = self.col("SELECT sample FROM analysis_sample WHERE report=? AND analysis=? ORDER BY position", r["id"])
            for part in ("by", "concluded_by"):
                d[part] = self.col("SELECT actor FROM analysis_actor WHERE report=? AND analysis=? AND part=? "
                                   "ORDER BY position", r["id"], part)
            rec["analyses"].append(clean(d))
        rec["relations"] = []
        for r in self.rows(f"SELECT * FROM relation WHERE report=? {order}"):
            d = self.item(r, "from_context", "to_context", figures=False)
            rec["relations"].append(clean(d | {"from": r["from_context"], "to": r["to_context"]}))
        rec["interpretations"] = []
        for r in self.rows(f"SELECT * FROM interpretation WHERE report=? {order}"):
            d = self.item(r, figures=False)
            d["by"] = self.col("SELECT actor FROM interpretation_actor WHERE report=? AND interpretation=? "
                               "ORDER BY position", r["id"])
            rec["interpretations"].append(clean(d))
        rec["references"] = []
        for r in self.rows(f"SELECT * FROM reference WHERE report=? {order}"):
            rec["references"].append(clean(self.item(r, figures=False) | {"year": year(r["year"])}))
        rec["records"] = []
        for r in self.rows(f"SELECT * FROM documentation WHERE report=? {order}"):
            d = self.item(r)
            d["depicts"] = self.col("SELECT target FROM documentation_depicts WHERE report=? AND documentation=? "
                                    "ORDER BY position", r["id"])
            rec["records"].append(clean(d))
        rec["figures"] = []
        for r in self.rows(f"SELECT * FROM figure WHERE report=? {order}"):
            d = {k: r[k] for k in ("id", "kind", "number", "caption", "page")}
            d["depicts"] = self.col("SELECT target FROM figure_depicts WHERE report=? AND figure=? ORDER BY position", r["id"])
            rec["figures"].append(d)
        return rec

    def graph(self):
        return Builder(self.record()).build()


# ----------------------------------------------------------------------------
# command line
# ----------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("db", type=Path)
    p = sub.add_parser("load"); p.add_argument("db", type=Path); p.add_argument("records", type=Path, nargs="+")
    p = sub.add_parser("graph"); p.add_argument("db", type=Path); p.add_argument("report")
    p.add_argument("-o", "--out", type=Path, required=True)
    p = sub.add_parser("check"); p.add_argument("db", type=Path); p.add_argument("report")
    p.add_argument("record", type=Path)
    args = ap.parse_args(argv)

    if args.cmd == "init":
        con = init(args.db)
        n = {k: con.execute("SELECT count(*) FROM ontology_term WHERE kind=?", (k,)).fetchone()[0]
             for k in ("class", "property")}
        print(f"{args.db}: {len(data_tables(con))} data tables, "
              f"{con.execute('SELECT count(*) FROM crm_mapping').fetchone()[0]} mapped columns, "
              f"{n['class']} ontology classes, {n['property']} properties")
        return 0

    con = connect(args.db)
    if args.cmd == "load":
        for path in args.records:
            rep = Loader(con, json.loads(path.read_text(encoding="utf-8"))).load()
            rows = sum(con.execute(f'SELECT count(*) FROM "{t}" WHERE report=?', (rep,)).fetchone()[0]
                       for t in data_tables(con) if t not in ("volume", "report"))
            print(f"{rep}: {rows} rows")
    elif args.cmd == "graph":
        g = Exporter(con, args.report).graph()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        g.serialize(destination=str(args.out), format="turtle")
        print(f"{args.out}: {len(g)} triples, {len(set(g.subjects()))} subjects")
    elif args.cmd == "check":
        direct = set(Builder(json.loads(args.record.read_text(encoding="utf-8"))).build())
        via_db = set(Exporter(con, args.report).graph())
        lost, extra = direct - via_db, via_db - direct
        print(f"{args.report}: {len(direct)} triples direct, {len(via_db)} through the tables, "
              f"{len(lost)} lost, {len(extra)} added")
        for label, triples in (("lost", lost), ("added", extra)):
            for t in sorted(triples)[:20]:
                print(f"  {label}: " + "  ".join(str(x) for x in t))
        return 1 if lost or extra else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
