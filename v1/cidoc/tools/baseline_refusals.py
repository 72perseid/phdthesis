#!/usr/bin/env python3
"""Load a record into a copy of the database and list everything it refuses.

A refused field is removed and the load is tried again, until the record goes
in.  The list is what the tables could not hold.

Usage: python tools/baseline_refusals.py out/excavations.sqlite data/sinekkaya_2024.json
"""
import json
import re
import shutil
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "db"))
from excavation_db import Loader, UnknownField, connect  # noqa: E402

db, rec_path = Path(sys.argv[1]), Path(sys.argv[2])
rec = json.loads(rec_path.read_text(encoding="utf-8"))
tmp = Path(tempfile.mkdtemp()) / "copy.sqlite"
refused = Counter()
for _ in range(2000):
    shutil.copy(db, tmp)
    con = connect(tmp)
    try:
        Loader(con, rec).load()
        break
    except UnknownField as e:
        where, fields = re.match(r"(.*): no column for (.*)", str(e)).groups()
        for f in eval(fields) if fields.startswith("[") else [fields.split("'")[1]]:
            if where == "record":
                refused[f"list '{f}' ({len(rec[f])} items)"] += 1
                del rec[f]
            else:
                lst, ident = where.split("/", 1)
                lst = lst.split(".")[0]
                item = next(i for i in rec[lst] if str(i.get("id", i.get("number"))) == ident.split(".")[0])
                refused[f"{lst}.{f}"] += 1
                del item[f]
    except sqlite3.IntegrityError as e:
        print("constraint:", e)
        raise
    finally:
        con.close()
for k, v in sorted(refused.items()):
    print(f"  refused  {k:40s} {v} time(s)")
print(f"{sum(refused.values())} refusals of {len(refused)} kinds; the rest loaded")
