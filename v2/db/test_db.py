#!/usr/bin/env python3
"""Tests of the version 2 database on a fresh copy. Run: python test_db.py

Part 1  wrong entries that the database must refuse
Part 2  entries that must work: a conflict, a chain of claims, a negative statement,
        a count table, a list sheet with an unknown column, a survey sheet
"""
import csv
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import fieldwork_db as fw

HERE = Path(__file__).resolve().parent
TMP = Path(tempfile.mkdtemp())
DB = TMP / "test.sqlite"
PY = sys.executable
run = lambda *a: subprocess.run([PY, str(HERE / "fieldwork_db.py"), *map(str, a)], capture_output=True, text=True)

assert run("init", DB).returncode == 0
con = fw.connect(DB)
con.execute("INSERT INTO dataset (id,title,fieldwork) VALUES ('t','Test','Test Höyük')")
con.execute("INSERT INTO dataset (id,title,fieldwork) VALUES ('u','Other','Other Höyük')")
L = fw.Loader(con, "t")
con.execute("BEGIN")
con.execute("PRAGMA defer_foreign_keys = ON")
trench = L.entity("place", "E53", label="Açma A", type="trench")
person = L.entity("actor", "E21", label="Ayşe Kaya")
lab = L.entity("actor", "E74", label="Laboratuvar")
season = L.entity("activity", "A9", label="2024 sezonu", type="season", begin=2024, end=2024, scale="CE")
unit = L.entity("activity", "A1", label="Açma A kazısı", type="excavation_unit", part_of=season, place=trench)
layer1 = L.entity("thing", "A2", label="Tabaka 1", type="layer", location=trench)
layer2 = L.entity("thing", "A2", label="Tabaka 2", type="layer", location=trench)
cut = L.entity("thing", "A3", label="Çukur kesimi", type="pit")
wall = L.entity("thing", "E25", label="Duvar 1", type="wall", class2="A8")
oven = L.entity("thing", "E25", label="Fırın", type="oven", class2="A8")
for x in (layer1, layer2, cut, wall, oven):
    L.insert("context", id=x)
sherd = L.entity("thing", "E22", label="Sırlı seramik", type="pottery", material="ceramic")
bone = L.entity("thing", "E20", label="Koyun kemiği", type="animal_bone")
roman = L.entity("period", "E4", label="Roma Dönemi", start_earliest=-30, end_latest=395, scale="CE")
c13 = L.entity("period", "E4", label="13. yüzyıl", start_earliest=1200, end_latest=1299, scale="CE")
report = L.entity("source", "E31", label="Rapor", type="excavation_report", year=2026)
page = L.entity("passage", "E31", label="s. 12", source=report, locator="12")
photo = L.entity("media", "E36", label="Resim 1", type="photograph")
con.commit()

# ───────────── Part 1: refusals ─────────────
WRONG = [
    ("a class that is not in the ontology",
     lambda: L.entity("thing", "E999", label="x")),
    ("a person registered as a thing",
     lambda: L.entity("thing", "E21", label="x")),
    ("an activity registered as a period",
     lambda: L.entity("period", "E7", label="x")),
    ("a code from the wrong list",
     lambda: L.insert("thing", id=L.entity("thing", "E22"), type="material/bronze") if False else
     con.execute("UPDATE thing SET type = 'material/bronze' WHERE id = ?", (sherd,))),
    ("a withdrawn code",
     lambda: (con.execute("UPDATE code SET state = 'withdrawn' WHERE id = 'thing_type/lamp'"),
              con.execute("UPDATE thing SET type = 'thing_type/lamp' WHERE id = ?", (sherd,)))),
    ("a work that took place at a find",
     lambda: con.execute("UPDATE activity SET place = ? WHERE id = ?", (sherd, unit))),
    ("a thing that is part of itself",
     lambda: con.execute("UPDATE thing SET part_of = id WHERE id = ?", (sherd,))),
    ("years in the wrong order",
     lambda: L.entity("activity", "E7", label="x", begin=2024, end=2020, scale="CE")),
    ("years before present in the wrong order",
     lambda: L.insert("dating", subject=bone, event="death", begin=9000, end=9500, scale="BP", claim=L.claim())),
    ("years without a scale",
     lambda: L.entity("activity", "E7", label="x", begin=2024)),
    ("a date without a claim",
     lambda: con.execute("INSERT INTO dating (id,subject,event,period) VALUES ('d',?,?,?)", (sherd, "making", roman))),
    ("the making of a bone",
     lambda: L.insert("dating", subject=bone, event="making", period=roman, claim=L.claim())),
    ("the death of a wall",
     lambda: L.insert("dating", subject=wall, event="death", period=roman, claim=L.claim())),
    ("a stratigraphic relation with a find",
     lambda: L.insert("relation", subject=layer1, type="overlies", object=sherd)),
    ("an excavation unit that removed a person",
     lambda: L.insert("relation", subject=unit, type="removed", object=person)),
    ("a property of the ontology with the wrong domain",
     lambda: L.insert("relation", subject=sherd, property="P14", object=person)),
    ("a property stored in the inverse direction",
     lambda: L.insert("relation", subject=person, property="P14i", object=unit)),
    ("a property that does not exist",
     lambda: L.insert("relation", subject=unit, property="P999", object=person)),
    ("a relation with a type and a property at once",
     lambda: L.insert("relation", subject=unit, type="used", property="P16", object=sherd)),
    ("a conclusion stored as a plain relation",
     lambda: L.insert("relation", subject=layer1, type="earlier_than", object=layer2)),
    ("a record stored as a conclusion",
     lambda: L.insert("assertion", subject=layer1, property="overlies", object_entity=layer2, claim=L.claim())),
    ("a conclusion without a claim",
     lambda: con.execute("INSERT INTO assertion (id,subject,property,object_text) VALUES ('a',?,?,?)",
                         (wall, "interpreted_as", "depo"))),
    ("an assertion with a term where an entity is needed",
     lambda: L.insert("assertion", subject=sherd, property="similar_to", object_code="thing_type/coin", claim=L.claim())),
    ("an assertion with a term from the wrong list",
     lambda: L.insert("assertion", subject=sherd, property="material_is", object_code="thing_type/coin", claim=L.claim())),
    ("an attribute on the wrong class",
     lambda: L.insert("attribute_value", entity=sherd, attribute="soil_colour", value_text="kahverengi")),
    ("text in a number attribute",
     lambda: L.insert("attribute_value", entity=unit, attribute="sieve_mesh", value_text="ince")),
    ("an attribute of another dataset",
     lambda: (con.execute("INSERT INTO attribute_def (id,label_en,applies_to,value_type,owner) VALUES "
                          "('u/x','x','E1','text','u')"),
              L.insert("attribute_value", entity=sherd, attribute="u/x", value_text="y"))),
    ("a context row for a find",
     lambda: L.insert("context", id=sherd)),
    ("a layer that confines",
     lambda: con.execute("UPDATE context SET confines = ? WHERE id = ?", (layer2, layer1)) if False else
     L.insert("context", id=L.entity("thing", "A2", label="x"), confines=layer1)),
    ("a sample row for a thing that is not a sample",
     lambda: L.insert("sample", id=sherd)),
    ("an analysis that is not an observation",
     lambda: L.insert("analysis", id=L.entity("activity", "E11", label="Onarım", type="restoration"),
                      method="radiocarbon")),
    ("a claim taken from a source without the passage",
     lambda: L.claim(kind="adopted")),
    ("a claim that rests on itself",
     lambda: (lambda c: L.insert("claim_basis", claim=c, basis_claim=c))(L.claim())),
    ("a geometry that is not coordinates",
     lambda: L.insert("geometry", entity=trench, kind="point", wkt="near the river", crs="crs/EPSG:4326")),
    ("a geometry without a coordinate system",
     lambda: con.execute("INSERT INTO geometry (id,entity,kind,wkt) VALUES ('g',?,?,?)", (trench, "point", "POINT(1 2)"))),
    ("an embargo without a date",
     lambda: con.execute("INSERT INTO dataset (id,title,fieldwork,access) VALUES ('e','x','x','embargo')")),
    ("a photograph given as the subject of a photograph of itself",
     lambda: L.insert("about", item=photo, target=photo)),
    ("a find given as a source",
     lambda: L.insert("about", item=sherd, target=wall)),
    ("a standard code linked as if it were an own code",
     lambda: con.execute("INSERT INTO own_code VALUES ('thing_type/coin','thing_type/lamp','same')")),
    ("a change of class after entry",
     lambda: con.execute("UPDATE entity SET class = 'E20' WHERE id = ?", (sherd,))),
    ("a relation type whose range does not fit its property",
     lambda: con.execute("INSERT INTO relation_type (code,label_en,module,property,domain,range) VALUES "
                         "('bad','bad','core','P14','E7','E53')")),
    ("a row in a table the entity is not registered for",
     lambda: con.execute("INSERT INTO place (id) VALUES (?)", (sherd,))),
]
refused = 0
for what, fn in WRONG:
    con.execute("BEGIN")
    try:
        fn()
        con.execute("COMMIT")
        print(f"   ACCEPTED  {what}")
    except (sqlite3.IntegrityError, fw.Refused) as e:
        con.execute("ROLLBACK")
        refused += 1
print(f"part 1: {refused} of {len(WRONG)} wrong entries refused")

# ───────────── Part 2: what must work ─────────────
ok = []
def expect(what, cond):
    ok.append(bool(cond))
    print(f"   {'ok    ' if cond else 'FAILED'} {what}")

con.execute("BEGIN")
con.execute("PRAGMA defer_foreign_keys = ON")
# a conflict: the oven by radiocarbon, the pottery from it by type
L.insert("find_context", thing=sherd, found_in=oven, found_by=unit, method="hand")
charcoal = L.entity("thing", "S13", label="Kömür örneği", type="charcoal")
taking = L.entity("activity", "S2", label="Örnek alma", type="sampling", part_of=unit)
L.insert("sample", id=charcoal, taken_from=oven, taken_by=taking)
c14 = L.entity("activity", "S4", label="C14", type="dating")
L.insert("analysis", id=c14, method="radiocarbon", laboratory=lab, lab_code="TEST-1")
L.insert("relation", subject=c14, type="observed", object=charcoal)
lab_claim = L.claim(kind="inferred", method="reasoning_method/laboratory_measurement", made_by=lab)
L.insert("claim_basis", claim=lab_claim, basis_entity=c14)
L.insert("dating", subject=oven, event="use", begin=1387, end=1476, scale="CE", claim=lab_claim)
type_claim = L.claim(kind="inferred", belief="probable", method="reasoning_method/typological_comparison", made_by=person)
L.insert("dating", subject=sherd, event="making", period=c13, claim=type_claim)
# a chain: the wall is dated through the oven, the building through the wall
wall_claim = L.claim(kind="inferred", belief="probable", method="reasoning_method/stratigraphic_position", made_by=person)
L.insert("claim_basis", claim=wall_claim, basis_claim=lab_claim)
L.insert("dating", subject=wall, event="making", begin=1350, end=1400, scale="CE", approx=1, claim=wall_claim)
phase_claim = L.claim(kind="inferred", belief="possible", made_by=person)
L.insert("claim_basis", claim=phase_claim, basis_claim=wall_claim)
L.insert("assertion", subject=wall, property="interpreted_as", object_text="geç dönem atölyesi", claim=phase_claim)
# a negative statement
bedrock = L.entity("thing", "A2", label="Ana kaya", type="layer")
L.insert("context", id=bedrock)
no = L.claim(belief="false", made_by=person, passage=page)
L.insert("relation", subject=unit, type="removed", object=bedrock, claim=no)
# a hedged find place, an own attribute, a property taken from the ontology, a geometry, years before present
L.insert("find_context", thing=bone, found_in=layer2, claim=L.claim(belief="possible"))
L.insert("dating", subject=bone, event="death", begin=9500, end=9000, scale="BP", error=40, claim=L.claim(kind="inferred"))
L.insert("relation", subject=cut, type="cuts", object=layer2)
L.insert("relation", subject=layer1, type="overlies", object=layer2)
L.insert("relation", subject=person, property="P74", object=trench)
L.insert("geometry", entity=trench, kind="polygon", wkt="POLYGON((34.6 36.8, 34.7 36.8, 34.7 36.9, 34.6 36.8))",
         crs="crs/EPSG:4326", precision_m=0.5)
L.insert("dimension", entity=unit, kind="dimension_kind/removed_volume", value=8710, unit="unit/litre")
L.insert("attribute_value", entity=unit, attribute="sieve_mesh", value_number=2)
L.insert("about", item=photo, target=oven)
L.insert("participation", activity=season, actor=person, role="director")
con.commit()

notes = fw.conflicts(con)
expect("the conflict between the oven and its pottery is listed", any("Fırın" in n and "Sırlı" in n for n in notes))
falls = fw.depends_on(con, lab_claim)
expect("revising the laboratory date reaches the wall and the interpretation", set(falls) == {wall_claim, phase_claim})

ex = fw.Exporter(con, "t")
g = ex.export()
bad = ex.errors + ex.validate()
expect(f"the graph has no statement against the ontology ({len(g)} statements)", not bad)
for b in bad[:10]:
    print("        ", b)
AP5 = fw.URIRef(ex.terms["AP5"]["uri"])
expect("the negative statement is in the graph as a claim and not as a fact",
       (ex.uri("entity", unit), AP5, ex.uri("entity", bedrock)) not in g
       and any(str(o) == "false" for o in g.objects(None, fw.URIRef(ex.terms["J5"]["uri"]))))
P10 = fw.URIRef(ex.terms["P10"]["uri"])
expect("the probable period of the sherd is not written as a fact",
       not any(o == ex.uri("entity", c13) for o in g.objects(None, P10)))
O21 = fw.URIRef(ex.terms["O21"]["uri"])
expect("the possible find place of the bone is not written as a fact",
       not any(o == ex.uri("entity", layer2) for o in g.objects(None, O21)))

# a loop in the stratigraphy is found by the check
con.execute("BEGIN")
loop = L.insert("relation", subject=layer2, type="overlies", object=layer1)
con.commit()
expect("a loop in the stratigraphy is reported", any("lies above itself" in x for x in fw.check_data(con)))
con.execute("DELETE FROM relation WHERE id = ?", (loop,))
con.commit()

# sheets
sheet = TMP / "finds.csv"
expect("an empty sheet is written", run("sheet", DB, "finds", "-o", sheet).returncode == 0)
head = next(csv.reader(open(sheet, encoding="utf-8-sig"), delimiter=";"))
with open(sheet, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(head + ["Hamur rengi"])                       # a column the template does not know
    w.writerow(["B-101", "Kandil parçası", "kandil", "seramik", "Tabaka 1", "1", "Roma Dönemi", "parça", "evet", "", "kiremit"])
    w.writerow(["B-102", "Sikke", "sikke", "bronz", "Tabaka 2", "3", "Roma Dönemi?", "", "", "yüzeyi aşınmış", ""])
    w.writerow(["B-103", "Ağırşak", "ağırşak", "taş", "Tabaka 2", "1", "", "", "", "", "gri"])
r = run("fill", DB, "finds", "t", sheet)
expect("a filled sheet with an unknown column and an unknown term is stored", r.returncode == 0)
q = lambda s, *a: con.execute(s, a).fetchone()[0]
expect("the unknown term became an own code", q("SELECT count(*) FROM code WHERE owner = 't' AND code = 'ağırşak'") == 1)
expect("the unknown column became an own attribute with two values",
       q("SELECT count(*) FROM attribute_value WHERE attribute = 't/Hamur rengi'") == 2)
expect("'Roma Dönemi?' became a possible date",
       q("SELECT count(*) FROM dating d JOIN claim c ON c.id = d.claim JOIN entity e ON e.id = d.subject "
         "WHERE e.source_id = 'B-102' AND c.belief = 'possible'") == 1)
with open(sheet, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(head)
    w.writerow(["B-104", "Boncuk", "boncuk", "cam", "Tabaka 99", "1", "", "", "", ""])
r = run("fill", DB, "finds", "t", sheet)
expect("a sheet that names an unknown context is refused as a whole",
       r.returncode == 1 and q("SELECT count(*) FROM entity WHERE source_id = 'B-104'") == 0)

matrix = TMP / "lithics.csv"
with open(matrix, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Tür", "Neolitik", "Neolitik?", "Toplam"])
    w.writerow(["dilgi", "10", "4", "15"])                       # printed 15, cells 14
    w.writerow(["çekirdek", "3", "", "3"])
    w.writerow(["Toplam", "13", "5", "18"])                      # column 2 printed 5, cells 4
r = run("fill", DB, "count_by_period", "t", matrix, "--label", "Yontmataş")
expect("a count table is stored", r.returncode == 0)
sums = fw.sum_check(con, "t")
expect("the row and the column whose printed totals do not match are reported, and nothing else",
       len(sums) == 2 and any("dilgi" in s for s in sums) and any("Neolitik?" in s for s in sums))
for s in sums:
    print("        ", s)

survey = TMP / "survey.csv"
run("sheet", DB, "survey_units", "-o", survey)
head = next(csv.reader(open(survey, encoding="utf-8-sig"), delimiter=";"))
with open(survey, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(head)
    w.writerow(["YA-01", "Tarla 1", "yüzey araştırması birimi", "", "POINT(30.1 38.2)", "60", "nadas", ""])
    w.writerow(["YA-02", "Tarla 2", "yüzey araştırması birimi", "", "POINT(30.2 38.2)", "20", "zeytinlik", "yoğun bitki örtüsü"])
r = run("fill", DB, "survey_units", "t", survey)
expect("a survey sheet with coordinates is stored", r.returncode == 0 and q("SELECT count(*) FROM geometry") == 3)

expect("the check finds nothing wrong", run("check", DB).returncode == 0)
a = run("audit", DB)
expect("every column with data reaches the graph", a.returncode == 0)
if a.returncode:
    print(a.stdout)
v = run("view", DB, "t", "-o", TMP / "view")
text = (TMP / "view" / "t_thing.csv").read_text(encoding="utf-8-sig") + (TMP / "view" / "t_activity.csv").read_text(encoding="utf-8-sig")
expect("the view shows the own attribute, the negative statement and the hedged date",
       "Hamur rengi" in text and "Ana kaya (NOT)" in text and "(possible)" in text)
print(f"part 2: {sum(ok)} of {len(ok)} passed")
sys.exit(0 if refused == len(WRONG) and all(ok) else 1)
