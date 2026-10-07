#!/usr/bin/env python3
"""Load a record of version 1 into the version 2 database. A test tool, not part of the design.

    from_v1.py DB RECORD.json [RECORD.json ...]

Every statement of the record is tried on its own. What the database refuses is listed and counted.
What has no place is listed too. Nothing is forced in.
"""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

from fieldwork_db import Loader, Refused, connect

FIGURE_TYPE = {"Resim": "photograph", "Şekil": "drawing", "Tablo": "table", "Plan": "plan", "Harita": "map"}
INVERSE = {"is cut by": "cuts", "underlies": "overlies", "is filled by": "fills"}
BELIEF = {"uncertain": "possible", "one of": "possible", "interpreted": "probable"}
METHOD_WORDS = [("radiocarbon", "laboratory_measurement"), ("stratigraph", "stratigraphic_position"),
                ("coin", "coin_evidence"), ("sikke", "coin_evidence"), ("inscription", "inscription"),
                ("pottery", "typological_comparison"), ("typolog", "typological_comparison"),
                ("technique", "building_technique"), ("architect", "building_technique")]


class Converter:
    def __init__(self, con, record, name):
        self.con, self.d, self.ds = con, record, name
        self.L = Loader(con, name)
        self.refused, self.lost = [], Counter()
        self.passages, self.groups, self.classes, self.abouts = {}, {}, {}, set()
        self.tried = 0
        self.wholes = {f["part_of"] for f in record.get("finds", []) if f.get("part_of")}

    def id(self, v1):
        return f"{self.ds}/{v1}"

    def attempt(self, what, fn, *a, **k):
        """One statement. A refusal is recorded and the load goes on."""
        self.tried += 1
        self.con.execute("SAVEPOINT one")
        try:
            out = fn(*a, **k)
            self.con.execute("RELEASE one")
            return out
        except (sqlite3.IntegrityError, Refused, KeyError) as e:
            self.con.execute("ROLLBACK TO one")
            self.con.execute("RELEASE one")
            self.refused.append(f"{what}: {e}")
            return None

    def no_place(self, what):
        self.lost[what] += 1

    def is_a(self, eid, sup):
        return self.con.execute("SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2) "
                                "WHERE e.id = ? AND s.super = ?", (eid, sup)).fetchone() is not None

    def fig(self, f):
        return self.id(f"resim-{f}" if isinstance(f, int) else f)

    def about(self, what, item, target):
        """The same link is often given twice in a record of version 1. It is stored once."""
        if (item, target) not in self.abouts:
            self.abouts.add((item, target))
            self.attempt(what, self.L.insert, "about", item=item, target=target)

    def claim_passage(self, e):
        if not e.get("pages"):
            return None
        return self.passage(self.report, ", ".join(str(p) for p in e["pages"]))

    def entity(self, table, e, cls, **cols):
        return self.attempt(f"{table} {e['id']}", self.L.entity, table, cls, label=e.get("label"),
                            remark=e.get("note"), eid=self.id(e["id"]), source_id=e["id"], **cols)

    # ── shared pieces ──
    def passage(self, source, locator):
        key = (source, str(locator))
        if key not in self.passages:
            self.passages[key] = self.L.entity("passage", "E31", label=f"s. {locator}", source=source,
                                               locator=str(locator))
        return self.passages[key]

    def pages(self, e):
        for p in e.get("pages", []):
            self.about(f"page {p} of {e['id']}", self.passage(self.report, p), self.id(e["id"]))

    def figures(self, e):
        for f in e.get("figures", []):
            self.about(f"figure {f} of {e['id']}", self.fig(f), self.id(e["id"]))

    def group(self, actors):
        """Several people behind one claim are a group."""
        key = tuple(sorted(actors))
        if len(key) == 1:
            return self.id(key[0])
        if key not in self.groups:
            names = [self.con.execute("SELECT label FROM entity WHERE id = ?", (self.id(a),)).fetchone() for a in key]
            g = self.L.entity("actor", "E74", label=", ".join(n["label"] for n in names if n))
            for a in key:
                self.L.insert("relation", subject=g, type="member", object=self.id(a))
            self.groups[key] = g
        return self.groups[key]

    def claim(self, by=None, belief="true", via=None, passage=None):
        kind, method, remark = "recorded", None, None
        if by and by.get("via"):
            kind, remark = "inferred", by["via"]
            low = by["via"].lower()
            method = next((f"reasoning_method/{m}" for w, m in METHOD_WORDS if w in low), None)
            if "personal communication" in low:
                kind, method = "recorded", None
        made_by = self.group(by["by"]) if by and by.get("by") else None
        return self.L.claim(belief=belief, kind=kind, method=method, made_by=made_by, remark=remark)

    def dimensions(self, e, eid):
        for d in e.get("dimensions", []) + e.get("excavated", []):
            kind = d["type"]
            kind = {"mass": "removed_mass"}.get(kind, kind) if "excavated" in e and d in e["excavated"] else kind
            unit = {"l": "litre", "t": "tonne"}.get(d.get("unit"), d.get("unit"))
            self.attempt(f"dimension {kind} of {e['id']}", self.L.insert, "dimension", entity=eid, kind=kind,
                         value=d.get("value"), value_min=d.get("min"), value_max=d.get("max"), unit=unit,
                         approx=1 if d.get("approx") else 0)
        if "count" in e:
            # The count of an assemblage that is broken down further is a total as printed.
            kind = "count_printed" if e["id"] in self.wholes else "count"
            self.attempt(f"count of {e['id']}", self.L.insert, "dimension", entity=eid,
                         kind=f"dimension_kind/{kind}", value=e["count"], unit="unit/piece")

    def event_for(self, eid):
        if self.is_a(eid, "E20"):
            return "death"
        if self.is_a(eid, "E24"):
            return "making"
        if self.is_a(eid, "A8"):
            return "formation"
        return "existence"

    def dating(self, e, eid):
        periods = ([e["period"]] if e.get("period") else []) + e.get("periods", [])
        belief = BELIEF.get(e.get("dating_certainty"), "true")
        for p in periods:
            def one(p=p):
                c = self.claim(e.get("dating_by"), belief)
                self.L.insert("dating", subject=eid, event=self.event_for(eid), period=self.id(p), claim=c)
            self.attempt(f"dating of {e['id']} to {p}", one)

    def identifier(self, e, eid, typ):
        if e.get("identifier"):
            self.attempt(f"identifier of {e['id']}", self.L.insert, "identifier", entity=eid,
                         type=f"identifier_type/{typ}", value=e["identifier"])

    def relation(self, what, subject, typ, obj, claim=None, remark=None):
        def one():
            t = self.con.execute("SELECT conclusion FROM relation_type WHERE code = ?", (typ,)).fetchone()
            if t and t["conclusion"]:
                self.L.insert("assertion", subject=subject, property=typ, object_entity=obj,
                              claim=claim or self.L.claim())
            else:
                self.L.insert("relation", subject=subject, type=typ, object=obj, claim=claim, remark=remark)
        self.attempt(what, one)

    def assertion(self, what, subject, prop, claim=None, **value):
        def one():
            t = self.con.execute("SELECT code_list FROM relation_type WHERE code = ?", (prop,)).fetchone()
            v = dict(value)
            if "object_code" in v:
                v["object_code"] = self.L.code(t["code_list"], v["object_code"])
            self.L.insert("assertion", subject=subject, property=prop, claim=claim or self.L.claim(), **v)
        self.attempt(what, one)

    # ── the record ──
    def run(self):
        d, doc = self.d, self.d["document"]
        site = next((f for f in d.get("features", []) if f["class"].startswith("E27")), None)
        self.con.execute("INSERT INTO dataset (id,title,fieldwork,season,language,access,method) VALUES (?,?,?,?,?,?,?)",
                         (self.ds, doc["title"], site["label"] if site else doc["title"], "2024", "language/tr",
                          "open", "Read from the published report. See the report of version 1."))
        vol = doc["volume"]
        self.volume = self.L.entity("source", "E31", label=vol["title"], eid=self.id(vol["id"]), source_id=vol["id"],
                                    type="proceedings", year=int(vol["published"]))
        self.L.insert("identifier", entity=self.volume, type="identifier_type/isbn", value=vol["isbn"])
        self.report = self.L.entity("source", "E31", label=doc["title"], eid=self.id("report"), source_id="report",
                                    type="excavation_report", year=int(doc["published"]), language="tr",
                                    part_of=self.volume, url=doc.get("source_file"))
        self.L.insert("identifier", entity=self.report, type="identifier_type/locator", value=doc["pages"])

        for a in d.get("actors", []):
            self.entity("actor", a, a["class"].split("_")[0])
        for a in d.get("actors", []):
            aid = self.id(a["id"])
            if a.get("member_of"):
                self.attempt(f"member_of {a['id']}", self.con.execute, "UPDATE actor SET member_of = ? WHERE id = ?",
                             (self.id(a["member_of"]), aid))
            if a.get("orcid"):
                self.attempt(f"orcid {a['id']}", self.L.insert, "identifier", entity=aid,
                             type="identifier_type/orcid", value=a["orcid"])
        for a in doc["authors"]:
            self.relation(f"author {a}", self.report, "authored_by", self.id(a))
            self.attempt(f"dataset author {a}", self.L.insert, "dataset_actor", dataset=self.ds, actor=self.id(a),
                         role="author", position=doc["authors"].index(a) + 1)
        self.relation("editor", self.volume, "edited_by", self.id(vol["editor"]))
        self.relation("publisher", self.volume, "published_by", self.id(vol["publisher"]))
        if vol.get("place"):
            city = self.L.entity("place", "E53", label=vol["place"])
            self.relation("place of publication", self.volume, "published_at", city)

        for p in d.get("places", []):
            self.entity("place", p, "E53", type=p.get("type"))
        for p in d.get("places", []):
            if p.get("within"):
                self.attempt(f"place within {p['id']}", self.con.execute,
                             "UPDATE place SET part_of = ? WHERE id = ?", (self.id(p["within"]), self.id(p["id"])))

        for p in d.get("periods", []):
            b = int(p["begin"]) if p.get("begin") else None
            e = int(p["end"]) if p.get("end") else None
            self.entity("period", p, "E4", start_earliest=b, end_latest=e, scale="CE" if (b or e) else None,
                        approx=1 if p.get("approx") else 0)
        for p in d.get("periods", []):
            if p.get("within"):
                self.attempt(f"period within {p['id']}", self.con.execute,
                             "UPDATE period SET part_of = ? WHERE id = ?", (self.id(p["within"]), self.id(p["id"])))

        for r in d.get("references", []):
            self.entity("source", r, "E31", citation=r["citation"], year=int(r["year"]) if r.get("year") else None)

        for f in d.get("figures", []):
            fid = f.get("id") or f"resim-{f['number']}"
            kind = f.get("kind", "Resim")
            self.attempt(f"figure {fid}", self.L.entity, "media", "E36", label=f["caption"], eid=self.id(fid),
                         source_id=f"{kind} {f['number']}", type=FIGURE_TYPE.get(kind, kind),
                         shown_in=self.passage(self.report, f["page"]))

        things = d.get("features", []) + d.get("strata", [])
        # A wall or a pit that stands in a stratigraphic relation is also a stratigraphic unit.
        in_sequence = {x for r in d.get("relations", []) for x in (r["from"], r["to"])}
        for f in things:
            cls = f["class"].split("_")[0]
            unit = f["id"] in in_sequence and not self.con.execute(
                "SELECT 1 FROM ontology_subclass WHERE sub = ? AND super = 'A8'", (cls,)).fetchone()
            self.entity("thing", f, cls, type=f.get("type"), class2="A8" if unit else None)
            self.classes[f["id"]] = cls
            if self.is_a(self.id(f["id"]), "A8") or self.is_a(self.id(f["id"]), "E26"):
                self.attempt(f"context {f['id']}", self.L.insert, "context", id=self.id(f["id"]))
        for f in things:
            fid = self.id(f["id"])
            if f.get("part_of"):
                self.attempt(f"part_of {f['id']}", self.con.execute, "UPDATE thing SET part_of = ? WHERE id = ?",
                             (self.id(f["part_of"]), fid))
            if f.get("location"):
                self.attempt(f"location {f['id']}", self.con.execute, "UPDATE thing SET location = ? WHERE id = ?",
                             (self.id(f["location"]), fid))
            if f.get("at_feature"):
                self.relation(f"at_feature {f['id']}", fid, "lies_in", self.id(f["at_feature"]))
            self.identifier(f, fid, "context_code")
            self.dimensions(f, fid)
            self.dating(f, fid)

        for r in d.get("relations", []):
            s, o, t = self.id(r["from"]), self.id(r["to"]), r["type"]
            if t in INVERSE:
                s, o, t = o, s, INVERSE[t]
            t = t.replace(" ", "_")
            c = None
            if r.get("certainty") or r.get("pages"):
                c = self.L.claim(belief=BELIEF.get(r.get("certainty"), "true"),
                                 kind="inferred" if r.get("certainty") else "recorded",
                                 passage=self.claim_passage(r))
            self.relation(f"relation {r['id']}", s, t, o, claim=c, remark=r.get("note"))

        acts = d.get("activities", [])
        for a in acts:
            ts = a.get("timespan", {})
            b = int(ts["begin"]) if ts.get("begin") else None
            e = int(ts["end"]) if ts.get("end") else None
            places = a.get("took_place_at", [])
            self.entity("activity", a, a["class"].split("_")[0], type=a.get("type"), begin=b, end=e,
                        scale="CE" if (b or e) else None, place=self.id(places[0]) if places else None,
                        approx=1 if ts.get("approx") else 0)
        for a in acts:
            aid = self.id(a["id"])
            if a.get("part_of"):
                self.attempt(f"activity part_of {a['id']}", self.con.execute,
                             "UPDATE activity SET part_of = ? WHERE id = ?", (self.id(a["part_of"]), aid))
            for c in a.get("carried_out_by", []):
                self.attempt(f"participation {c['actor']} in {a['id']}", self.L.insert, "participation",
                             activity=aid, actor=self.id(c["actor"]), role=c.get("role"))
            for p in a.get("took_place_at", [])[1:] + a.get("also_at", []):
                self.relation(f"also_at {a['id']}", aid, "also_at" if self.is_a(self.id(p), "E53") else "worked_on",
                              self.id(p))
            if a.get("at_feature"):
                self.relation(f"at_feature {a['id']}", aid, "worked_on", self.id(a["at_feature"]))
            for x in a.get("continued", []):
                self.relation(f"continued {a['id']}", aid, "continued", self.id(x))
            if a.get("investigated"):
                self.relation(f"investigated {a['id']}", aid, "investigated", self.id(a["investigated"]))
            for x in a.get("removed", []):
                self.relation(f"removed {a['id']}", aid, "removed", self.id(x))
            for x in a.get("used", []):
                self.relation(f"used {a['id']}", aid, "used", self.id(x))
            for x in a.get("produced", []):
                self.relation(f"produced {a['id']}", aid, "formed", self.id(x))
            if a.get("purpose_of"):
                self.relation(f"purpose {a['id']}", aid, "had_purpose", self.id(a["purpose_of"]))
            for s in a.get("sources", []):
                src = self.id(s["ref"])
                self.about(f"cited for {a['id']}", self.passage(src, s["pages"]) if s.get("pages") else src, aid)
            self.identifier(a, aid, "project_number")
            self.dimensions(a, aid)
        self.about("report is about the campaign", self.report, self.id(doc["documents"]))

        for f in d.get("finds", []):
            fid = self.entity("thing", f, f["class"].split("_")[0], type=f.get("type"), material=f.get("material"))
        for f in d.get("finds", []):
            fid = self.id(f["id"])
            if f.get("part_of"):
                self.attempt(f"find part_of {f['id']}", self.con.execute,
                             "UPDATE thing SET part_of = ? WHERE id = ?", (self.id(f["part_of"]), fid))
            for where in dict.fromkeys(filter(None, [f.get("from_stratum"), f.get("at_feature")])):
                self.attempt(f"find context of {f['id']}", self.L.insert, "find_context", thing=fid,
                             found_in=self.id(where), found_by=self.id(f["found_by"]) if f.get("found_by") else None)
            if f.get("condition"):
                self.assertion(f"condition of {f['id']}", fid, "condition", object_code=f["condition"])
            if f.get("depicts"):
                self.assertion(f"depiction on {f['id']}", fid, "depicts_motif", object_code=f["depicts"])
            if f.get("inscribed"):
                self.attempt(f"inscribed {f['id']}", self.L.insert, "attribute_value", entity=fid,
                             attribute="inscribed", value_number=1)
            for t in f.get("taxa", []):
                self.assertion(f"taxon of {f['id']}", fid, "taxon", object_code=t,
                               claim=self.claim(f.get("identified_by")) if f.get("identified_by") else None)
            for c in f.get("comparanda", []):
                def one(c=c):
                    other = self.L.entity("thing", "E22", label=c["label"], type="assemblage")
                    cl = self.L.claim(kind="inferred", method="reasoning_method/typological_comparison",
                                      remark=c.get("refs"))
                    self.L.insert("assertion", subject=fid, property="similar_to", object_entity=other, claim=cl)
                self.attempt(f"comparandum of {f['id']}", one)
            self.dimensions(f, fid)
            self.dating(f, fid)

        for s in d.get("samples", []):
            def one(s=s):
                taking = self.L.entity("activity", "S2", label=f"Örnek alma: {s['label']}", type="sampling",
                                       part_of=self.id(s["taken_during"]) if s.get("taken_during") else None)
                self.L.entity("thing", "S13", label=s["label"], eid=self.id(s["id"]), source_id=s["id"],
                              type=s.get("material_type"))
                self.L.insert("sample", id=self.id(s["id"]), taken_by=taking,
                              taken_from=self.id(s["taken_from"]) if s.get("taken_from") else None)
            self.attempt(f"sample {s['id']}", one)
            for t in s.get("taxa", []):
                self.assertion(f"taxon of {s['id']}", self.id(s["id"]), "taxon", object_code=t)

        for a in d.get("analyses", []):
            def one(a=a):
                low = a["type"].lower()
                method = "radiocarbon" if "radiocarbon" in low else a["type"]
                self.L.entity("activity", "S4", label=a["label"], eid=self.id(a["id"]), source_id=a["id"],
                              remark=a.get("note"), type="dating" if "dating" in low else "analysis")
                self.L.insert("analysis", id=self.id(a["id"]), method=method)
            self.attempt(f"analysis {a['id']}", one)
            for s in a.get("samples", []):
                self.relation(f"sample of {a['id']}", self.id(a["id"]), "observed", self.id(s))
            if a.get("result") and a.get("dates"):
                def res(a=a):
                    target = self.id(a["dates"])
                    c = self.L.claim(kind="inferred", method="reasoning_method/laboratory_measurement")
                    self.L.insert("claim_basis", claim=c, basis_entity=self.id(a["id"]))
                    self.L.insert("dating", subject=target, event="use" if self.is_a(target, "E24") else self.event_for(target),
                                  begin=int(a["result"]["begin"]), end=int(a["result"]["end"]), scale="CE", claim=c)
                self.attempt(f"result of {a['id']}", res)

        for i in d.get("interpretations", []):
            def one(i=i):
                c = self.L.claim(kind="inferred", made_by=self.group(i["by"]) if i.get("by") else None,
                                 remark=i.get("basis"), passage=self.claim_passage(i))
                self.L.insert("assertion", subject=self.id(i["about"]), property="interpreted_as",
                              object_text=i["assigned"], claim=c)
            self.attempt(f"interpretation {i['id']}", one)

        for p in d.get("plans", []):
            def one(p=p):
                pid = self.L.entity("source", "E29", label=p["label"], eid=self.id(p["id"]), source_id=p["id"],
                                    remark=p.get("note"), type="plan of work")
                if p.get("planned_for"):
                    self.L.insert("attribute_value", entity=pid, attribute="planned_for",
                                  value_number=int(p["planned_for"]))
                for x in p.get("about", []) + ([p["place"]] if p.get("place") else []):
                    self.about(f"plan {p['id']} concerns {x}", pid, self.id(x))
            self.attempt(f"plan {p['id']}", one)

        for r in d.get("records", []):
            def one(r=r):
                self.L.entity("media", "E73" if "model" in r["type"].lower() else "E36", label=r["label"],
                              eid=self.id(r["id"]), source_id=r["id"], type=r["type"], scale=r.get("scale"),
                              made_by=self.id(r["made_by"]) if r.get("made_by") else None)
                for x in r.get("depicts", []):
                    self.about(f"record {r['id']} shows {x}", self.id(r["id"]), self.id(x))
            self.attempt(f"record {r['id']}", one)

        for f in d.get("figures", []):
            fid = f.get("id") or f"resim-{f['number']}"
            for x in f.get("depicts", []):
                self.about(f"figure {fid} shows {x}", self.id(fid), self.id(x))
        for kind in ("actors", "places", "periods", "features", "strata", "activities", "finds", "samples",
                     "analyses", "interpretations", "plans", "references", "records", "relations"):
            for e in d.get(kind, []):
                if kind in ("interpretations", "relations"):
                    continue
                self.pages(e)
                if kind != "records":
                    self.figures(e)
                else:
                    for f in e.get("figures", []):
                        self.about(f"figure {f} of {e['id']}", self.fig(f), self.id(e["id"]))


def main():
    db, files = sys.argv[1], sys.argv[2:]
    con = connect(db)
    for f in files:
        name = Path(f).stem.replace("_", "-")
        con.execute("BEGIN")
        con.execute("PRAGMA defer_foreign_keys = ON")
        c = Converter(con, json.load(open(f, encoding="utf-8")), name)
        c.run()
        con.commit()
        own = con.execute("SELECT count(*) FROM code WHERE owner = ?", (name,)).fetchone()[0]
        print(f"\n{name}: {c.tried} statements tried, {len(c.refused)} refused, "
              f"{sum(c.lost.values())} without a place, {own} own codes made")
        kinds = Counter(r.split(":", 1)[1].strip()[:90] for r in c.refused)
        for k, n in kinds.most_common():
            print(f"   refused {n:3}  {k}")
        for r in c.refused[:400]:
            print(f"      {r[:170]}")
        for k, n in c.lost.most_common():
            print(f"   no place {n:3}  {k}")


if __name__ == "__main__":
    main()
