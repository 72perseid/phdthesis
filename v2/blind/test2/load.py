#!/usr/bin/env python3
"""Blind test 2. Loads reader A's statements into an unchanged copy of the database, by ../RULES.md.

Every statement is tried for real (rule R15). The plan below says where each statement is tried.
The outcome is not written in the plan. It follows from what the database accepts and from the rules:
    own code made            -> C at best
    own attribute, raw property -> D at best
    remark                   -> E
    a named loss (rule 4.3)  -> B at best
    nothing                  -> F
"""
import csv
import json
import re
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DBDIR = HERE.parent.parent / "db"
sys.path.insert(0, str(DBDIR))
import fieldwork_db as fw  # noqa: E402

DB = HERE / "hacimusalar.sqlite"
DS = "hacimusalar-2024"
subprocess.run([sys.executable, str(DBDIR / "fieldwork_db.py"), "init", str(DB)], check=True, capture_output=True)
con = fw.connect(DB)
con.execute("INSERT INTO dataset (id,title,fieldwork,season,access,method) VALUES (?,?,?,?,?,?)",
            (DS, "Hacımusalar Höyük Kazısı 2024 Yılı Çalışmaları", "Hacımusalar Höyük", "2024", "open",
             "Blind test 2. Statements listed by reader A. Loaded by the rules in RULES.md."))
L = fw.Loader(con, DS)
S = {x["n"]: x for x in json.load(open(HERE / "readerA" / "statements.json", encoding="utf-8"))}
ORDER = "ABCDEF"
OUT = {}
ents = {}

# Rule R19. The loader names a kind of thing. The class comes from this table.
CLASS = {"site": ("thing", "E27"), "built": ("thing", "E25"), "layer": ("thing", "A2"), "cut": ("thing", "A3"),
         "find": ("thing", "E22"), "bone": ("thing", "E20"), "sample": ("thing", "S13"), "person": ("actor", "E21"),
         "group": ("actor", "E74"), "place": ("place", "E53"), "period": ("period", "E4"), "season": ("activity", "A9"),
         "dig": ("activity", "A1"), "sampling": ("activity", "S2"), "analysis": ("activity", "S4"),
         "conserve": ("activity", "E11"), "work": ("activity", "E7"), "doc": ("source", "E31"),
         "image": ("media", "E36"), "plan": ("source", "E29")}


class Try:
    """One statement. Collects the worst outcome of its parts."""

    def __init__(self, n):
        self.x, self.level, self.where, self.notes = S[n], "A", [], []

    def worse(self, level, note=None):
        if ORDER.index(level) > ORDER.index(self.level):
            self.level = level
        if note and note not in self.notes:
            self.notes.append(note)

    def done(self):
        x = self.x
        if x["hedge"] and self.level in "ABCD" and not any("claim" in w or "approx" in w for w in self.where):
            self.worse("B", f"The hedge '{x['hedge']}' is lost.")
        if x["negative"] and self.level in "ABCD" and not any("belief false" in w for w in self.where):
            self.worse("B", "The denial is only in the text.")
        OUT[x["n"]] = (self.level, "; ".join(self.where), " ".join(self.notes))


def attempt(fn, *a, **k):
    con.execute("SAVEPOINT s")
    try:
        r = fn(*a, **k)
        con.execute("RELEASE s")
        return r, None
    except (sqlite3.IntegrityError, fw.Refused) as e:
        con.execute("ROLLBACK TO s")
        con.execute("RELEASE s")
        return None, str(e)


def ent(name, kind, **cols):
    key = (name.strip().lower(), CLASS[kind][0])
    if key not in ents:
        table, cls = CLASS[kind]
        ents[key] = L.entity(table, cls, label=name.strip(), **cols)
    return ents[key]


def unit_of(eid):
    """Rule R20. A built feature that stands in a stratigraphic relation is also a stratigraphic unit."""
    r = con.execute("SELECT class, class2 FROM entity WHERE id = ?", (eid,)).fetchone()
    a8 = con.execute("SELECT 1 FROM ontology_subclass WHERE sub = ? AND super = 'A8'", (r["class"],)).fetchone()
    if not a8 and r["class2"] is None and r["class"] == "E25":
        con.execute("UPDATE entity SET class2 = 'A8' WHERE id = ?", (eid,))
    if not con.execute("SELECT 1 FROM context WHERE id = ?", (eid,)).fetchone():
        attempt(L.insert, "context", id=eid)
    return eid


def code(t, lst, text):
    c = L.code(lst, text)
    if con.execute("SELECT owner FROM code WHERE id = ?", (c,)).fetchone()["owner"] is not None:
        t.worse("C", f"own code in the list {lst}")
    return c


def nums(text):
    return [float(v.replace(",", ".")) for v in re.findall(r"\d+[.,]\d+|\d+", text)]


def claim(t, kind="recorded", **k):
    x = t.x
    belief = "false" if x["negative"] and not x["hedge"] else "probable" if x["hedge"] else "true"
    if x["negative"] and x["hedge"]:
        t.worse("B", "A statement that is both denied and hedged. The belief can hold one of the two.")
    t.where.append(f"claim, belief {belief}")
    return L.claim(belief=belief, kind="inferred" if x["hedge"] else kind, **k)


# ───────────── actions. Each writes to the database and records where ─────────────

def none(t, why):
    t.where.append("")
    t.worse("F", why)


def text(t, e, why="Free text. No structure fits."):
    old = con.execute("SELECT remark FROM entity WHERE id = ?", (e,)).fetchone()["remark"]
    new = f"{t.x['subject']} {t.x['says']}: {t.x['value']}"
    con.execute("UPDATE entity SET remark = ? WHERE id = ?", ((old + " | " if old else "") + new, e))
    t.where.append("entity.remark")
    t.worse("E", why)


def column(t, table, e, col, value, lst=None):
    v = code(t, lst, value) if lst else value
    _, err = attempt(con.execute, f"UPDATE {table} SET {col} = ? WHERE id = ?", (v, e))
    t.where.append(f"{table}.{col}")
    if err:
        t.worse("F", f"Refused: {err}")
    return err


def relation(t, s, typ, o, with_claim=False):
    row = con.execute("SELECT conclusion FROM relation_type WHERE code = ?", (typ,)).fetchone()
    if row["conclusion"]:
        _, err = attempt(L.insert, "assertion", subject=s, property=typ, object_entity=o, claim=claim(t))
        t.where.append(f"assertion {typ}")
    else:
        c = claim(t) if (with_claim or t.x["hedge"] or t.x["negative"]) else None
        _, err = attempt(L.insert, "relation", subject=s, type=typ, object=o, claim=c)
        t.where.append(f"relation {typ}")
    if err:
        t.worse("F", f"Refused: {err}")
    return err


def raw(t, s, prop, o):
    _, err = attempt(L.insert, "relation", subject=s, property=prop, object=o)
    t.where.append(f"relation with the raw property {prop}")
    t.worse("F" if err else "D", f"Refused: {err}" if err else "No declared relation. A property was taken from the ontology.")


def stated(t, e, prop, **value):
    """A conclusion with a term, an entity or text as its value."""
    lst = con.execute("SELECT code_list FROM relation_type WHERE code = ?", (prop,)).fetchone()["code_list"]
    if "object_code" in value:
        value["object_code"] = code(t, lst, value["object_code"])
    _, err = attempt(L.insert, "assertion", subject=e, property=prop, claim=claim(t), **value)
    t.where.append(f"assertion {prop}")
    if err:
        t.worse("F", f"Refused: {err}")


def says_text(t, e):
    stated(t, e, "interpreted_as", object_text=f"{t.x['says']}: {t.x['value']}")


def own(t, e, name, value=None):
    v = t.x["value"] if value is None else value
    aid = f"{DS}/{name}"
    try:
        num, typ = fw.number(v), "decimal"
    except ValueError:
        num, typ = v, "text"
    row = con.execute("SELECT value_type FROM attribute_def WHERE id = ?", (aid,)).fetchone()
    if row is None:
        con.execute("INSERT INTO attribute_def (id,label_en,label_tr,applies_to,value_type,owner) VALUES (?,?,?,?,?,?)",
                    (aid, name, name, "E1", typ, DS))
    elif row["value_type"] == "text":
        num, typ = str(v), "text"
    elif typ == "text":
        t.worse("F", "An own attribute that held numbers cannot take text.")
        return
    c = claim(t) if (t.x["hedge"] or t.x["negative"]) else None
    _, err = attempt(L.insert, "attribute_value", entity=e, attribute=aid, claim=c,
                     value_number=num if typ != "text" else None, value_text=num if typ == "text" else None)
    t.where.append(f"own attribute '{name}'")
    t.worse("F" if err else "D", f"Refused: {err}" if err else "No column, relation or declared attribute for it.")


def declared(t, e, attribute, number=None, text_value=None):
    _, err = attempt(L.insert, "attribute_value", entity=e, attribute=attribute, value_number=number,
                     value_text=text_value, claim=claim(t) if t.x["hedge"] else None)
    t.where.append(f"declared attribute {attribute}")
    if err:
        t.worse("F", f"Refused: {err}")
    return err


def measure(t, e, kind, value=None, lo=None, hi=None, unit="m", fallback=None):
    """A measurement. If the database refuses it, an own attribute is tried (rule R16)."""
    k = code(t, "dimension_kind", kind)
    u = code(t, "unit", unit)
    approx = 1 if re.search(r"yaklaşık|neredeyse|y\.", t.x["hedge"]) else 0
    _, err = attempt(L.insert, "dimension", entity=e, kind=k, value=value, value_min=lo, value_max=hi, unit=u,
                     approx=approx)
    if err:
        t.level = "A"
        t.notes = [n for n in t.notes if not n.startswith("own code")]
        own(t, e, fallback or kind)
        t.notes.append(f"First tried as a measurement. Refused: {err}")
    else:
        t.where.append("dimension" + (", approx" if approx else ""))
        if t.x["hedge"] and not approx:
            t.worse("B", f"The hedge '{t.x['hedge']}' is lost.")


def sizes(t, e, fallback="boyut"):
    """'a x b' without names (rule R6). The kinds of measurement are names, so own kinds are needed."""
    for i, v in enumerate(nums(t.x["value"])):
        measure(t, e, f"boyut {i + 1}", value=v, unit="cm" if "cm" in t.x["value"] else "m", fallback=fallback)


def dated(t, e, event, period=None, begin=None, end=None):
    c = claim(t)
    p = None
    if period:
        p = ent(period, "period")
        if re.search(r"/|-| ile | arasında", period):
            t.worse("B", "Several periods in one name. Stored as one period.")
    _, err = attempt(L.insert, "dating", subject=e, event=event, period=p, begin=begin, end=end,
                     scale="CE" if begin is not None else None, claim=c)
    t.where.append(f"dating, event {event}")
    if err:
        t.worse("F", f"Refused: {err}")


def found(t, thing, where=None, by=None, method=None):
    m = code(t, "collection_method", method) if method else None
    _, err = attempt(L.insert, "find_context", thing=thing, found_in=where, found_by=by, method=m)
    t.where.append("find_context")
    if err:
        t.worse("F", f"Refused: {err}")


def shown(t, target, tag=None):
    tag = tag or t.x["value"]
    m = re.match(r"(Resim|Tablo|Çizim)\W*(\d+)", tag.strip())
    f = ent(f"{m.group(1)} {m.group(2)}", "image")
    if not con.execute("SELECT 1 FROM about WHERE item = ? AND target = ?", (f, target)).fetchone():
        _, err = attempt(L.insert, "about", item=f, target=target)
        if err:
            t.worse("F", f"Refused: {err}")
    t.where.append("about")


def takes_part(t, work, actor, role=None):
    r = code(t, "role", role) if role else None
    _, err = attempt(L.insert, "participation", activity=work, actor=actor, role=r)
    t.where.append("participation")
    if err:
        t.worse("F", f"Refused: {err}")


def year(t, work, col, y, day_lost=True):
    _, err = attempt(con.execute, f"UPDATE activity SET {col} = ?, scale = 'CE' WHERE id = ?", (y, work))
    t.where.append(f"activity.{col}")
    if err:
        t.worse("F", f"Refused: {err}")
    if day_lost:
        t.worse("B", "Years are whole numbers. Day and month are lost.")


def lost(t, what):
    t.worse("B", what)


def named_only(t):
    t.worse("B", "An entity that holds only a name, with no kind from a list.")


# ───────────── fixed points ─────────────
con.execute("BEGIN")
con.execute("PRAGMA defer_foreign_keys = ON")
paper = ent("Hacımusalar Höyük Kazısı 2024 Yılı Çalışmaları", "doc", type="excavation_report")
site = ent("Hacımusalar Höyük", "site")
project = ent("Hacımusalar Höyük arkeolojik araştırmaları", "season", type="excavation")
season = ent("Hacımusalar Höyük 2024 sezonu", "season", type="season", part_of=project)
north = ent("Kuzey Yamaç alanı", "place")
south = ent("Güney Yamaç", "place")
top = ent("Höyüğün üst düzlüğü", "place")
church = ent("Merkezi Kilise", "built")
monastery = ent("Manastır yapısı", "built")
dig_n = ent("Kuzey Yamaç kazısı 2024", "dig", type="excavation_unit", part_of=season, place=north)
dig_c = ent("Merkezi Kilise 1. Etap kazısı", "dig", type="excavation_unit", part_of=season)
dig_old = ent("Kuzey Yamaç kazıları 1994'ten beri", "dig", type="excavation_unit", part_of=project)
gpr = ent("Yer radarı çalışmaları", "work", part_of=project)
ert = ent("ERT çalışması", "work", part_of=season)
dual = ent("Çift yöntemli jeofizik", "work", part_of=season)
grid = ent("Karelaj çalışması 1993", "work")
digit = ent("Karelajın dijitalleştirilmesi", "work", type="documentation", part_of=season)
sond_s = ent("Güney Yamaç sondajları", "dig")
sond = ent("C4a6 sondajı", "dig", part_of=dig_n)
paleo = ent("Paleo-coğrafya çalışmaları", "plan")
outreach = ent("Kamu yararına etkinlikler", "work")
symposium = ent("Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "work")
talk = ent("Konuşma", "work", part_of=symposium)
wall_ia = ent("Demir Çağı sur duvarı", "built")
eba = ent("ETÇ yapı kalıntıları (C4a8)", "built")
debris = ent("Kerpiç üst yapı enkazı (C4a7)", "layer")
fill_thick = ent("Kalın dolgu (Kuzey Yamaç)", "layer")
culture = ent("Kültür dolgusu", "layer")


def trench(name):
    return ent(name, "place", type="trench")


def dig_of(name):
    return ent(f"{name} kazısı 2024", "dig", type="excavation_unit", part_of=dig_c if name.startswith("E") else dig_n,
               place=trench(name))


def person(name):
    return ent(" ".join(w.capitalize() if w.isupper() else w for w in name.split()), "person")


PLAN = {}


def plan(ns, fn, *a, **k):
    for n in ([ns] if isinstance(ns, int) else ns):
        assert n not in PLAN, n
        PLAN[n] = (fn, a, k)


R = lambda a, b: range(a, b + 1)
E_ = lambda name, kind, **c: (lambda: ent(name, kind, **c))          # entity made when the statement is tried
V = lambda t: t.x["value"]

# ── document structure: no place
plan([1, 6, 34, 35, 46, 66, 159, 173, 397, 409, 410, 411, 412, 413, 414, 457, 463, 496, 516], none,
     "Structure of the printed document. The database has no place for it.")

# ── the paper, the site, permits
plan(2, lambda t: t.where.append("entity.label"))
plan(3, lambda t: relation(t, paper, "authored_by", person(V(t))))
plan(4, lambda t: (column(t, "place", ent("Elmalı", "place", type="district"), "part_of", ent("Antalya", "place", type="province")),
                   t.notes.append("Stored as: Elmalı lies in Antalya.")))
plan(5, lambda t: column(t, "thing", site, "location", ent("Elmalı", "place", type="district")))
plan([7, 8], lambda t: takes_part(t, project, ent(V(t), "group"), "adına yürütülen kurum"))
plan(9, lambda t: (relation(t, project, "motivated_by", ent("Cumhurbaşkanlığı Kararnamesi", "doc")),
                   lost(t, "'Permitted by' is stored as 'was motivated by'.")))
plan(10, lambda t: (column(t, "source", ent("Cumhurbaşkanlığı Kararnamesi", "doc"), "year", 2022),
                    lost(t, "Years are whole numbers. Day and month are lost.")))
plan(11, lambda t: attempt(L.insert, "identifier", entity=ent("Cumhurbaşkanlığı Kararnamesi", "doc"),
                           type="identifier_type/permit_number", value=V(t)) and t.where.append("identifier"))
plan(12, lambda t: relation(t, project, "investigated", site))

# ── people
plan(13, lambda t: takes_part(t, project, person("Bülent Arıkan"), V(t)))
for n, who in ((16, "Selda Baybo"), (19, "Ergin Tatar"), (21, "Fatih Mehmet Çongur"), (23, "Onur Kaya"), (25, "Selma Akgül")):
    plan(n, lambda t, who=who: takes_part(t, season, person(who), V(t)))
plan([17, 60], lambda t: own(t, person(t.x["subject"]), "unvan"))
plan([26, 38], lambda t: own(t, person(t.x["subject"]), "görev"))
plan([18, 20, 22, 24], lambda t: column(t, "actor", person(t.x["subject"]), "member_of", ent(V(t), "group")))
plan(63, lambda t: column(t, "actor", person("Bülent Arıkan"), "member_of", ent("Evrim ve Ekosistem ABD", "group")))
plan(62, lambda t: column(t, "actor", ent("Evrim ve Ekosistem ABD", "group"), "member_of", ent("Avrasya Yer Bilimleri Enstitüsü", "group")))
plan(61, lambda t: column(t, "actor", ent("Avrasya Yer Bilimleri Enstitüsü", "group"), "member_of", ent("İstanbul Teknik Üniversitesi", "group")))
plan(64, lambda t: own(t, person("Bülent Arıkan"), "adres"))
plan(65, lambda t: attempt(L.insert, "identifier", entity=person("Bülent Arıkan"), type="identifier_type/orcid",
                           value=V(t)) and t.where.append("identifier"))
plan([27, 28, 29, 30, 31, 162, 164, 169, 170, 171], lambda t: measure(
    t, ent(t.x["subject"], "group"), "count", value={"beş": 5, "iki": 2, "bir": 1, "altı": 6}.get(V(t)) or nums(V(t))[0],
    unit="piece", fallback="kişi sayısı"))
plan([32, 33], lambda t: takes_part(t, season, ent("uzmanlar", "group"), V(t)))
plan([50, 51], lambda t: takes_part(t, gpr, ent(V(t), "group")))
plan(163, lambda t: takes_part(t, dig_n, ent("öğrenciler", "group")))
plan(37, lambda t: takes_part(t, grid, person(V(t))))

# ── the season and other work: years, places, methods
plan(14, lambda t: (year(t, season, "begin", 2024), year(t, season, "end", 2024)))
plan(15, lambda t: measure(t, season, "duration", value=3, unit="ay"))
plan(36, lambda t: year(t, grid, "begin", 1993, day_lost=False))
plan(47, lambda t: year(t, project, "begin", 2022, day_lost=False))
plan(49, lambda t: year(t, gpr, "begin", 2022, day_lost=False))
plan([81, 187], lambda t: year(t, dig_old, "begin", 1994, day_lost=False))
plan(190, lambda t: year(t, ent("C4a7-C4b7 kazısı", "dig"), "begin", 2023, day_lost=False))
plan(215, lambda t: year(t, ent("Kerpiç dolgunun kazısı", "dig"), "begin", 2023, day_lost=False))
plan(216, lambda t: relation(t, dig_of("C4a7"), "continued", ent("Kerpiç dolgunun kazısı", "dig")))
plan(161, lambda t: (year(t, dig_n, "begin", 2024), year(t, dig_n, "end", 2024)))
plan(172, lambda t: (year(t, dig_c, "begin", 2024), year(t, dig_c, "end", 2024)))
plan(478, lambda t: year(t, dig_c, "end", 2024))
plan(509, lambda t: year(t, symposium, "begin", 2024))
plan(48, lambda t: column(t, "activity", gpr, "place", top))
plan(126, lambda t: column(t, "activity", sond_s, "place", south))
plan(160, lambda t: t.where.append("activity.place"))
plan(223, lambda t: column(t, "activity", sond, "place", trench("C4a6")))
plan([52, 53, 67, 77, 149], lambda t: (relation(t, gpr if t.x["n"] != 149 else dual, "also_at", ent(V(t), "place")), named_only(t)))
plan(71, lambda t: relation(t, gpr, "worked_on", monastery))
plan(83, lambda t: column(t, "activity", ert, "type", V(t), lst="activity_type"))
plan(146, lambda t: column(t, "activity", dual, "type", V(t), lst="activity_type"))
plan(401, lambda t: column(t, "activity", dig_c, "type", V(t), lst="activity_type"))
plan(400, lambda t: (con.execute("UPDATE entity SET label = ? WHERE id = ?", (V(t), dig_c)), t.where.append("entity.label")))
plan(148, lambda t: raw(t, ert, "P183", dual))
plan(292, lambda t: raw(t, dig_of("C5b2"), "P175", dig_of("C5b1")))
plan(98, lambda t: measure(t, ert, "depth", value=40))
plan(93, lambda t: measure(t, ert, "elektrot aralığı", value=1))
plan(167, lambda t: measure(t, dig_c, "removed_volume", value=120, unit="m3"))
plan(460, lambda t: measure(t, dig_c, "removed_volume", value=120.78, unit="m3"))
plan(217, lambda t: measure(t, dig_of("C4a7"), "depth", value=1.3))
plan(352, lambda t: measure(t, dig_of("C4b10"), "depth", value=0.40))
plan(376, lambda t: measure(t, dig_of("C4c10"), "depth", value=0.20))
plan([344, 368], lambda t: measure(t, dig_of("C4b10" if t.x["n"] == 344 else "C4c10"), "duration",
                                   value=8 if t.x["n"] == 344 else 2, unit="gün"))
plan([225, 226], lambda t: measure(t, sond, "length" if "length" in t.x["says"] else "width", value=nums(V(t))[0]))
plan(341, lambda t: measure(t, dig_of("C5b1"), "Locus sayısı", value=5, unit="piece"))
plan([283, 349], lambda t: own(t, dig_of("C5b1" if t.x["n"] == 283 else "C4b10"), "başlangıç Locus"))
plan(89, lambda t: measure(t, ent("ERT profilleri", "place"), "count", value=10, unit="piece", fallback="hat sayısı"))
plan(92, lambda t: measure(t, ent("ERT profilleri", "place"), "length", lo=10, hi=240, fallback="hat uzunluğu"))
plan(520, lambda t: measure(t, ent("birinci ERT profili", "place"), "length", value=240, fallback="hat uzunluğu"))
plan(188, lambda t: relation(t, dig_old, "removed", unit_of(ent("ETÇ seviyeleri", "layer"))))
plan(180, lambda t: (relation(t, ent("C4a8 kazısı (önceki sezonlar)", "dig"), "removed", unit_of(wall_ia)),
                     lost(t, "'Along a line of five metres' is lost. A relation cannot carry a measurement.")))
plan([198, 199], lambda t: relation(t, dig_of("C4a7"), "removed", unit_of(ent(V(t) + " (C4a7-C4b7)", "built"))))
plan(304, lambda t: relation(t, dig_of("C5b1"), "removed", unit_of(ent("duvarlar (C5b1 ve C5b2)", "built"))))
plan(370, lambda t: (relation(t, dig_of("C4c10"), "removed", unit_of(ent("Demir Devri duvarlar (C4c10)", "built"))),
                     lost(t, "'Was started' is lost.")))
plan(133, lambda t: (relation(t, ent("Güney Yamaç açması 2023", "dig"), "worked_on", ent("duvarlar (Güney Yamaç)", "built")),
                     lost(t, "'A further part of the wall' is lost.")))
plan([471, 472], lambda t: (relation(t, dig_c, "worked_on", ent(t.x["subject"], "built")),
                            lost(t, "'Was exposed' is stored as 'was worked on'.")))
plan([303, 373, 374], lambda t: (relation(t, ent("Belgeleme: " + V(t), "work", type="documentation"), "worked_on",
                                          ent(t.x["subject"], "built")), lost(t, "The way of recording is only in a name.")))
plan(527, lambda t: [relation(t, dig_n, "also_at", trench(v.strip())) for v in V(t).split(",")])
plan([532, 562], lambda t: relation(t, ent("Fotoğraf çekimi: " + t.x["subject"], "work", type="documentation"), "used",
                                    ent("İHA", "find", type="tool")))
plan(512, lambda t: t.where.append("activity.part_of"))
plan(513, lambda t: (con.execute("UPDATE entity SET label = ? WHERE id = ?", (V(t), talk)), t.where.append("entity.label")))
plan([510, 511], lambda t: takes_part(t, symposium, ent(V(t), "group"), "düzenleyen"))
plan(398, lambda t: takes_part(t, dig_c, ent("Geleceğe Miras Projesi", "group"), "funder"))
plan(399, lambda t: column(t, "actor", ent("Geleceğe Miras Projesi", "group"), "member_of", ent(V(t), "group")))
plan(378, lambda t: declared(t, ent("Kuzey Yamaç kazılarının devamı", "plan"), "planned_for", number=2025))
plan(118, lambda t: (attempt(L.insert, "about", item=paleo, target=ent("Elmalı Ovası", "place")), t.where.append("about")))

# ── places, points, elevations
plan(174, lambda t: column(t, "place", ent("P2 noktası", "place"), "part_of", north))
plan([197, 342], lambda t: column(t, "place", trench(re.split(r"[ -]", t.x["subject"])[0]), "part_of", north))
plan([97, 175, 281], lambda t: measure(t, ent(t.x["subject"], "place"), "elevation", value=nums(V(t))[0], fallback="kot"))
plan([340, 353, 354], lambda t: measure(t, trench(t.x["subject"].split()[0]), "depth" if "depth" in t.x["says"] or "level" in t.x["says"]
                                        else "elevation", value=nums(V(t))[0], fallback="kot veya derinlik"))
plan([152, 166], lambda t: measure(t, ent(t.x["subject"], "place"), "area", value=nums(V(t))[0], unit="m2", fallback="alan"))
plan([388, 403], lambda t: sizes(t, ent(t.x["subject"], "place")))
plan([207, 209], lambda t: sizes(t, trench(t.x["subject"].split()[0])))
plan(402, lambda t: measure(t, ent("Merkezi Kilise açmaları", "place"), "count", value=7, unit="piece", fallback="açma sayısı"))
plan(547, lambda t: (column(t, "place", ent("Merkezi Kilise açmaları", "place"), "part_of", ent(V(t), "place")), named_only(t)))

# ── Table 1: one trench per row
for i, name in enumerate(["E4d9", "E4d10", "E5d1", "E5c3", "E5c4", "E5c5", "E5b6"]):
    b = 415 + 6 * i
    plan(b, lambda t, name=name: (trench(name), t.where.append("place, kind trench")))
    plan(b + 1, lambda t, name=name: year(t, dig_of(name), "begin", 2024))
    plan(b + 3, lambda t, name=name: year(t, dig_of(name), "end", 2024))
    plan(b + 2, lambda t, name=name: measure(t, dig_of(name), "açılış kotu", value=nums(V(t))[0]))
    plan(b + 4, lambda t, name=name: measure(t, dig_of(name), "kapanış kotu", value=nums(V(t))[0]))
    plan(b + 5, lambda t, name=name: measure(t, dig_of(name), "removed_volume", value=nums(V(t))[0], unit="m3"))
plan(458, lambda t: t.worse("B", "The same day as in statement 172. Years are whole numbers.") or t.where.append("activity.begin"))
plan(459, lambda t: t.worse("B", "The same day as in statement 478. Years are whole numbers.") or t.where.append("activity.end"))

# ── built things and layers
B_ = lambda t: ent(t.x["subject"], "built")
LY = lambda t: ent(t.x["subject"], "layer")
plan([176, 324, 551, 552, 555, 560], lambda t: column(t, "thing", B_(t), "location", trench(re.search(r"[A-E]\d[a-d]\d+", V(t)).group(0))))
plan(465, lambda t: (column(t, "thing", B_(t), "location", ent(V(t), "place")), named_only(t)))
plan([129, 177], lambda t: column(t, "thing", B_(t), "material", V(t), lst="material"))
plan(298, lambda t: column(t, "thing", B_(t), "material", V(t), lst="material"))
plan(178, lambda t: (column(t, "thing", ent("Sur duvarı temeli", "built", part_of=wall_ia), "material", V(t), lst="material"),
                     column(t, "thing", ent("Sur duvarı temeli", "built"), "type", "temel", lst="thing_type")))
plan([202, 211, 284, 297, 380, 473], lambda t: column(t, "thing", B_(t) if t.x["n"] not in (211, 380) else LY(t), "type", V(t), lst="thing_type"))
plan([203, 212, 289, 375, 464], lambda t: stated(t, B_(t) if t.x["n"] in (203, 289, 464) else LY(t), "condition", object_code=V(t)))
plan([182, 377, 557], lambda t: relation(t, unit_of(ent(V(t), "built")), "overlies", unit_of(B_(t)))
     if t.x["says"] == "lies below" else relation(t, unit_of(B_(t)), "overlies", unit_of(ent(V(t), "built"))))
plan(102, lambda t: relation(t, ent(V(t), "layer"), "overlies", LY(t)))
plan(249, lambda t: relation(t, unit_of(ent("çöp çukurları (C4a7)", "built")), "cuts", debris))
plan(251, lambda t: relation(t, debris, "earlier_than", unit_of(ent("çöp çukurları (C4a7)", "built"))))
plan(329, lambda t: relation(t, unit_of(B_(t)), "abuts", unit_of(ent("çöp çukuru (C5b2, oval)", "built"))))
plan(393, lambda t: relation(t, unit_of(ent("çöp çukurları (Kuzey Yamaç)", "built")), "cuts", fill_thick, with_claim=True))
plan([390, 391, 392], lambda t: relation(t, fill_thick, "contains_remains_of", ent(V(t), "find", type="assemblage")))
plan(470, lambda t: column(t, "thing", B_(t), "part_of", monastery))
plan(477, lambda t: (column(t, "thing", ent("apsis yapısı", "built"), "part_of", church), named_only(t)))
plan(559, lambda t: (column(t, "thing", B_(t), "part_of", ent(V(t), "built")), named_only(t)))
plan([255, 313, 338], lambda t: (relation(t, unit_of(ent(V(t) + f" ({t.x['n']})", "layer")), "fills", unit_of(B_(t))),
                                 column(t, "thing", ent(V(t) + f" ({t.x['n']})", "layer"), "type", V(t), lst="thing_type")))
plan([265, 268, 310], lambda t: (column(t, "thing", ent(f"taban ({t.x['n']})", "built", part_of=B_(t), type="floor"),
                                        "material", V(t), lst="material")))
plan([467, 468, 553], lambda t: stated(t, B_(t), "material_is", object_code=V(t)))
plan([107, 144], lambda t: stated(t, ent(t.x["subject"], "layer" if t.x["n"] == 107 else "built"), "material_is", object_code=V(t)))
plan(54, lambda t: stated(t, church, "function", object_code=V(t)))
plan([130, 132, 285, 326, 347, 535, 539], lambda t: own(t, B_(t), "biçim" if "shape" in t.x["says"] else "işçilik"))
plan([106, 125], lambda t: own(t, LY(t), "elektrik direnci"))
plan([99, 250, 308, 293], lambda t: measure(t, B_(t) if t.x["n"] != 99 else LY(t), "count", unit="piece",
                                            value={"üç": 3, "iki": 2}.get(V(t)) or {"toplam yedi": 7}.get(V(t))))
# measurements of built things and layers
plan([57, 58], lambda t: (measure(t, B_(t), "depth", value=1 if t.x["n"] == 57 else 1.5),
                          lost(t, "'Top lies at' and 'extends to' are not told apart.")))
plan([103, 155], lambda t: (measure(t, LY(t) if t.x["n"] == 103 else B_(t), "depth", value=nums(V(t))[0]),
                            lost(t, "'Begins at' is lost.")))
plan([100, 105], lambda t: measure(t, LY(t), "depth", value=nums(V(t))[0]))
plan([82, 381], lambda t: measure(t, culture if t.x["n"] == 82 else LY(t), "thickness", value=12 if t.x["n"] == 82 else None,
                                  lo=4 if t.x["n"] == 381 else None, hi=5 if t.x["n"] == 381 else None))
plan([143, 206], lambda t: measure(t, B_(t), "length", value=nums(V(t))[0]))
plan(137, lambda t: (measure(t, B_(t), "length", value=20), lost(t, "'Further to the north' is lost.")))
plan([219, 254], lambda t: measure(t, wall_ia if t.x["n"] == 219 else B_(t), "width" if t.x["n"] == 219 else "diameter",
                                   lo=3 if t.x["n"] == 219 else 1))
plan([286, 327], lambda t: measure(t, B_(t), "diameter" if t.x["n"] == 286 else "depth", value=nums(V(t))[0]))
plan(269, lambda t: measure(t, ent("çöp çukurları (C4a7)", "built"), "depth", hi=1))
plan(270, lambda t: measure(t, ent("çöp çukurları (C4a7)", "built"), "depth", lo=0.10))
plan(184, lambda t: measure(t, eba, "elevation", value=1049))
plan(185, lambda t: sizes(t, ent(t.x["subject"], "place")))
plan([204, 205, 299], lambda t: measure(t, B_(t), "width" if "width" in t.x["says"] else "height",
                                        value=2 if "iki" in V(t) else 1, unit="sıra"))

# ── dates
plan([179, 183, 301, 371], lambda t: dated(t, ent(t.x["subject"], "built"), "making", period=V(t)))
plan([131, 135], lambda t: dated(t, B_(t), "making", period=V(t)))
plan(248, lambda t: dated(t, debris, "formation", period=V(t)))
plan(R(382, 386), lambda t: dated(t, ent("Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "layer"), "formation", period=V(t)))
plan([69, 70], lambda t: (dated(t, church, "use", period=V(t)), lost(t, "'From' and 'until' are lost. Both periods are stored alike.")))
plan(114, lambda t: (dated(t, site, "existence", period=V(t)), lost(t, "'First settled' is stored as 'existed in'.")))
plan(115, lambda t: (con.execute("UPDATE period SET start_earliest = -3500, scale = 'CE', approx = 1 WHERE id = ?",
                                 (ent("Geç Kalkolitik Dönem", "period"),)),
                     t.where.append("period.start_earliest, period.approx")))
plan(136, lambda t: (con.execute("UPDATE claim SET method = ? WHERE id = (SELECT claim FROM dating WHERE subject = ?)",
                                 (code(t, "reasoning_method", V(t)), ent("savunma sistemi", "built"))), t.where.append("claim.method")))

# ── interpretations kept as text with a claim
plan([76, 101, 109, 110, 111, 112, 113, 116, 142, 157, 195, 213, 220, 221, 306, 394, 396, 523, 524], lambda t: says_text(
    t, ent(t.x["subject"], "layer" if "katman" in t.x["subject"].lower() or "dolgu" in t.x["subject"].lower() else "built")))
plan([253, 273, 320], lambda t: relation(t, ent(t.x["subject"], "built" if t.x["n"] == 253 else "find"), "similar_to",
                                         ent(V(t), "find", type="assemblage")))
plan(307, lambda t: (attempt(L.insert, "claim_basis", claim=con.execute(
    "SELECT claim FROM assertion ORDER BY rowid DESC LIMIT 1").fetchone()[0], basis_entity=ent("C4c10 açmasının kesiti", "cut")),
    t.where.append("claim_basis")))

# ── finds
F_ = lambda t: ent(t.x["subject"], "bone" if re.search(r"kemi|kafatası|boynuz", t.x["subject"]) else "find")
KINDS = [230, 238, 244, 256, 261, 263, 271, 294, 311, 312, 315, 316, 317, 318, 321, 333, 335, 356, 362, 480, 484, 487, 490, 492]
plan(KINDS, lambda t: column(t, "thing", F_(t), "type", V(t), lst="thing_type"))
plan([231, 245, 363], lambda t: measure(t, F_(t), "count", value=1, unit="piece"))
plan([485, 489, 491, 493], lambda t: column(t, "thing", F_(t), "material", V(t), lst="material"))
plan([234, 258, 275, 486], lambda t: stated(t, F_(t), "condition", object_code=V(t)))
plan(239, lambda t: stated(t, ent("öküze ait kafatası", "bone"), "taxon", object_code=V(t)))
plan(488, lambda t: stated(t, F_(t), "identified_as", object_code=V(t)))
plan([236, 240, 247], lambda t: found(t, F_(t), by=sond))
plan([260, 262, 264], lambda t: found(t, F_(t), where=ent("küllü ve kireçli dolgu (255)", "layer")))
plan(272, lambda t: found(t, F_(t), where=debris))
plan(296, lambda t: [found(t, F_(t), where=trench(n)) for n in ("C5b1", "C5b2")])
plan(319, lambda t: [found(t, ent(n, "find"), where=trench("C5b1")) for n in (
    "at figürinleri (C5b1 ve C5b2)", "heykelcikler (C5b1 ve C5b2)", "ağırşaklar (C5b1 ve C5b2)", "diğer küçük buluntular (C5b1 ve C5b2)")])
plan(323, lambda t: (found(t, F_(t), where=ent("kazılan dolgu (C5b1 ve C5b2)", "layer")), named_only(t)))
plan(337, lambda t: [found(t, ent(n, k), where=ent("çöp çukuru (C5b2, oval)", "built")) for n, k in (
    ("kemik parçaları (C5b2 çöp çukurları)", "bone"), ("seramik parçaları (C5b2 çöp çukurları)", "find"))])
plan(360, lambda t: found(t, F_(t), where=trench("C4b10")))
plan(365, lambda t: found(t, F_(t), where=trench("C4b10"), method="yüzeyde"))
plan([481, 495], lambda t: found(t, F_(t), by=dig_c))
plan(366, lambda t: declared(t, F_(t), "museum_grade", number=1))
plan(494, lambda t: own(t, F_(t), "sınıf"))
plan([259, 357, 358, 359], lambda t: dated(t, F_(t), "making", period=V(t)))
plan([295, 322], lambda t: dated(t, F_(t), "making", period=V(t)))
plan(235, lambda t: measure(t, F_(t), "depth", value=1))
plan([232, 530], lambda t: sizes(t, ent("kerpiç blok", "find")))
plan([233, 243], lambda t: own(t, F_(t), "buluntu durumu"))
plan([274, 276], lambda t: own(t, F_(t), "korunan kısım" if t.x["n"] == 274 else "işçilik"))
plan(277, lambda t: own(t, F_(t), "yüzey işlemi"))
plan(482, lambda t: (column(t, "thing", F_(t), "location", ent(V(t), "place")), lost(t, "'Either ... or' is lost.")))
plan(483, lambda t: (raw(t, F_(t), "P53", ent(V(t), "place")), lost(t, "'Either ... or' is lost.")))

# ── figures
CAPTIONS = [517, 518, 519, 525, 529, 531, 542, 545, 550, 554, 558, 561, 461]
plan(CAPTIONS, lambda t: (ent(t.x["subject"], "image"), con.execute(
    "UPDATE entity SET remark = NULL, label = ? WHERE id = ?", (t.x["subject"] + ": " + V(t), ent(t.x["subject"], "image"))),
    t.where.append("entity.label of the media item")))
FIG = {59: ("Manastır'a ait binaların kalıntıları", "built"), 75: ("Resim 1’de görülen yapılar", "built"), 91: ("ERT profilleri", "place"),
       96: None, 123: ("birinci ERT profili", "place"), 196: None, 237: ("kerpiç blok", "find"), 252: ("çöp çukurları (C4a7)", "built"),
       288: ("çöp çukuru (C5b1)", "built"), 328: ("çöp çukuru (C5b2, oval)", "built"), 355: None, 404: None, 405: None,
       469: ("ikincil malzeme (spolia)", "find"), 474: ("yol", "built"), 479: None, 521: ("birinci ERT profili", "place"), 528: None}
for n, target in FIG.items():
    plan(n, lambda t, target=target: shown(
        t, ent(*target) if target else {96: ert, 196: north, 355: trench("C4b10"), 404: dig_c, 405: dig_c, 479: dig_c, 528: north}[t.x["n"]],
        tag=t.x["subject"] if t.x["n"] == 528 else None))

# ── everything else is free text on the entity it is about
TEXT_ON = {
    "project": [39, 40, 41, 42, 43, 44, 45, 72, 497, 498, 499, 500, 501, 502, 503],
    "gpr": [68, 78, 79, 80], "ert": [84, 85, 86, 87, 88, 90, 94, 95, 124, 522], "dual": [147, 150, 151, 153, 154],
    "paleo": [117, 119, 120], "sond_s": [127], "site": [104, 121, 122, 138, 139, 140, 141],
    "dig_n": [165, 186, 189, 191, 192, 193, 194, 200, 201, 208, 210, 278, 279, 280, 282, 290, 291, 305, 343, 345,
              348, 350, 351, 367, 369, 372, 378 + 1, 387, 526, 544],
    "dig_c": [168, 406, 407, 408, 462, 466, 548, 549],
    "sond": [224, 227, 228, 229], "outreach": [504, 505, 506, 507, 508], "talk": [514, 515],
    "debris": [214, 218, 222], "fill_thick": [389, 395], "eba": [181], "culture": [108],
}
for key, ns in TEXT_ON.items():
    plan(ns, lambda t, key=key: text(t, globals()[key]))
SUBJECT_TEXT = [55, 56, 73, 74, 128, 134, 145, 156, 158, 241, 242, 246, 257, 266, 267, 287, 300, 302, 309, 314, 325, 330, 331,
                332, 334, 336, 339, 346, 361, 364, 475, 476, 533, 534, 536, 537, 538, 540, 541, 543, 546, 556, 563]
plan(SUBJECT_TEXT, lambda t: text(t, ent(t.x["subject"], "find" if S[t.x["n"]]["group"] == "FIND" else "built")))

missing = sorted(set(S) - set(PLAN))
assert not missing, f"no plan for {missing}"
assert not set(PLAN) - set(S)

for n in sorted(S):
    t = Try(n)
    fn, a, k = PLAN[n]
    a = [v() if callable(v) and getattr(v, "__name__", "") == "<lambda>" and v.__code__.co_argcount == 0 else v for v in a]
    try:
        fn(t, *a, **k)
    except (sqlite3.IntegrityError, fw.Refused) as e:
        t.worse("F", f"Refused: {e}")
    t.done()
con.commit()

CORE = {"DOC", "PEOPLE", "WORK", "PLACE", "BUILT", "FIND", "MEASURE", "DATE", "INTERP", "LAB", "FIGURE"}
with open(HERE / "outcome.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["n", "page", "group", "core", "subject", "says", "value", "hedge", "negative", "outcome", "where", "note"])
    for n in sorted(S):
        x = S[n]
        w.writerow([n, x["page"], x["group"], "yes" if x["group"] in CORE else "no", x["subject"], x["says"], x["value"],
                    x["hedge"], "yes" if x["negative"] else "", *OUT[n]])

NAMES = {"A": "typed, complete", "B": "typed, part lost", "C": "own term", "D": "own structure", "E": "text only", "F": "not stored"}


def table(title, ns):
    c = Counter(OUT[n][0] for n in ns)
    print(f"\n{title}: {len(ns)} statements")
    for k in ORDER:
        print(f"   {k} {NAMES[k]:17} {c[k]:4}  {100 * c[k] / max(len(ns), 1):5.1f} %")


table("all statements", list(S))
table("core scope", [n for n in S if S[n]["group"] in CORE])
print("\nper group      n     A     B     C     D     E     F")
for g in sorted({x["group"] for x in S.values()}, key=lambda g: -sum(x["group"] == g for x in S.values())):
    ns = [n for n in S if S[n]["group"] == g]
    c = Counter(OUT[n][0] for n in ns)
    print(f"   {g:8} {len(ns):4}  " + "  ".join(f"{c[k]:4}" for k in ORDER) + ("" if g in CORE else "   outside the core"))
h = [n for n in S if S[n]["hedge"]]
d = [n for n in S if S[n]["negative"]]
print(f"\nhedges {len(h)}: kept {sum('is lost' not in OUT[n][2] and OUT[n][0] in 'ABCD' for n in h)}, "
      f"lost {sum('is lost' in OUT[n][2] for n in h)}, text only or not stored {sum(OUT[n][0] in 'EF' for n in h)}")
print(f"denials {len(d)}: kept as a claim {sum('belief false' in OUT[n][1] for n in d)}, "
      f"text only or not stored {sum(OUT[n][0] in 'EF' for n in d)}")
print("\nown codes by list")
for r in con.execute("SELECT list, count(*) AS k FROM code WHERE owner IS NOT NULL GROUP BY list ORDER BY k DESC"):
    print(f"   {r['k']:4}  {r['list']}")
print("\nrefusals by the database")
for note, k in Counter(re.search(r"Refused: [^.]*", OUT[n][2]).group(0) for n in S if "Refused" in OUT[n][2]).most_common():
    print(f"   {k:4}  {note}")
