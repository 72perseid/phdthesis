#!/usr/bin/env python3
"""Blind test 3. Loads reader A's statements into an unchanged copy of the database, by ../RULES.md.

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

DB = HERE / "hisardere.sqlite"
DS = "hisardere-2024"
subprocess.run([sys.executable, str(DBDIR / "fieldwork_db.py"), "init", str(DB)], check=True, capture_output=True)
con = fw.connect(DB)
con.execute("INSERT INTO dataset (id,title,fieldwork,season,access,method) VALUES (?,?,?,?,?,?)",
            (DS, "İznik Hisardere Nekropolü 2024 Yılı Kazı Çalışmaları", "İznik Hisardere Nekropolü", "2024", "open",
             "Blind test 3. Statements listed by reader A. Loaded by the rules in RULES.md."))
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
paper = ent("İznik Hisardere Nekropolü 2024 Yılı Kazı Çalışmaları", "doc", type="excavation_report")
site = ent("İznik Hisardere Nekropolü", "site")
season = ent("İznik Hisardere Nekropolü 2024 yılı kazı çalışmaları", "season", type="season")
gmp = ent("Geleceğe Miras Projesi", "work")
basilica = ent("Bazilika", "built")
WORKS = {
    "aug": ent("01.08.2024-30.08.2024 çalışmaları", "dig", part_of=season),
    "oct": ent("03.10.2024-29.11.2024 çalışmaları", "dig", part_of=season),
    "scan": ent("Yeraltı görüntüleme sistemi taraması", "work"),
    "arch": ent("Mimari belgeleme çalışmaları", "work", part_of=season),
    "pottery": ent("Seramik ve küçük buluntu değerlendirme çalışmaları", "work", part_of=season),
    "conserve": ent("Restorasyon ve konservasyon çalışmaları", "conserve", part_of=season),
    "anthro": ent("Antropoloji çalışmaları", "analysis", part_of=season),
    "loot": ent("Kaçak kazılar", "work", type="looting"),
}
TRENCH = re.compile(r"^([A-L](?:-[A-L])?[-/ ]?\d{2}(?:-\d{2})?)\b")
COMPOUND = re.compile(r"^[A-L]-[A-L]|\d-\d|Kesit")


def words(v):
    return len(v.split())


def is_term(v):
    """The rules do not say what a term is. The loader takes up to four words as a term, more as a sentence."""
    return words(v) <= 4


def trench(name):
    return ent(name.replace(" açması", "").replace(" plankaresi", "").replace(" Plankaresi", "").strip(), "place", type="square")


def dig_of(name):
    return ent(f"{name} kazı çalışmaları", "dig", part_of=season, place=trench(name))


def person(name):
    return ent(" ".join(w.capitalize() if w.isupper() else w for w in name.split()), "person")


def subject(t):
    """The entity that the statement is about, with the class that rule R19 gives."""
    x, s = t.x, t.x["subject"]
    low = s.lower()
    if re.search(r"iskelet|kemik|diş|vertebra", low):
        return ent(s, "bone")
    if x["group"] == "FIND" or (x["group"] in ("DATE", "LAB") and re.search(r"seramik|tabak|kandil|kap|amphora|kase|testi|küpe|sikke|obje|eser", low)):
        return ent(s, "find")
    if re.search(r"tabakası|toprak|harcı", low):
        return unit_of(ent(s, "layer"))
    m = TRENCH.match(s)
    if m and re.search(r"açması|plankaresi$", low):
        return trench(s)
    return ent(s, "built")


def place_of(t, v):
    """Where something was found or lies: a square, or a built thing, or a layer."""
    if TRENCH.match(v):
        if COMPOUND.search(v):
            t.worse("B", "A compound of squares is stored as one place.")
        return trench(v)
    for key, e in list(ents.items()):
        if key[1] == "thing" and (key[0] == v.lower() or key[0].startswith(v.lower().replace(" mezar içi", ""))):
            return e
    low = v.lower()
    if re.search(r"toprağı|tabakası", low):
        return unit_of(ent(v, "layer"))
    return ent(v, "built")


PLAN = {}
NUMBER = {"bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8}


def number_in(v):
    w = v.lower().replace("toplam ", "").split()
    if w and w[0] in NUMBER:
        return NUMBER[w[0]]
    n = nums(v.replace(".", "") if re.fullmatch(r"\d\.\d{3}.*", v.strip()) else v)
    return n[0] if n else None


def metric(t, e, kind, fallback=None):
    v = t.x["value"]
    unit = "cm" if "cm" in v else "m"
    n = nums(v)
    if not n:
        return text(t, e, "A size given in words.")
    measure(t, e, kind, value=n[0], unit=unit, fallback=fallback)
    if t.x["hedge"] and not re.search(r"yaklaşık", t.x["hedge"]):
        t.worse("B", f"The hedge '{t.x['hedge']}' is lost. A measurement has no claim.")
        t.where.append("approx")


def decide(t):
    x = t.x
    g, says, v, s = x["group"], x["says"], x["value"], x["subject"]
    # ── outside the data
    if g == "STRUCT":
        return none(t, "Structure of the printed document. The database has no place for it.")
    if g == "DESCR":
        return text(t, site, "A judgement or a general description.")
    if g == "DOC":
        if says == "has title":
            return t.where.append("entity.label")
        if says == "has author":
            return relation(t, paper, "authored_by", person(v))
        return text(t, paper)
    if g == "FIGURE":
        if says == "caption reads":
            f = ent(s, "image")
            con.execute("UPDATE entity SET label = ? WHERE id = ?", (f"{s}: {v}", f))
            return t.where.append("entity.label of the media item")
        return shown(t, subject(t))
    # ── people and administration
    if says == "role in the work":
        work = next((WORKS[k] for k, w in (("arch", "mimari"), ("pottery", "seramik"), ("conserve", "konservasyon"),
                                          ("anthro", "antropoloji")) if w in v.lower()), None)
        if work:
            return takes_part(t, work, person(s))
        if g == "ADMIN" or not is_term(v):
            return text(t, season, "A role described in a sentence.")
        return takes_part(t, season, person(s), v)
    if says == "title":
        return own(t, person(s), "unvan")
    if says == "address of affiliation":
        return own(t, person(s), "adres")
    if says == "affiliation":
        column(t, "actor", person(s), "member_of", ent(v, "group"))
        if "," in v:
            t.worse("B", "University, faculty and department are one name.")
        return
    if says.startswith("identifier"):
        attempt(L.insert, "identifier", entity=person(s), type="identifier_type/orcid", value=v)
        return t.where.append("identifier")
    if says == "count in the team":
        return measure(t, season, f"{s} sayısı", value=number_in(v), unit="piece")
    if says in ("was permitted by", "was carried out under the presidency of"):
        return takes_part(t, season, ent(v, "group"), "izin veren" if "permitted" in says else "başkanlık")
    if says == "was financially supported by":
        return takes_part(t, season, ent(v, "group"), "funder")
    if says == "was funded by":
        takes_part(t, WORKS["aug" if s.startswith("01") else "oct"], ent("Kültür ve Turizm Bakanlığı", "group"), "funder")
        return lost(t, "'From the allowance' is lost.")
    if says == "was part of project":
        work = WORKS["oct"] if s.startswith("03") else dig_of(s.split()[0]) if TRENCH.match(s) else dig_of("E-15")
        return column(t, "activity", work, "part_of", gmp)
    if says == "was carried out by":
        return takes_part(t, season, ent("Kazı ekibi", "group"))
    # ── the work
    if says == "took place between":
        work = season if s.startswith("İznik") else WORKS["aug" if s.startswith("01") else "oct"]
        year(t, work, "begin", 2024)
        return year(t, work, "end", 2024)
    if says == "took place in" and "2020" in v:
        year(t, WORKS["scan"], "begin", 2020)
        return lost(t, "The month is lost. Years are whole numbers.")
    if says == "took place in square":
        relation(t, WORKS["aug" if s.startswith("01") else "oct"], "also_at", trench(v))
        if COMPOUND.search(v):
            lost(t, "A compound of squares is stored as one place.")
        return
    if says == "had work area":
        ent(v, "work", part_of=season)
        t.where.append("activity.part_of")
        return named_only(t)
    if says == "number of work areas":
        return measure(t, season, "çalışma alanı sayısı", value=5, unit="piece")
    if says == "was scanned with":
        relation(t, WORKS["scan"], "used", ent(v, "find", type="tool"))
        return t.where.append("relation worked_on") or relation(t, WORKS["scan"], "worked_on", site)
    if says == "was documented with":
        if not is_term(v):
            return text(t, site)
        m = L.entity("media", "E36", label=v, type=code(t, "media_type", v))
        attempt(L.insert, "about", item=m, target=site)
        return t.where.append("media.type, about")
    if g == "WORK" and says == "is made of":
        return column(t, "thing", ent(s, "built"), "material", v, lst="material")
    if g == "WORK" and says == "is supported by":
        column(t, "thing", ent(v, "built"), "part_of", ent(s, "built"))
        return named_only(t)
    if says in ("trench limits measure", "work started at elevation"):
        if "x" in v:
            return sizes(t, trench(s))
        return measure(t, trench(s), "elevation", value=nums(v)[0], fallback="açılış kotu")
    # ── history: looting
    if g == "HISTORY":
        if "kaçak" in v:
            relation(t, WORKS["loot"], "worked_on", subject(t))
            if says != "was looted by":
                lost(t, f"'{says}' is stored as 'was worked on'.")
            return
        if says == "was used earlier for":
            return stated(t, site, "function", object_code=v)
        return text(t, site)
    # ── elevations, measurements, counts
    if says in ("elevation",):
        return metric(t, subject(t), "elevation")
    if g == "MEASURE":
        e = subject(t)
        m = re.match(r"measures \((length|width|height|depth|diameter|thickness)\)", says)
        if m:
            return metric(t, e, m.group(1))
        if says == "measures (inner length)":
            metric(t, e, "length")
            return lost(t, "'Inner' is lost.")
        if says == "measures (measurable total length)":
            metric(t, e, "length")
            return lost(t, "'Measurable' is lost.")
        if says == "measures" and "x" in v:
            return sizes(t, e)
        if says == "measures" or "between" in says:
            return own(t, e, "aradaki mesafe", value=v)
        return metric(t, e, re.sub(r"measures \(|\)", "", says).replace("[unclear]", "").strip()[:30])
    if says.startswith("count") or says == "consist of" or "number of" in says:
        e = subject(t)
        n = number_in(v)
        if n is None:
            return text(t, e, "A count given in words.")
        if says in ("count", "consist of"):
            unit = "çift" if "çift" in v else "piece"
            measure(t, e, "count", value=2 if unit == "çift" and False else n, unit=unit)
            if says == "count" and g == "FIND" and "envanterlik" in s:
                declared(t, e, "museum_grade", number=1)
            return
        if says == "count received for conservation":
            measure(t, e, "count", value=n, unit="çift" if "çift" in v else "piece")
            relation(t, WORKS["conserve"], "modified", e)
            return lost(t, "Count and conservation are stored apart. That this count was handed over is lost.")
        kind = {"count of individuals": "birey sayısı", "count (bags)": "count"}.get(says, says[:30])
        return measure(t, e, kind, value=n, unit="poşet" if "bags" in says else "piece")
    # ── dates
    if g == "DATE":
        e = subject(t)
        event = "making" if con.execute("SELECT class FROM entity WHERE id = ?", (e,)).fetchone()[0] in ("E22", "E25") else "existence"
        if says == "is dated to period" or says == "is dated to":
            y = re.search(r"MS (\d)\.-(\d)\. yy", v)
            if y:                                   # a span of centuries is one span of years
                return dated(t, e, event, begin=(int(y.group(1)) - 1) * 100 + 1, end=int(y.group(2)) * 100)
            return dated(t, e, event, period=v)
        if says.startswith("share"):
            period = re.search(r"(Roma|Helenistik|Bizans) D\w+", says).group(0)
            part = ent(f"{s}: {period}", "find", part_of=e)
            dated(t, part, "making", period=period)
            return measure(t, part, "oran", value=nums(v)[0], unit="percent")
        if says.startswith("general density"):
            dated(t, e, "making", period=v)
            return lost(t, "'In general' is lost. The whole group is dated to the period.")
        return text(t, e)
    # ── interpretations
    if g == "INTERP":
        return says_text(t, subject(t))
    # ── finds
    if g == "FIND":
        e = subject(t)
        if says == "kind":
            return column(t, "thing", e, "type", v, lst="thing_type")
        if says == "is made of":
            return column(t, "thing", e, "material", v, lst="material")
        if says.startswith("was found in"):
            if x["negative"]:
                return text(t, place_of(t, re.sub(r"^.*\((.*?)\)$", r"\1", s)),
                            "Something that was not found. It does not exist, so it cannot be an entity (rule R25).")
            return found(t, e, where=place_of(t, v))
        if says in ("position in place", "size") or says == "condition":
            if not is_term(v):
                return text(t, e, "Described in a sentence.")
            if says == "condition":
                return stated(t, e, "condition", object_code=v)
            return own(t, e, "buluntu durumu")
        return text(t, e)
    # ── laboratory and conservation
    if g == "LAB":
        e = subject(t) if re.search(r"iskelet|kemik|diş|testi|eser|sikke", s.lower()) else None
        if says in ("tool used",):
            return relation(t, WORKS["conserve"], "used", ent(v, "find", type="tool"))
        if says in ("substance used", "substance applied"):
            sub = ent(re.sub(r"%\d+ oranında ", "", v), "find")
            relation(t, WORKS["conserve"], "used", sub)
            return measure(t, sub, "derişim", value=nums(v)[0], unit="percent")
        if says in ("disease observed", "observed") and e is not None and is_term(v):
            return stated(t, e, "condition", object_code=v)
        if says == "sex is":
            return own(t, e, "cinsiyet")
        if says == "was examined by":
            return relation(t, WORKS["anthro"], "observed", e)
        if says == "was examined for":
            return column(t, "analysis", analysis_row(), "method", v, lst="analysis_method")
        if says == "criterion used" and is_term(v):
            c = L.claim(kind="inferred", method=code(t, "reasoning_method", v), remark=s)
            return t.where.append("claim.method")
        return text(t, e or WORKS["conserve" if "konservasyon" in s or "temizli" in s or "eser" in s else "anthro"],
                    "A step, an aim or a method described in a sentence.")
    # ── places
    if g == "PLACE":
        return text(t, subject(t), "A position described in words.")
    # ── built things
    if g == "BUILT":
        e = subject(t)
        if says in ("kind", "type"):
            if not is_term(v):
                return text(t, e, "The kind is described in a sentence. The term cannot be taken apart (rule R18).")
            return column(t, "thing", e, "type", v, lst="thing_type")
        if says in ("condition", "has character"):
            return stated(t, e, "condition", object_code=v) if is_term(v) else text(t, e, "Described in a sentence.")
        if says in ("orientation", "colour", "workmanship", "masonry", "form", "is built as"):
            if not is_term(v):
                return text(t, e, "Described in a sentence.")
            return own(t, e, {"orientation": "doğrultu", "colour": "renk", "workmanship": "işçilik", "masonry": "örgü",
                              "form": "biçim", "is built as": "örgü"}[says])
        if says in ("is made of",):
            return column(t, "thing", e, "material", v, lst="material")
        if says in ("bear", "bears") and is_term(v):
            return stated(t, e, "depicts_motif", object_code=v)
        if says in ("is part of",):
            column(t, "thing", e, "part_of", ent(v.capitalize(), "built"))
            return named_only(t) if not con.execute("SELECT type FROM thing WHERE id = ?", (e,)).fetchone()[0] else None
        if says == "has part" or says in ("is coated with", "is paved with", "is covered with", "is filled with") and is_term(v):
            part = ent(f"{v} ({s})", "built", part_of=e)
            return column(t, "thing", part, "type", re.sub(r"^(iki adet|bir) ", "", v), lst="thing_type")
        if says == "lies below":
            return relation(t, unit_of(ent(v, "built")), "overlies", unit_of(e))
        if says == "was built over":
            return relation(t, e, "lies_in", site)
        if says in ("lies in", "is located in") and re.search(r"lunette|duvarı|kesiti$", v):
            column(t, "thing", e, "part_of", ent(v, "built"))
            return named_only(t)
        return text(t, e, "A position, a relation or a state described in words.")
    if g == "ADMIN":
        return text(t, season)
    return text(t, season if g == "WORK" else site, "A step, an aim, a reason or a decision described in a sentence.")


def analysis_row():
    a = WORKS["anthro"]
    if not con.execute("SELECT 1 FROM analysis WHERE id = ?", (a,)).fetchone():
        L.insert("analysis", id=a)
    return a


for n in S:
    PLAN[n] = (decide, (), {})

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
    w.writerow(["n", "page", "group", "form", "core", "subject", "says", "value", "hedge", "negative", "outcome", "where", "note"])
    for n in sorted(S):
        x = S[n]
        w.writerow([n, x["page"], x["group"], x["form"], "yes" if x["group"] in CORE else "no", x["subject"], x["says"], x["value"],
                    x["hedge"], "yes" if x["negative"] else "", *OUT[n]])

NAMES = {"A": "typed, complete", "B": "typed, part lost", "C": "own term", "D": "own structure", "E": "text only", "F": "not stored"}


def table(title, ns):
    c = Counter(OUT[n][0] for n in ns)
    print(f"\n{title}: {len(ns)} statements")
    for k in ORDER:
        print(f"   {k} {NAMES[k]:17} {c[k]:4}  {100 * c[k] / max(len(ns), 1):5.1f} %")


table("all statements", list(S))
table("core scope", [n for n in S if S[n]["group"] in CORE])
for form in ("list", "prose"):
    table(f"core scope, {form}", [n for n in S if S[n]["group"] in CORE and S[n]["form"] == form])
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
