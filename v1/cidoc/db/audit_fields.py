#!/usr/bin/env python3
"""Does every filled column reach the graph?

For each kind of field that holds a value, the field is removed from the
record read out of the database and the graph is built again.  If the graph
does not change, the field is stored but says nothing in the graph.

Usage: python db/audit_fields.py out/excavations.sqlite [report ...]
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from excavation_db import Builder, Exporter, connect  # noqa: E402

EXPECTED_SILENT = {
    ("top", "$comment"): "remark about the record, not about the excavation",
    ("top", "schema_version"): "version of the record format",
    ("document.volume", "place"): "place of publication: no path chosen yet",
    ("document.volume", "published"): "year of the volume: no path chosen yet",
    ("document", "language"): "equals the default (tr), so removing it changes nothing",
    ("figures", "kind"): "equals the default (Resim), so removing it changes nothing",
}
# the link from a row to its figure is also written from the figure's side (figure_depicts)
EXPECTED_SILENT |= {(lst, "figures"): "same link is also stored from the figure's side"
                    for lst in ("features", "strata", "finds", "activities", "records")}


def main(db, reports):
    con = connect(Path(db))
    reports = reports or [r[0] for r in con.execute("SELECT id FROM report ORDER BY id")]
    bad = 0
    for rep in reports:
        rec = Exporter(con, rep).record()
        full = set(Builder(copy.deepcopy(rec)).build())
        fields = [("top", k) for k in rec if not isinstance(rec[k], (list, dict)) and k not in ("base_uri", "shared_uri")]
        fields += [("document", k) for k in rec["document"] if k not in ("id", "title", "authors", "source_file", "pages", "volume")]
        fields += [("document.volume", k) for k in rec["document"].get("volume", {}) if k not in ("id", "title")]
        for lst, items in rec.items():
            if isinstance(items, list):
                fields += [(lst, k) for k in sorted({k for i in items for k in i}) if k not in ("id", "label", "class", "number", "caption", "page", "citation", "assigned", "about", "from", "to", "type", "found_by", "result", "actor")]
        silent, tested = [], 0
        for where, key in fields:
            r = copy.deepcopy(rec)
            if where == "top":
                r.pop(key)
            elif where == "document":
                r["document"].pop(key)
            elif where == "document.volume":
                r["document"]["volume"].pop(key)
            else:
                for i in r[where]:
                    i.pop(key, None)
            tested += 1
            try:
                same = set(Builder(r).build()) == full
            except KeyError:
                same = False            # the builder cannot even work without it
            if same:
                silent.append((where, key))
        unexpected = [s for s in silent if s not in EXPECTED_SILENT]
        bad += len(unexpected)
        print(f"{rep}: {tested} kinds of field tested, {len(silent)} leave no trace in the graph, {len(unexpected)} unexpected")
        for s in silent:
            print(f"    {s[0]}.{s[1]:18s} {EXPECTED_SILENT.get(s, 'UNEXPECTED: stored but lost on the way to the graph')}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
