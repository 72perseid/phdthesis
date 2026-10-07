# CIDOC CRM pipeline for KST excavation reports

Turns one Kazı Sonuçları Toplantısı paper into a CIDOC CRM knowledge graph.
Two worked examples from 45. KST Cilt 1:

| Paper | Record | Graph |
| --- | --- | --- |
| 14 Seleukeia Sidera 2024 (classical city, theatre, bulk finds) | `data/seleukeia_sidera_2024.json` (format v1) | 1,802 triples |
| 18 Yumuktepe 2024 (mound, stratigraphy, radiocarbon, archaeobotany) | `data/yumuktepe_2024.json` (format v2) | 3,667 triples |

    ../../.venv/bin/python build_graph.py data/yumuktepe_2024.json -o out/yumuktepe_2024.ttl
    ../../.venv/bin/python run_queries.py out/yumuktepe_2024.ttl          # SHACL + 13 competency questions
    ../../.venv/bin/python visualize_graph.py out/yumuktepe_2024.ttl      # interactive HTML

| File | Role |
| --- | --- |
| `schema.md` | the JSON record format (v2) and its CRM mapping; what changed from v1 |
| `extraction_prompt.md` | rules for extracting a record from a paper (for a person or an LLM) |
| `data/*.json` | one record per paper, with page provenance |
| `build_graph.py` | JSON → Turtle (rdflib); CRM 7.1 + CRMarchaeo 2.1.1 + CRMsci 3.2 |
| `shapes.ttl` | 16 SHACL rules; violations fail, warnings report what the paper omits |
| `queries/cq01..cq13_*.rq` | competency questions in SPARQL, none tied to a specific paper |
| `run_queries.py` | validates with pySHACL and prints query results |
| `visualize_graph.py` | pyvis network; `--focus`, `--helpers`, `--inline-css` |
| `out/` | generated graphs, HTML views, validation and query logs |

Dependencies: `rdflib`, `pyshacl`, `pyvis` (installed in `../../.venv`); `pdftotext` (poppler) for the text step.

## Relational step (db/)

The record is now loaded into a SQLite database first, and the graph is generated from the tables.

| File | Purpose |
| --- | --- |
| `db/schema.sql` | 30 data tables; classes restricted to the official ontology terms; references enforced |
| `db/crm_mapping.csv` | one fixed CRM path for every content column (116) |
| `db/excavation_db.py` | `init`, `load`, `graph`, `check` (compares the graph through the tables with the direct one) |
| `db/test_constraints.py` | twelve wrong entries the database must refuse |
| `db/questions/*.sql` | cross-site questions in SQL |
| `ontology/*.rdf` | CIDOC CRM 7.1.3, CRMarchaeo 2.1.1, CRMsci 3.2 as downloaded from cidoc-crm.org |
| `out/pilot_overview.html` | one-page overview of the chain report, tables, graph, answer |

```
python db/excavation_db.py init  out/excavations.sqlite
python db/excavation_db.py load  out/excavations.sqlite data/seleukeia_sidera_2024.json data/yumuktepe_2024.json
python db/excavation_db.py check out/excavations.sqlite yumuktepe-2024 data/yumuktepe_2024.json
python db/excavation_db.py graph out/excavations.sqlite yumuktepe-2024 -o out/yumuktepe_2024.ttl
python db/test_constraints.py out/excavations.sqlite
```

Result on both papers: 0 statements lost, 0 added. Not covered yet: coordinates and geometry (CRMgeo RDFS was not downloadable), the PC property classes, a general statements table for content without a column.

## Third paper (Sinekkaya)

`out/third_paper_test.md` reports what the database refused and what changed.
`db/audit_fields.py` checks that every stored field reaches the graph.
`tools/baseline_refusals.py` lists everything a record holds that the tables cannot.
