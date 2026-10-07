#!/usr/bin/env python3
"""
run_queries.py - Validate a report graph against shapes.ttl (SHACL) and run
the competency questions in queries/*.rq against it.

Usage
  python run_queries.py out/seleukeia_sidera_2024.ttl            # validate + all queries
  python run_queries.py out/seleukeia_sidera_2024.ttl -q cq1     # one query
  python run_queries.py out/seleukeia_sidera_2024.ttl --no-validate
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import logging

from rdflib import Graph

# rdflib cannot turn BC xsd:dateTime values into Python datetimes and logs a
# traceback for each; the literals are valid XSD and are kept as written.
logging.getLogger("rdflib.term").setLevel(logging.ERROR)

HERE = Path(__file__).resolve().parent


def validate(data: Graph) -> bool:
    from pyshacl import validate as shacl_validate
    shapes = Graph().parse(HERE / "shapes.ttl")
    conforms, report, text = shacl_validate(data, shacl_graph=shapes, inference="none",
                                            abort_on_first=False, allow_warnings=True)
    SH = "http://www.w3.org/ns/shacl#"
    from rdflib import URIRef
    from rdflib.namespace import RDF, RDFS
    warnings, violations = [], []
    for r in report.subjects(RDF.type, URIRef(SH + "ValidationResult")):
        sev = str(report.value(r, URIRef(SH + "resultSeverity")))
        node = report.value(r, URIRef(SH + "focusNode"))
        msg = str(report.value(r, URIRef(SH + "resultMessage")))
        label = data.value(node, RDFS.label) or node
        (warnings if sev.endswith("Warning") else violations).append((msg, str(label)))
    print(f"SHACL: {'conforms' if conforms else 'VIOLATIONS'} ({len(violations)} violations, {len(warnings)} warnings)")
    for kind, rows in (("violation", violations), ("warning", warnings)):
        for msg, label in sorted(rows):
            print(f"  {kind}: {msg} -> {label}")
    return conforms


def short(g: Graph, value) -> str:
    try:
        s = value.n3(g.namespace_manager)
    except Exception:
        s = str(value)
    if s.startswith("<") and s.endswith(">"):
        s = s[1:-1].rsplit("/", 1)[-1]
    return re.sub(r"@[a-z]{2}$", "", s.replace('"', "").split("^^")[0])


def run_query(g: Graph, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    title = next((ln[1:].strip() for ln in text.splitlines() if ln.startswith("#")), path.stem)
    print(f"\n=== {path.stem}: {title}")
    res = g.query(text)
    cols = [str(v) for v in res.vars]
    rows = [[short(g, r[i]) if r[i] is not None else "" for i in range(len(cols))] for r in res]
    widths = [max(len(c), *(len(row[i]) for row in rows)) if rows else len(c) for i, c in enumerate(cols)]
    widths = [min(w, 60) for w in widths]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*[c[:w] for c, w in zip(cols, widths)]))
    print(fmt.format(*["-" * w for w in widths]))
    for row in rows:
        print(fmt.format(*[cell[:w] for cell, w in zip(row, widths)]))
    print(f"({len(rows)} rows)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("graph", type=Path)
    ap.add_argument("-q", "--query", help="run only this query (file stem in queries/)")
    ap.add_argument("--no-validate", action="store_true")
    args = ap.parse_args(argv)

    g = Graph().parse(args.graph)
    print(f"{args.graph}: {len(g)} triples")
    ok = True
    if not args.no_validate:
        ok = validate(g)
    files = sorted((HERE / "queries").glob("*.rq"))
    if args.query:
        files = [f for f in files if f.stem == args.query]
    for f in files:
        run_query(g, f)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
