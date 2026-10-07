#!/usr/bin/env python3
"""Blind test. Loads the statements of one unseen paper into an unchanged copy of the database.

    load_blind.py

Input   statements.json   made by a reader that has never seen the tables. Frozen before loading.
Output  zerzevan.sqlite   a fresh copy built from the unchanged files in ../db
        outcome.csv       one line per statement: where it went, or why it did not go in

Every statement gets one outcome:
    1  typed      a column, a declared relation, a standard code
    2  template   a declared attribute
    3  own        it needed an own code, an own attribute or a raw property of the ontology
    4  text       only kept as free text in a remark
    X  not stored refused by the database, or no place at all

Nothing in ../db is changed by this script.
"""
import csv
import json
import re
import sqlite3
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "db"))
import fieldwork_db as fw  # noqa: E402

DB = HERE / "zerzevan.sqlite"
DS = "zerzevan-2024"
subprocess.run([sys.executable, str(HERE.parent.parent / "db" / "fieldwork_db.py"), "init", str(DB)],
               check=True, capture_output=True)
con = fw.connect(DB)
con.execute("INSERT INTO dataset (id,title,fieldwork,season,access,method) VALUES (?,?,?,?,?,?)",
            (DS, "Zerzevan Kalesi 2024 Yılı Çalışmaları", "Zerzevan Kalesi", "2024", "open",
             "Blind test. Statements listed by a reader without knowledge of the tables."))
L = fw.Loader(con, DS)
S = json.load(open(HERE / "statements.json", encoding="utf-8"))
OUT = {}                     # n -> (level, where, note)
ents = {}                    # name -> id
NUM = {"bir": 1, "birer": 1, "iki": 2, "üç": 3}


def out(x, level, where, note=""):
    if x["hedge"] and level in ("1", "2", "3") and "claim" not in where:
        note = (note + " The hedge '" + x["hedge"] + "' is lost.").strip()
    OUT[x["n"]] = (level, where, note)


def attempt(fn, *a, **k):
    """Returns (result, None) or (None, message of the database)."""
    con.execute("SAVEPOINT s")
    try:
        r = fn(*a, **k)
        con.execute("RELEASE s")
        return r, None
    except (sqlite3.IntegrityError, fw.Refused) as e:
        con.execute("ROLLBACK TO s")
        con.execute("RELEASE s")
        return None, str(e)


def E(name, table, cls, class2=None, **cols):
    key = name.strip().lower()
    if key not in ents:
        ents[key] = L.entity(table, cls, label=name.strip(), class2=class2, **cols)
    return ents[key]


def is_own(code_id):
    return con.execute("SELECT owner FROM code WHERE id = ?", (code_id,)).fetchone()["owner"] is not None


def coded(lst, text):
    c = L.code(lst, text)
    return c, is_own(c)


def remark(eid, text, table="entity"):
    old = con.execute(f"SELECT remark FROM {table} WHERE id = ?", (eid,)).fetchone()["remark"]
    con.execute(f"UPDATE {table} SET remark = ? WHERE id = ?", ((old + " | " if old else "") + text, eid))


def own_attr(eid, name, value):
    aid = f"{DS}/{name}"
    try:
        v, typ = fw.number(value), "decimal"
    except ValueError:
        v, typ = value, "text"
    row = con.execute("SELECT value_type FROM attribute_def WHERE id = ?", (aid,)).fetchone()
    if row is None:
        con.execute("INSERT INTO attribute_def (id,label_en,label_tr,applies_to,value_type,owner) VALUES (?,?,?,?,?,?)",
                    (aid, name, name, "E1", typ, DS))
    elif row["value_type"] == "text":
        v, typ = value, "text"
    L.insert("attribute_value", entity=eid, attribute=aid, value_number=v if typ != "text" else None,
             value_text=v if typ == "text" else None)


def metres(text):
    return [float(v.replace(",", ".")) for v in re.findall(r"\d+[.,]\d+|\d+", text)]


def dim(eid, kind, value=None, lo=None, hi=None, unit="m"):
    k, own_k = coded("dimension_kind", kind)
    u, own_u = coded("unit", unit)
    r, err = attempt(L.insert, "dimension", entity=eid, kind=k, value=value, value_min=lo, value_max=hi, unit=u)
    return err, own_k or own_u


def rel(s, typ, o, claim=None):
    return attempt(L.insert, "relation", subject=s, type=typ, object=o, claim=claim)[1]


def about(item, target):
    if not con.execute("SELECT 1 FROM about WHERE item = ? AND target = ?", (item, target)).fetchone():
        return attempt(L.insert, "about", item=item, target=target)[1]


def thing(name, cls="E22", class2=None, **cols):
    return E(name, "thing", cls, class2=class2, **cols)


def place(name, typ=None, part_of=None):
    return E(name, "place", "E53", type=typ, part_of=part_of)


def person(name):
    return E(re.sub(r"\s+", " ", name).title() if name.isupper() or name.split()[-1].isupper() else name, "actor", "E21")


def group(name):
    return E(name, "actor", "E74")


def activity(name, cls="E7", typ=None, **cols):
    return E(name, "activity", cls, type=typ, **cols)


def figure(tag):
    """'Resim: 8' or 'Çizim 1' gives the media item."""
    m = re.match(r"(Resim|Çizim)\W*(\d+)", tag.strip())
    name = f"{m.group(1)} {m.group(2)}"
    return E(name, "media", "E36", type="photograph" if m.group(1) == "Resim" else "drawing", shown_in=None)


def source_for(cite):
    """'Coşkun, 2019a, s. 568' gives the source of the bibliography and the passage."""
    m = re.search(r"(\d{4}[a-z]?)", cite)
    names = re.sub(r"\bvd\.?|\bve\b|,", " ", cite[: m.start()]).split()
    page = re.search(r"(?:s\.\s*)?(\d+(?:-\d+)?)\s*$", cite[m.end():])
    for key, (sid, text) in BIB.items():
        if f"({m.group(1)})" in text and all(n.lower() in text.lower() for n in names[:1]):
            first = text.lower().split("(")[0]
            several = "," in first.replace(names[0].lower() + ",", "", 1).strip(" .,a")
            if len(names) == 1 and several != ("vd" in cite):
                continue                                   # one author cited, several listed, or the reverse
            if len(names) > 1 and not all(n.lower() in first for n in names):
                continue
            if page:
                return L.entity("passage", "E31", label=f"s. {page.group(1)}", source=sid, locator=page.group(1))
            return sid
    return None


con.execute("BEGIN")
con.execute("PRAGMA defer_foreign_keys = ON")

# ───────────── fixed points of the paper ─────────────
volume = E("45. Kazı Sonuçları Toplantısı Bildirileri, Cilt 1", "source", "E31", type="proceedings")
report = E("Zerzevan Kalesi 2024 Yılı Çalışmaları", "source", "E31", type="excavation_report", language="tr")
site = thing("Zerzevan Kalesi", "E27", class2="E25", type="site")
ents["zerzevan askeri yerleşimi"] = site
season = activity("Zerzevan Kalesi arkeolojik kazı ve restorasyon çalışmaları", "A9", typ="season",
                  begin=2024, end=2024, scale="CE")
for alias in ("çalışmalar", "2024 sezonu çalışmaları", "2024 yılı çalışmaları", "2024 yılı kazı sezonu",
              "2024 yılı zerzevan kalesi kazı sezonu", "on birinci dönem kazı, belgeleme ve restorasyon çalışmaları",
              "zerzevan kalesi kazı, belgeleme ve restorasyon çalışmaları (2024)", "kazılar", "2024 yılı"):
    ents[alias] = season
rel(season, "investigated", site)
about(report, season)
mithras = thing("Mithras Kutsal Alanı", "E25", type="building")
for alias in ("mithras kutsal alanı (mithraeum)", "kutsal alan", "mithras kutsal alanı kazı alanı",
              "kutsal alan (roma’nın en erken mithraeumlarından biri)"):
    ents[alias] = mithras
dig = activity("Mithras Kutsal Alanı kazı çalışmaları", "A1", typ="excavation_unit", part_of=season)
clean = activity("alan temizliği ve yapı temizliği", "E7", typ="cleaning", part_of=season)
ents["çevre düzenleme çalışmaları"] = activity("Çevre düzenleme çalışmaları", "E7", typ="landscaping", part_of=season)
BIB = {}
for x in S:
    if x["says"] == "is listed in the bibliography":
        y = re.search(r"\((\d{4})", x["subject"])
        sid = L.entity("source", "E31", label=x["subject"][:80], citation=x["subject"], year=int(y.group(1)))
        BIB[x["n"]] = (sid, x["subject"])
        out(x, "1", "source.citation")

# ───────────── finds ─────────────
FIND_SAYS = {"is find of kind", "has find code", "was found during", "was found in grid square",
             "was found in position within grid square", "was found at location", "was found on",
             "was found at elevation", "was found between elevations", "number of pieces", "is made of",
             "is in condition", "is shown in figure", "measures (diameter)", "measures (depth)"}
by_subject = defaultdict(list)
for x in S:
    by_subject[x["subject"]].append(x)
find_subjects = [s for s, rows in by_subject.items() if any(r["says"] in ("is find of kind", "was found at elevation")
                                                            for r in rows)]
for s in find_subjects:
    rows = [r for r in by_subject[s] if r["says"] in FIND_SAYS]
    get = lambda says: [r for r in rows if r["says"] == says]
    kind = get("is find of kind")
    name = kind[0]["value"] if kind else s
    bone = "kemik" in name and "amulet" not in name
    fid = L.entity("thing", "E20" if bone else "E22", label=s)
    ents[s.lower()] = fid
    for r in kind:
        text = re.sub(r"\(\?\)", "", r["value"]).strip()
        if r["hedge"]:
            c, own = coded("thing_type", text)
            cl = L.claim(belief="possible")
            _, err = attempt(L.insert, "assertion", subject=fid, property="identified_as", object_code=c, claim=cl)
            out(r, "X" if err else "3" if own else "1", "assertion identified_as, with a claim", err or
                ("own code for the kind" if own else ""))
        else:
            c, own = coded("thing_type", text)
            con.execute("UPDATE thing SET type = ? WHERE id = ?", (c, fid))
            out(r, "3" if own else "1", "thing.type", "own code for the kind" if own else "")
    for r in get("has find code"):
        _, err = attempt(L.insert, "identifier", entity=fid, type="identifier_type/find_number", value=r["value"])
        out(r, "X" if err else "1", "identifier", err or "")
    for r in get("is made of"):
        c, own = coded("material", r["value"])
        con.execute("UPDATE thing SET material = ? WHERE id = ?", (c, fid))
        out(r, "3" if own else "1", "thing.material", "own code for the material" if own else "")
    sq = get("was found in grid square")
    pos = get("was found in position within grid square")
    by = get("was found during")
    on = get("was found on")
    where = None
    if sq:
        where = place(sq[0]["value"], "square")
        out(sq[0], "1", "find_context.found_in, place of kind square")
        if pos:
            where = place(f"{sq[0]['value']}, {pos[0]['value']}", None, part_of=where)
            out(pos[0], "1", "find_context.found_in, place inside the square",
                "Stored as a place with a name. The database has no kind of place for it.")
    method, own_m = (coded("collection_method", on[0]["value"]) if on and on[0]["value"] == "yüzeyde" else (None, False))
    fc, err = attempt(L.insert, "find_context", thing=fid, found_in=where,
                      found_by={"Mithras Kutsal Alanı kazı çalışmaları": dig}.get(by[0]["value"], clean) if by else season,
                      method=method)
    for r in by:
        out(r, "X" if err else "1", "find_context.found_by", err or "")
    for r in on:
        if r["value"] == "yüzeyde":
            out(r, "3" if own_m else "1", "find_context.method", "own code for 'yüzeyde'" if own_m else "")
        else:
            remark(fc, r["value"], "find_context")
            out(r, "4", "find_context.remark", "How the find lay has no place.")
    for r in get("was found at location"):
        remark(fc, r["value"], "find_context")
        out(r, "4", "find_context.remark", "A position relative to a building. Direction and building are not data.")
    for r in get("was found at elevation"):
        err, own = dim(fid, "elevation", value=metres(r["value"])[0])
        out(r, "X" if err else "1", "dimension, kind elevation", err or "")
    for r in get("was found between elevations"):
        v = metres(r["value"])
        err, own = dim(fid, "elevation", lo=min(v), hi=max(v))
        out(r, "X" if err else "1", "dimension, kind elevation, as a range", err or "")
    for r in get("number of pieces"):
        w = r["value"].split()[0]
        n = NUM.get(w) or int(w)
        err, own = dim(fid, "count", value=n, unit="piece")
        out(r, "X" if err else "1", "dimension, kind count", err or "")
    for r in get("is in condition"):
        c, own = coded("condition", r["value"])
        _, err = attempt(L.insert, "assertion", subject=fid, property="condition", object_code=c, claim=L.claim())
        out(r, "X" if err else "3" if own else "1", "assertion condition", err or ("own code" if own else ""))
    for r in get("is shown in figure"):
        err = about(figure(r["value"]), fid)
        out(r, "X" if err else "1", "about", err or "")
    for r in get("measures (diameter)") + get("measures (depth)"):
        err, own = dim(fid, "diameter" if "diameter" in r["says"] else "depth", value=metres(r["value"])[0])
        out(r, "X" if err else "1", "dimension", err or "")

# ───────────── everything else, statement by statement ─────────────
PEOPLE_ROLE = {}                       # person -> role statement, waiting for the participation
for x in S:
    if x["says"] == "has the role":
        PEOPLE_ROLE.setdefault(x["subject"].lower(), []).append(x)
TEAM = {"arkeolog", "sanat tarihçi", "restoratör", "mimar", "bakanlık yetkili uzmanı", "zerzevan kalesi kazı heyet üyesi"}


def two_sizes(x, eid):
    v = metres(x["value"])
    errs = [dim(eid, f"boyut {i + 1}", value=a)[0] for i, a in enumerate(v)]
    e = next((e for e in errs if e), None)
    out(x, "X" if e else "3", "dimension, own kinds", e or
        "The paper gives 'a x b' and does not say which is length and which is width.")


def text_claim(x, eid, belief=None):
    cl = L.claim(kind="inferred", belief=belief or ("probable" if x["hedge"] else "true"))
    _, err = attempt(L.insert, "assertion", subject=eid, property="interpreted_as",
                     object_text=f"{x['says']}: {x['value']}", claim=cl)
    out(x, "X" if err else "1", "assertion interpreted_as, text with a claim", err or "")
    return cl


last_claim = {}
for x in S:
    if x["n"] in OUT:
        continue
    n, s, says, v = x["n"], x["subject"], x["says"], x["value"]
    k = s.lower()

    # ── the document
    if says == "is part of volume":
        con.execute("UPDATE source SET part_of = ? WHERE id = ?", (volume, report)); out(x, "1", "source.part_of")
    elif says == "has title" and n == 2:
        out(x, "1", "entity.label")
    elif says == "has title":
        own_attr(person(s), "unvan", v); out(x, "3", "own attribute 'unvan'", "No place for an academic title.")
    elif says == "was written by":
        err = rel(report, "authored_by", person(v)); out(x, "X" if err else "1", "relation authored_by", err or "")
    elif says == "has ORCID":
        _, err = attempt(L.insert, "identifier", entity=person(s), type="identifier_type/orcid", value=v)
        out(x, "X" if err else "1", "identifier", err or "")
    elif says == "has website":
        _, err = attempt(L.insert, "identifier", entity=person(s), type="identifier_type/url", value=v)
        out(x, "X" if err else "1", "identifier", err or "")
    elif says == "has affiliation":
        con.execute("UPDATE actor SET member_of = ? WHERE id = ?", (group(v), person(s)))
        out(x, "1", "actor.member_of", "The whole affiliation is one name. Faculty and department are not separated.")
    elif says in ("is named in page header of volume", "section contains") or (says == "is part of" and s.isupper() or
                                                                               says == "is part of" and v.isupper()):
        out(x, "X", "", "Structure of the printed document. No place, and not fieldwork data.")

    # ── people
    elif says == "participated in":
        a = group(s) if s in ("heyet üyeleri", "işçiler") else person(s)
        roles = [r for r in PEOPLE_ROLE.get(k, []) if r["value"].lower() in TEAM and r["page"] == x["page"]]
        role, own = (coded("role", roles[0]["value"]) if roles else (None, False))
        _, err = attempt(L.insert, "participation", activity=season, actor=a, role=role)
        out(x, "X" if err else "1", "participation", err or "")
        for r in roles[:1]:
            out(r, "X" if err else "3" if own else "1", "participation.role", err or ("own code for the role" if own else ""))
    elif says == "has the role":
        if v.lower() in TEAM:
            a = person(s)
            role, own = coded("role", v)
            if s.lower() in ("fatma durma", "şıvan ayus") and "Heyet" in v:
                _, err = attempt(L.insert, "participation", activity=season, actor=a, role=role)
                out(x, "X" if err else "3" if own else "1", "participation.role", err or ("own code for the role" if own else ""))
            else:
                out(x, "X", "", "The role was not tied to a participation by the loader.")
        elif v == "sponsor":
            role, own = coded("role", v)
            _, err = attempt(L.insert, "participation", activity=season, actor=group(s), role=role)
            out(x, "X" if err else "3" if own else "1", "participation.role", err or "own code for the role")
        else:
            own_attr(person(s), "görev", v)
            out(x, "3", "own attribute 'görev'", "An office held in an institution. No place for it. The institution "
                "inside the office name is not linked.")
    elif says in ("thanked for support", "thanked for"):
        if s.startswith("footnote"):
            remark(season, f"{s}: {v}"); out(x, "4", "entity.remark of the season")
        else:
            a = person(s) if (len(s.split()) in (2, 3) and s.lower() in PEOPLE_ROLE and s != "Safir Tuz") else group(s)
            role, own = coded("role", "teşekkür edilen")
            _, err = attempt(L.insert, "participation", activity=season, actor=a, role=role)
            out(x, "X" if err else "3", "participation.role", err or "own code: a person or body that is thanked")
    elif says == "was carried out with permission of":
        role, own = coded("role", "izin veren")
        _, err = attempt(L.insert, "participation", activity=season, actor=group(v), role=role)
        out(x, "X" if err else "3", "participation.role", err or "own code for the role")
    elif says == "was directed by":
        role, own = coded("role", "director")
        _, err = attempt(L.insert, "participation", activity=season, actor=person("Aytaç Coşkun"), role=role)
        out(x, "X" if err else "1", "participation.role", err or "")
    elif says in ("are continuously employed by", "were taken as service procurement under", "were employed through",
                  "were employed by"):
        remark(group(s), f"{says}: {v}"); out(x, "4", "entity.remark", "Employment has no place.")

    # ── the season
    elif says in ("took place from", "took place until"):
        remark(season, f"{says} {v}")
        out(x, "4", "entity.remark", "Years are whole numbers. The year 2024 is stored. Day and month are text only.")
    elif says == "continues for duration":
        if v == "12 ay":
            err, own = dim(season, "duration", value=12, unit="ay")
            out(x, "X" if err else "3", "dimension", err or "own code for the unit month")
        else:
            remark(season, f"süre: {v}"); out(x, "4", "entity.remark")
    elif says == "is season number":
        own_attr(season, "sezon sırası", v); out(x, "3", "own attribute", "No place for the running number of a season.")
    elif says in ("is a special project of",) or (says == "is described as" and "çalışmaları" in s):
        remark(season, f"{says}: {v}"); out(x, "4", "entity.remark")
    elif says == "is described as" and s == "Zikrullah Erdoğan":
        remark(person(s), v); out(x, "4", "entity.remark")
    elif says == "took place in season":
        out(x, "1", "activity.part_of")
    elif says == "took place in grid square":
        err = rel(dig, "also_at", place(v, "square"))
        out(x, "X" if err else "1", "relation also_at", err or
            "'T23/2-3-4' is stored as one place. It is not resolved into three squares.")
    elif says == "took place in":
        a = dig if s == "2024 yılı çalışmaları" else ents[k]
        err = rel(a, "worked_on", mithras if "Mithras" in v else site)
        out(x, "X" if err else "1", "relation worked_on", err or "")
    elif says == "has purpose" and k in ents:
        remark(ents[k], f"amaç: {v}"); out(x, "4", "entity.remark", "A purpose given as text has no place.")

    # ── places and buildings
    elif says in ("is located in", "is located in grid square", "was documented in grid square", "is located at",
                  "is concentrated in", "are kept in", "were moved to"):
        if "stratejik" in v:
            remark(site, v); out(x, "4", "entity.remark")
            continue
        if says == "is concentrated in":
            last_claim[k] = text_claim(x, site)
            continue
        t = thing(s, "E25") if k not in ents else ents[k]
        p = place(v, "square" if "grid" in says else None)
        has = con.execute("SELECT location FROM thing WHERE id = ?", (t,)).fetchone()
        if has is None:
            out(x, "X", "", "The subject is not a thing.")
        elif has["location"] is None:
            _, err = attempt(con.execute, "UPDATE thing SET location = ? WHERE id = ?", (p, t))
            out(x, "X" if err else "1", "thing.location", err or "")
        else:
            _, err = attempt(L.insert, "relation", subject=t, property="P53", object=p)
            out(x, "X" if err else "3", "relation with the raw property P53", err or
                "A thing has one column for its place. The second place needed a property taken from the ontology.")
    elif says in ("distance to Çınar ilçesi", "distance to Demirölçek Mahallesi"):
        remark(site, f"{says}: {v}"); out(x, "4", "entity.remark", "A distance between two places has no place.")
    elif says == "is also called":
        c, own = coded("identifier_type", "diğer ad")
        _, err = attempt(L.insert, "identifier", entity=mithras, type=c, value=v)
        out(x, "X" if err else "3", "identifier, own kind", err or "An entity has one name. A second name needed an own code.")
    elif says == "vegetation was cleaned around and inside":
        if s.startswith("yapılar"):
            remark(clean, v); out(x, "4", "entity.remark")
        else:
            err = rel(clean, "worked_on", mithras if "Mithras" in s else thing(s, "E25", type="building"))
            out(x, "X" if err else "1", "relation worked_on", err or "'Around and inside' is lost.")
    elif says == "was arranged":
        err = rel(ents["çevre düzenleme çalışmaları"], "worked_on", site); out(x, "X" if err else "1", "relation worked_on", err or "")
    elif says in ("is used as", "has use"):
        c, own = coded("function", v)
        _, err = attempt(L.insert, "assertion", subject=thing(s, "E22" if "cam" in s else "E25"), property="function",
                         object_code=c, claim=L.claim())
        out(x, "X" if err else "3", "assertion function", err or "own code. The list of functions is empty.")
    elif says == "is used for purpose":
        remark(thing(s, "E25"), v); out(x, "4", "entity.remark")
    elif says in ("was approved by", "was financed by"):
        a = activity("Ziyaretçi Karşılama Merkezi inşası", "E12", typ="inşaat", part_of=None)
        role, own = coded("role", "funder" if "financed" in says else "onaylayan")
        _, err = attempt(L.insert, "participation", activity=a, actor=group(v), role=role)
        out(x, "X" if err else "3" if own else "1", "participation.role", err or ("own code for the role" if own else ""))
    elif says == "construction continued":
        a = activity("Ziyaretçi Karşılama Merkezi inşası", "E12", typ="inşaat")
        err = rel(a, "worked_on", thing(s, "E25", type="building"))
        out(x, "X" if err else "3", "activity with an own kind, relation worked_on", err or "own code for the kind of work")

    # ── inventory
    elif says == "number of pieces":
        t = thing(s, "E22", type="assemblage")
        err, own = dim(t, "count", value=int(v.split()[0]), unit="piece")
        if "envanterlik" in s:
            L.insert("attribute_value", entity=t, attribute="museum_grade", value_number=1)
        out(x, "X" if err else "1", "dimension, kind count", err or "")
    elif says == "were delivered to":
        err = rel(thing(s, "E22"), "keeper", group(v)); out(x, "X" if err else "1", "relation keeper", err or "")
    elif says == "result of work of year":
        for t in ("envanterlik eserler", "etüdlük eserler"):
            _, err = attempt(L.insert, "find_context", thing=ents[t], found_by=season)
        out(x, "X" if err else "1", "find_context.found_by", err or "")

    # ── documentation
    elif says == "began in":
        a = activity(s, "E7", typ="documentation", begin=2014, scale="CE"); out(x, "1", "activity.begin")
    elif says == "missing parts were completed in":
        a = activity(s, "E7", typ="documentation", part_of=season); out(x, "1", "activity.part_of")
    elif says == "was made with instrument":
        err = rel(activity(s, "E7"), "used", thing(v, "E22", type="tool")); out(x, "X" if err else "1", "relation used", err or "")
    elif says == "were added to":
        remark(ents[k], f"{says}: {v}"); out(x, "4", "entity.remark")
    elif says == "is shown in figure":
        target = ents.get(k) or (dig if "kazı çalışmaları" in k else E(s, "media", "E36", type="plan"))
        m = re.match(r"(Resim|Çizim)\W*(\d+)(?:-(\d+))?", v)
        errs = [about(figure(f"{m.group(1)} {i}"), target) for i in range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1)]
        e = next((e for e in errs if e), None)
        out(x, "X" if e else "1", "about", e or "")
    elif says == "were completed" and "çizim" in s:
        a = activity(s, "E7", typ="documentation", part_of=season)
        _, err = attempt(L.insert, "relation", subject=a, property="P183", object=dig)
        out(x, "X" if err else "3", "relation with the raw property P183", err or
            "'Before the excavation': order in time between two works has no declared relation.")
    elif says in ("were documented in detail", "were documented", "was documented"):
        if says == "was documented":
            out(x, "X", "", "Says only that a kind of find was recorded. No entity to attach it to.")
        else:
            a = activity("Detaylı belgeleme çalışmaları", "E7", typ="documentation", part_of=season)
            err = rel(a, "worked_on", thing(s, "E22", type="assemblage"))
            out(x, "X" if err else "1", "relation worked_on", err or "")
    elif says in ("was documented by", "reconstruction drawings were completed", "reconstructions were updated"):
        kind = v if says == "was documented by" else "rekonstrüksiyon"
        m = L.entity("media", "E36", label=f"{s}: {kind}", type=kind)
        err = about(m, mithras if "Mithras" in s else thing(s, "E25"))
        own = is_own(con.execute("SELECT type FROM media WHERE id = ?", (m,)).fetchone()["type"])
        out(x, "X" if err else "3" if own else "1", "media with about", err or ("own code for the kind of record" if own else ""))
    elif says == "cites publication":
        src = source_for(v)
        if src is None:
            out(x, "X", "", f"'{v}' could not be matched to one entry of the bibliography.")
        elif "en erken" in s or "hayvan" in s:
            cl = last_claim.get("kutsal alan" if "en erken" in s else "hayvan")
            _, err = attempt(L.insert, "claim_basis", claim=cl, basis_entity=src)
            out(x, "X" if err else "1", "claim_basis", err or "")
        else:
            target = site if "Zerzevan" in s else mithras if "Mithras" in s else ents[k]
            err = about(src, target)
            out(x, "X" if err else "1", "about", err or
                "The source is tied to the thing, not to the sentence that cites it.")

    # ── the excavated area
    elif says == "has elevation" or says in ("highest elevation", "lowest elevation", "lies between elevations"):
        if "poligon" in s:
            p = place(s)
            err, own = dim(p, "elevation", value=metres(v)[0])
            if err:
                own_attr(p, "kot", v)
                out(x, "3", "own attribute 'kot'", f"Refused as a measurement: {err}. A place cannot carry a measurement.")
            else:
                out(x, "1", "dimension")
        else:
            t = ents.get(k) or thing(s, "E25")
            vals = metres(v)
            err, own = dim(t, "elevation", value=vals[0]) if len(vals) == 1 else dim(t, "elevation", lo=min(vals), hi=max(vals))
            note = "Highest and lowest are two statements. They share one row as a range." if "est " in says else ""
            if says == "lowest elevation":
                con.execute("DELETE FROM dimension WHERE entity = ? AND kind = 'dimension_kind/elevation'", (t,))
                err, own = dim(t, "elevation", lo=889.444, hi=892.444)
            out(x, "X" if err else "1", "dimension, kind elevation", err or note)
    elif says == "was used as reference for":
        err = rel(dig, "also_at", place(s))
        out(x, "X" if err else "3" if False else "4" if err else "4", "entity.remark", "")
        remark(place(s), f"{says}: {v}")
        OUT[n] = ("4", "entity.remark", "A reference point for levelling. 'Used' needs a thing, and a place is not a thing.")
    elif says == "was reached in area measuring":
        t = thing("ana kaya", "A2", type="layer")
        attempt(L.insert, "context", id=t)
        rel(dig, "removed", t)
        two_sizes(x, t)
    elif says == "were found on" and k in ("oyuklar", "kanallar"):
        t = thing(s, "E25", type="pit" if k == "oyuklar" else s)
        err = rel(t, "lies_in", thing("ana kaya", "A2"))
        out(x, "X" if err else "1", "relation lies_in", err or "")
    elif says in ("is interpreted as", "is interpreted as designed in accordance with", "was recorded as", "form",
                  "complement each other"):
        t = ents.get(k) or thing(s, "E25")
        last_claim[k] = text_claim(x, t)
    elif says == "is evaluated on the basis of":
        con.execute("UPDATE claim SET remark = COALESCE(remark || ' | ', '') || ? WHERE id = ?", (v, last_claim["kutsal alan"]))
        out(x, "4", "claim.remark", "The basis of a claim must be an entity or another claim. 'Its plan' is neither.")
    elif says == "runs in direction":
        own_attr(thing(s, "E25"), "doğrultu", v); out(x, "3", "own attribute 'doğrultu'", "No place for an orientation.")
    elif says in ("measures (length)", "measures (total height)", "measures (height)"):
        err, own = dim(ents.get(k) or thing(s, "E25"), "length" if "length" in says else "height", value=metres(v)[0])
        out(x, "X" if err else "1", "dimension", err or "")
    elif says in ("measures (width)", "measures (entrance dimensions)", "measures"):
        two_sizes(x, ents.get(k) or thing(s, "E25"))
    elif says in ("measures (depth in the north)", "measures (depth in the south)"):
        err, own = dim(thing(s, "E25"), "derinlik, " + ("kuzey" if "north" in says else "güney"), value=metres(v)[0])
        out(x, "X" if err else "3", "dimension, own kind", err or "A measurement taken at a named point of a thing needed an own code.")
    elif says == "depth varies according to":
        remark(thing(s, "E25"), f"{says}: {v}"); out(x, "4", "entity.remark")
    elif says == "more extensive trenches are planned for":
        p = L.entity("source", "E29", label=f"Planlanan açmalar: {v}", type="plan")
        err = about(p, thing("Drenaj sistemi", "E25"))
        own = is_own(con.execute("SELECT type FROM source WHERE id = ?", (p,)).fetchone()["type"])
        out(x, "X" if err else "3" if own else "1", "source of class E29 with about", err or "own code for the kind: a plan of work")
    elif says == "were numbered":
        remark(mithras, f"{s}: {v}"); out(x, "4", "entity.remark")
    elif says == "number of steps uncovered":
        err, own = dim(thing(s, "E25"), "basamak sayısı", value=11, unit="piece")
        out(x, "X" if err else "3", "dimension, own kind", err or "own code: number of steps")
    elif says == "is located behind":
        remark(thing(s, "E25"), f"{says}: {v}")
        out(x, "4", "entity.remark", "A position of one built thing relative to another has no declared relation.")
    elif says == "is covered with":
        t = thing("tonoz", "E25", type=v, part_of=thing(s, "E25"))
        own = is_own(con.execute("SELECT type FROM thing WHERE id = ?", (t,)).fetchone()["type"])
        out(x, "3" if own else "1", "thing.part_of", "Stored as a vault that is part of the hall. own code for the kind of vault.")
    elif says == "preserved part":
        err, own = dim(thing("tonoz", "E25"), "korunan uzunluk", value=1)
        out(x, "X" if err else "3", "dimension, own kind", err or "own code: preserved length")
    elif says == "lie below":
        a, b = thing(v, "E25", class2="A8", type="floor"), thing(s, "E25", class2="A8")
        for t in (a, b):
            attempt(L.insert, "context", id=t)
        err = rel(a, "overlies", b)
        out(x, "X" if err else "1", "relation overlies", err or "Stored in the other direction: the floor overlies the sockets.")
    elif says in ("was found in grid square", "were uncovered in grid square", "was found in position within grid square"):
        t = ents.get(k) or thing(s, "E22", type="assemblage")
        _, err = attempt(L.insert, "find_context", thing=t, found_in=place(v, "square"), found_by=dig)
        out(x, "X" if err else "1", "find_context.found_in", err or "")
    elif says == "were uncovered in year":
        out(x, "1", "find_context.found_by", "Through the excavation work, which is part of the season of 2024.")
    elif says == "number of unit numbers given":
        err, own = dim(thing(s, "E22"), "count", value=56, unit="piece"); out(x, "X" if err else "1", "dimension, kind count", err or "")
    elif says == "are numbered in range":
        c, own = coded("identifier_type", "ünit numarası")
        _, err = attempt(L.insert, "identifier", entity=thing("özellikli mimari bloklar", "E22"), type=c, value=v)
        out(x, "X" if err else "3", "identifier, own kind", err or "A range of numbers for 56 blocks is stored as one text.")

    # ── the site in general
    elif says == "was founded in":
        p = E("MS 2.-3. yüzyıllar", "period", "E4", start_earliest=100, end_latest=299, scale="CE")
        _, err = attempt(L.insert, "dating", subject=site, event="making", period=p, claim=L.claim())
        out(x, "X" if err else "1", "dating, event making", err or
            "Worked only because the site was given a second class. A site alone cannot have a making.")
    elif says in ("was founded in an arrangement to meet", "conforms at minimum level with", "hosts many structures reflecting",
                  "is notable in terms of", "is described as", "is described as unique in terms of"):
        remark(ents.get(k) or site, f"{s} {says}: {v}"); out(x, "4", "entity.remark")
    elif says == "was uncovered by":
        t = mithras if s == "tapınak" else thing("Yeraltı Yapısı", "E25")
        err = rel(season, "worked_on", t); out(x, "X" if err else "1", "relation worked_on", err or "")
    elif says == "was built with technique":
        own_attr(mithras, "yapım tekniği", v); out(x, "3", "own attribute", "No place for a building technique.")
    elif says == "frequently encountered at its eastern borders":
        out(x, "X", "", "History in general. Its subject is not part of the fieldwork.")

    # ── finds in store
    elif says == "were evaluated in detail in":
        a = activity("Eser deposu değerlendirme çalışmaları", "E7", typ="analysis", part_of=season)
        err = rel(a, "worked_on", thing("eserler", "E22", type="assemblage")); out(x, "X" if err else "1", "relation worked_on", err or "")
    elif says in ("have a wide range in terms of", "were grouped by", "shows", "has functional details such as",
                  "show variety suited to", "provide important data about", "contribute to understanding of"):
        t = thing("seramikler" if says in ("have a wide range in terms of", "were grouped by") else s, "E20" if "kemik" in s else "E22",
                  type="assemblage")
        remark(t, f"{says}: {v}"); out(x, "4", "entity.remark")
    elif says == "is a kind of":
        parent, _ = coded("thing_type", v)
        child, _ = coded("thing_type", s)
        con.execute("UPDATE code SET parent = ? WHERE id = ?", (parent, child))
        out(x, "3", "code.parent, between two own codes", "A statement about the vocabulary. Both terms are missing from the list.")
    elif says == "is among important metal finds":
        t = thing(s, "E22", type="assemblage", part_of=thing("Metal buluntular", "E22", type="assemblage"))
        out(x, "1", "thing.part_of", "'Important' is lost.")
    elif says == "is made of":
        c, own = coded("material", v)
        con.execute("UPDATE thing SET material = ? WHERE id = ?", (c, thing(s, "E22")))
        out(x, "3" if own else "1", "thing.material")
    elif says == "was made with technique":
        own_attr(thing("Metal buluntular", "E22"), "üretim tekniği: " + v, "var")
        out(x, "3", "own attribute", "No place for a technique of making.")
    elif says == "is dated to" and "cam" in s:
        p = E("MS 1.-7. yüzyıllar", "period", "E4", start_earliest=1, end_latest=699, scale="CE")
        _, err = attempt(L.insert, "dating", subject=thing(s, "E22", type="assemblage"), event="making", period=p, claim=L.claim())
        out(x, "X" if err else "1", "dating", err or "")
    elif says == "is dated to":
        remark(figure(s), f"tarih: {v}"); out(x, "4", "entity.remark", "A drawing has no year of its own.")
    elif says == "include form":
        c, own = coded("thing_type", v)
        L.entity("thing", "E22", label=f"cam {v}", type=c, part_of=thing("cam eserler", "E22"))
        out(x, "3" if own else "1", "thing.type and thing.part_of", "own code for the form" if own else "")
    elif says == "were examined in":
        a = L.entity("activity", "S4", label=v, type="analysis", part_of=season)
        L.insert("analysis", id=a, method="zooarchaeology")
        ents["arkeozooloji"] = a
        err = rel(a, "observed", thing(s, "E20", type="animal_bone")); out(x, "X" if err else "1", "analysis and relation observed", err or "")
    elif says == "species was identified among animal bones":
        src = source_for(x["who"])
        cl = L.claim(kind="adopted", passage=src)
        last_claim["hayvan"] = cl
        c, own = coded("taxon", s)
        part = L.entity("thing", "E20", label=s, part_of=thing("hayvan kemik kalıntıları", "E20"))
        _, err = attempt(L.insert, "assertion", subject=part, property="taxon", object_code=c, claim=cl)
        out(x, "X" if err else "3", "assertion taxon, with a claim taken from a source", err or
            "own code. The list of species is empty.")

    # ── conservation
    elif says in ("was restored", "conservation was completed"):
        a = activity("Restorasyon ve konservasyon çalışmaları", "E11", typ="conservation", part_of=season)
        err = rel(a, "modified", thing(s, "E22", type="assemblage")); out(x, "X" if err else "1", "relation modified", err or "")
    elif says in ("show on surface", "have on them", "show"):
        c, own = coded("condition", v)
        cl = L.claim(belief="probable" if x["hedge"] else "true")
        _, err = attempt(L.insert, "assertion", subject=thing(s, "E22", type="assemblage"), property="condition",
                         object_code=c, claim=cl)
        out(x, "X" if err else "3", "assertion condition, with a claim", err or "own code for the kind of damage")
    elif says in ("were softened with", "were joined with", "surface is coated with", "was prepared at concentration"):
        a = activity("Restorasyon ve konservasyon çalışmaları", "E11", typ="conservation")
        name = re.sub(r"\s*\(?%[\d-]+\)?( oranında( hazırlanan)?)?\s*", " ", v if "prepared" not in says else s).strip()
        sub = thing(name, "E22", type="konservasyon malzemesi")
        if not con.execute("SELECT 1 FROM relation WHERE subject = ? AND object = ?", (a, sub)).fetchone():
            rel(a, "used", sub)
        pc = re.findall(r"%(\d+)(?:-(\d+))?", v + " " + s)[0]
        err, own = dim(sub, "derişim", value=float(pc[0]) if not pc[1] else None, lo=float(pc[0]) if pc[1] else None,
                       hi=float(pc[1]) if pc[1] else None, unit="percent")
        out(x, "X" if err else "3", "relation used, and dimension of an own kind", err or
            "own code: concentration. One substance with three concentrations for three uses cannot be told apart.")
    elif says in ("were mechanically cleaned with", "were treated with", "were cleaned under", "were removed with",
                  "was immersed in", "were treated mechanically in", "was used where"):
        a = activity("Restorasyon ve konservasyon çalışmaları", "E11", typ="conservation")
        tool = thing(s if says == "was used where" else v, "E22", type="tool")
        err = None
        if not con.execute("SELECT 1 FROM relation WHERE subject = ? AND object = ?", (a, tool)).fetchone():
            err = rel(a, "used", tool)
        out(x, "X" if err else "1", "relation used", err or "Which tool was used on which material is lost.")
    elif says == "could not clean some places":
        remark(thing("dişçi motorunun çeşitli başlıkları", "E22"), f"{s}: {v}")
        out(x, "4", "entity.remark", "A negative statement about a tool. A claim with the belief false needs a relation to deny.")
    elif says in ("were measured (weight)", "were measured (dimensions)", "were measured again (weight)",
                  "were measured again (dimensions)", "was prepared after", "were treated according to", "were completed") \
            or (says == "has purpose"):
        a = activity("Restorasyon ve konservasyon çalışmaları", "E11", typ="conservation")
        remark(a, f"{s} {says}: {v}")
        out(x, "4", "entity.remark", "Says that something was measured or done. No value is given." if "measured" in says else "")

    # ── figures
    elif says == "figure shows":
        f = figure(s)
        con.execute("UPDATE entity SET label = ? WHERE id = ?", (f"{s}: {v}", f))
        p = L.entity("passage", "E31", label=f"s. {x['page']}", source=report, locator=str(x["page"]))
        con.execute("UPDATE media SET shown_in = ? WHERE id = ?", (p, f))
        out(x, "1", "entity.label of the media item")
    else:
        out(x, "X", "", "No rule in the loader. Not tried.")

con.commit()

missing = [x["n"] for x in S if x["n"] not in OUT]
assert not missing, missing
with open(HERE / "outcome.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["n", "page", "subject", "says", "value", "hedge", "outcome", "where", "note"])
    for x in S:
        w.writerow([x["n"], x["page"], x["subject"], x["says"], x["value"], x["hedge"], *OUT[x["n"]]])

names = {"1": "typed", "2": "template", "3": "own", "4": "text only", "X": "not stored"}
c = Counter(v[0] for v in OUT.values())
print(f"statements {len(S)}")
for k in "1234X":
    print(f"   {k} {names[k]:11} {c[k]:5}  {100 * c[k] / len(S):5.1f} %")
finds = {x["n"] for s in find_subjects for x in by_subject[s]}
rest = [n for n in OUT if n not in finds]
for title, ns in (("find list", finds), ("all other statements", rest)):
    cc = Counter(OUT[n][0] for n in ns)
    print(f"{title}: {len(ns)}  " + "  ".join(f"{k}={cc[k]}" for k in "1234X"))
print("\nnot stored, by reason")
for (note, says), k in Counter((OUT[x["n"]][2][:110], x["says"]) for x in S if OUT[x["n"]][0] == "X").most_common():
    print(f"   {k:4}  {says}: {note}")
print("\ntext only, by kind of statement")
for (says, note), k in Counter((x["says"], OUT[x["n"]][2][:90]) for x in S if OUT[x["n"]][0] == "4").most_common():
    print(f"   {k:4}  {says}: {note}")
print("\nown, by reason")
for (where, note), k in Counter((OUT[x["n"]][1], OUT[x["n"]][2][:90]) for x in S if OUT[x["n"]][0] == "3").most_common():
    print(f"   {k:4}  {where}: {note}")
print("\nhedges lost:", sum("hedge" in v[2] and "is lost" in v[2] for v in OUT.values()), "of", sum(bool(x["hedge"]) for x in S))
print("\nown codes made, by list")
for r in con.execute("SELECT list, count(*) AS k FROM code WHERE owner IS NOT NULL GROUP BY list ORDER BY k DESC"):
    print(f"   {r['k']:4}  {r['list']}")
