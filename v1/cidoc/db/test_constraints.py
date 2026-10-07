#!/usr/bin/env python3
"""What the tables refuse. Each case must fail; the database is left unchanged.

Usage: python db/test_constraints.py out/excavations.sqlite
"""
import copy
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from excavation_db import Loader, UnknownField, connect  # noqa: E402

R = "yumuktepe-2024"
SQL_CASES = [
    ("a class outside the ontologies",
     "INSERT INTO entity VALUES ('{r}','x1','find')",
     "INSERT INTO find (report,id,class,label,type,found_by) VALUES ('{r}','x1','E99_Treasure','x','coin','campaign-2024')"),
    ("a class of the wrong family (a find typed as a person)",
     "INSERT INTO entity VALUES ('{r}','x1','find')",
     "INSERT INTO find (report,id,class,label,type,found_by) VALUES ('{r}','x1','E21_Person','x','coin','campaign-2024')"),
    ("a find from a trench that does not exist",
     "INSERT INTO entity VALUES ('{r}','x1','find')",
     "INSERT INTO find (report,id,class,label,type,found_by) VALUES ('{r}','x1','E22_Human-Made_Object','x','coin','trench-zz')"),
    ("a find without the unit that found it",
     "INSERT INTO entity VALUES ('{r}','x1','find')",
     "INSERT INTO find (report,id,class,label,type) VALUES ('{r}','x1','E22_Human-Made_Object','x','coin')"),
    ("a period that ends before it begins",
     "INSERT INTO entity VALUES ('{r}','x1','period')",
     "INSERT INTO period (report,id,label,begin_year,end_year) VALUES ('{r}','x1','x',1300,1200)"),
    ("a year 0",
     "INSERT INTO entity VALUES ('{r}','x1','period')",
     "INSERT INTO period (report,id,label,begin_year,end_year) VALUES ('{r}','x1','x',0,100)"),
    ("a stratigraphic relation of an unknown type",
     "INSERT INTO entity VALUES ('{r}','x1','relation')",
     "INSERT INTO relation (report,id,from_context,type,to_context) VALUES ('{r}','x1','a701','is near','bx')"),
    ("a context that cuts itself",
     "INSERT INTO entity VALUES ('{r}','x1','relation')",
     "INSERT INTO relation (report,id,from_context,type,to_context) VALUES ('{r}','x1','a701','cuts','a701')"),
    ("a malformed ORCID",
     "INSERT INTO entity VALUES ('{r}','x1','actor')",
     "INSERT INTO actor (report,id,class,label,orcid) VALUES ('{r}','x1','E21_Person','x','0000-0001')"),
    ("a measurement without a value",
     "INSERT INTO dimension (report,id,position,type,unit) VALUES ('{r}','a701',99,'length','m')"),
    ("the same id used twice in one report",
     "INSERT INTO entity VALUES ('{r}','a701','find')"),
]


def main(path):
    con = connect(Path(path))
    ids = [r[0] for r in con.execute("SELECT id FROM context WHERE report=? AND kind='feature' LIMIT 2", (R,))]
    failed = 0
    for label, *statements in SQL_CASES:
        try:
            con.execute("BEGIN")
            for s in statements:
                con.execute(s.format(r=R).replace("'a701'", f"'{ids[0]}'").replace("'bx'", f"'{ids[1]}'"))
            con.execute("COMMIT")
            print(f"  ACCEPTED (wrong)  {label}")
            failed += 1
        except sqlite3.IntegrityError as e:
            print(f"  refused   {label:58s} {e}")
        finally:
            if con.in_transaction:
                con.execute("ROLLBACK")
    # a record with a field the tables have no column for
    rec = json.loads((Path(__file__).resolve().parent.parent / "data/yumuktepe_2024.json").read_text(encoding="utf-8"))
    rec = copy.deepcopy(rec)
    rec["base_uri"] = rec["base_uri"].replace("yumuktepe-2024", "test-unknown-field")
    rec["finds"][0]["weight_g"] = 12
    try:
        Loader(con, rec).load()
        print("  ACCEPTED (wrong)  a field without a column")
        failed += 1
    except UnknownField as e:
        print(f"  refused   {'a field without a column':58s} {e}")
    finally:
        if con.in_transaction:
            con.rollback()
    print(f"{len(SQL_CASES) + 1 - failed} of {len(SQL_CASES) + 1} refused")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
