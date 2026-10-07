# Version 1 report

Closed on 2026-09-29. Everything in this folder is frozen. New work starts in `../v2/`.

## 1. What version 1 was

Version 1 was exploration. It asked whether the content of Turkish excavation reports can be turned into
CIDOC CRM data, and what kind of structure should sit between the report and the graph.

It used three papers from the 45th Kazı Sonuçları Toplantısı volume as test material.
The papers are a pilot. The thesis is about excavation data in general.

**The main result:** a structure derived from papers breaks on every new paper.
This happened with the JSON format and again with the database. Version 2 must be designed from the ontology.

## 2. The tries, in order

| # | Try | Result | What it taught |
|---|---|---|---|
| 1 | Split the volume into papers | 26 of 26 papers, matches the printed contents | Title detection by font size works. Cover and section headings mislead it |
| 2 | One paper to CIDOC CRM. Seleukeia Sidera, a classical city | 1,802 statements, 8 questions answered | The chain report, record, graph, validation, questions is workable |
| 3 | Same format on a second paper. Yumuktepe, a mound | The builder crashed, dates were invalid, 3 of 8 questions were empty | The format was fitted to paper 1. It needed 4 new lists and about 20 new fields |
| 4 | Discussion: one JSON for all papers | Rejected by the user | Reverse engineering the ontology was proposed. It was not followed until too late |
| 5 | Review of Linked Art | It covers only the moment of discovery | No excavation model to build on |
| 6 | Review of ARIADNE, and test of our graphs against it | 2 of 17 of their questions answered by their paths | Valid CIDOC CRM is not the same as comparable data |
| 7 | Bibliography and synthesis | 66 entries, four candidate problems | Nothing found for Türkiye beyond one 2021 article |
| 8 | Recent work by Hariri and colleagues | A model picks ontology classes for tables | Different approach and different user. Not a rival |
| 9 | Database first, graph second. The user's design | 30 tables, both papers pass through with nothing lost | The database refuses bad data at entry |
| 10 | Third paper on the database. Sinekkaya, a cave | 91 fields of 9 kinds refused | The database was also fitted to the papers |
| 11 | Review of the design failures | Seven failures named | Version 2 should be modular |

## 3. Final state of the three papers

| Check | Seleukeia Sidera | Yumuktepe | Sinekkaya |
|---|---|---|---|
| Paper number in the volume | 14 | 18 | 13 |
| Printed pages | 209 to 224 | 265 to 278 | 197 to 208 |
| Site type | classical city | mound | cave |
| Rows in the database | 329 | 693 | 881 |
| Statements in the graph | 1,802 | 3,667 | 5,028 |
| Lost between record and graph | 0 | 0 | 0 |
| Rule violations, of 18 rules | 0 | 0 | 0 |
| Warnings | 0 | 4 | 2 |
| Our questions answered, of 16 | 8 | 13 | 13 |
| ARIADNE questions by their paths, of 17 | 2 | 2 | 3 |
| ARIADNE questions by our paths, of 17 | 11 | 16 | 10 |
| ARIADNE catalogue fields held, of 19 | 10 | 10 | 10 |
| Rows that carry a free-text note | 19 | 49 | 48 |

The database has 34 tables and 129 columns, each with one CIDOC CRM path.
It knows 114 classes and 445 properties, read from the official files of CIDOC CRM 7.1.3, CRMarchaeo 2.1.1 and CRMsci 3.2.
It refused 12 of 12 deliberately wrong entries.

## 4. Schema changes forced by each paper

| Paper | New lists or tables | New fields |
|---|---|---|
| 1 Seleukeia Sidera | baseline | baseline |
| 2 Yumuktepe | 4 lists | about 20 |
| 3 Sinekkaya | 2 lists, 4 tables | 5 |

The two rows were not counted the same way. Version 2 must count changes by one rule from the start.

## 5. Errors found in the papers

The system found these. No reader was looking for them.

| Paper | Finding |
|---|---|
| Yumuktepe | The BX oven has a radiocarbon range of AD 1387 to 1476. The pottery from its hearth level is dated to the 13th century |
| Sinekkaya | The lithics table does not add up. Cells sum to 676, the printed total is 677, the row totals sum to 678 |
| Sinekkaya | 871 buckets of 10 litres is 8,710 litres. The paper gives 0.871 tonnes |
| Sinekkaya | The text cites a paper as 2025. The bibliography lists it as 2024 |

All are stored as printed.

## 6. Why version 1 fails

| # | Failure | Evidence |
|---|---|---|
| 1 | Every new kind of fact needs a new column | 91 refusals on paper 3 |
| 2 | The mapping to CIDOC CRM lives in program code. The mapping table is documentation only | A field was stored and dropped from the graph without any error |
| 3 | Dating certainty, relation certainty, attribution and interpretation are four mechanisms for one idea, a claim | A fifth variant was added for paper 3 |
| 4 | Counts and measurements are stored as finds | The lithics table became 60 find rows |
| 5 | The report is the root of everything | The same person in two papers is two unrelated rows |
| 6 | Types are free text | Nothing prevents two spellings of one type |
| 7 | No geometry. Time is calendar years only | Ages before present went into notes |

Two modelling errors are also open:

- Dating runs through a production event. That is wrong for bones, seeds and natural stones.
- Placeholder web addresses are used for every entity.

## 7. Still lost in version 1

These are in the papers and ended up in notes or nowhere:

- ages in years before present
- method details such as sieve mesh size
- negative results, such as layers that were not reached
- a condition that applies to part of an assemblage
- skeletal elements and vernacular names of animals
- coordinates and elevations
- matching of people, places and periods across papers

## 8. What the literature review found

Details and sources are in `research/bibliography_and_synthesis.md`.

| Source | What it offers | What it lacks for this thesis |
|---|---|---|
| CIDOC CRM with CRMarchaeo and CRMsci | The vocabulary | It needs a specialist, and it allows several valid paths for one fact |
| Linked Art | A simple profile of the ontology for museums | It models only the discovery of an object |
| ARIADNE | A catalogue of datasets across Europe | It describes datasets, not their content. Its own working group could not agree on one path per fact |
| Hariri and colleagues | A model that maps tables to the ontology | The model chooses the classes. The user must be able to judge them. Base ontology only |
| Turkish context, 2021 article | A description of the situation | No standard, no guideline, no tool |

Not yet read in full: the ARIADNE pattern annex, the full papers of Hariri and colleagues, Marlet 2019, Lien-Talks 2026, Hou 2026.
Not yet searched: literature in Turkish, and existing field recording systems with configurable fields.

## 9. The thesis problem as it stands

Stated by the user during version 1:

- Reports are a distilled account. They hold what the excavator allowed and what was sent to the ministry. The data stays in the excavation's own files.
- Archaeologists who inherit another excavation's data spend a long time understanding it. Sometimes nothing is handed over.
- Almost all archaeologists in Türkiye are non-technical and work in spreadsheets.
- Data should be shared for three reasons. Sharing returns as citations and projects. The data is national heritage. A tool for non-technical users removes the technical obstacle.

Only the third reason can be proven by the thesis itself. The first two need literature and a legal reading.

Working thesis sentence: a relational structure constrained to CIDOC CRM lets excavators share comparable data without knowing the ontology.

## 10. Decisions taken

| Decision | Taken by |
|---|---|
| The papers are a pilot and a demonstration, not the data source | user |
| Compatibility with Linked Art or ARIADNE is not a goal | user |
| Database first, graph generated from it. A model fills values and never chooses classes | user |
| Other researchers on the same question are colleagues | user |
| No published web pages. Outputs are local files | user |
| Hedged statements are never stored as facts | version 1 rule |
| Errors in a paper are stored as printed, with a note | version 1 rule |
| E-mail addresses are not recorded | version 1 rule |

## 11. Decisions still open

- What is the unit of sharing: an excavation, a season, a trench, a dataset?
- Who enters data: the excavator, or a model with a person checking?
- One database file per excavation, or one central store?
- How are hypotheses modelled in the graph?

## 12. Proposal for version 2

Three layers that change at different speeds.

| Layer | Contents | Expected change |
|---|---|---|
| Core | things, people, places, time, events, types, identifiers, part-of links | almost none |
| Modules | stratigraphy, sampling and analysis, claims, sources and documentation, geometry | rare |
| Templates | lithics sheet, fauna sheet, ceramics sheet, coin sheet | constant and cheap |

Rules for version 2:

1. Design the core and the modules from the ontology. Test them with papers.
2. Templates are rows of data. Adding one needs no new table and no new code.
3. The mapping to CIDOC CRM is data that the program executes.
4. There is one mechanism for claims.
5. The excavation is the root. A report is one source among others.
6. Count core changes, module additions and template additions separately.
7. The excavator sees a familiar table. It is generated from the template.

First real data after the pilot: the advisor's Access tables. They are a best case and not typical.

## 13. Limits of the evidence in version 1

- Three papers, all from one volume and one year.
- All three records were extracted by the same reader, who knew the schema.
- No archaeologist has checked the records against the papers.
- No real excavation data has been loaded.
- The 16 questions were written by the same reader who built the model.

## 14. What is in this folder

| Path | Contents |
|---|---|
| `split_papers.py` | Splits a proceedings volume into papers |
| `cidoc/data/` | The three records |
| `cidoc/text/` | Text of the Sinekkaya paper |
| `cidoc/build_graph.py` | Record to graph |
| `cidoc/shapes.ttl` | 18 validation rules |
| `cidoc/queries/` | 16 questions |
| `cidoc/run_queries.py` | Validates and runs the questions |
| `cidoc/visualize_graph.py` | Graph as an interactive page |
| `cidoc/db/` | Database schema, loader, mapping table, tests, three questions in SQL |
| `cidoc/ontology/` | Official ontology files |
| `cidoc/tools/` | Count table parser, Sinekkaya record generator, baseline test |
| `cidoc/ariadne/` | Tests against ARIADNE |
| `cidoc/out/` | Graphs, database, test outputs, pages |
| `cidoc/out/third_paper_test.md` | Full report of the third paper |
| `cidoc/out/pilot_overview.html` | One page that follows one paragraph through all steps |
| `cidoc/schema.md` | The record format |
| `cidoc/extraction_prompt.md` | 20 rules for extraction |
| `research/bibliography_and_synthesis.md` | Literature and its connection to the work |

Outside this folder and shared by all versions: `../kst_paper.pdf`, `../kst_paper_split/`, `../.venv/`.

Also made in version 1, outside the folder: a methodology document and two graph pages published online.
They describe the state after paper 2 and are not updated.

## 15. How to run version 1 again

From `v1/cidoc/`:

```
../../.venv/bin/python db/excavation_db.py init  out/excavations.sqlite
../../.venv/bin/python db/excavation_db.py load  out/excavations.sqlite data/seleukeia_sidera_2024.json data/yumuktepe_2024.json data/sinekkaya_2024.json
../../.venv/bin/python db/excavation_db.py check out/excavations.sqlite sinekkaya-2024 data/sinekkaya_2024.json
../../.venv/bin/python db/excavation_db.py graph out/excavations.sqlite sinekkaya-2024 -o out/sinekkaya_2024.ttl
../../.venv/bin/python run_queries.py out/sinekkaya_2024.ttl
../../.venv/bin/python db/audit_fields.py out/excavations.sqlite
../../.venv/bin/python db/test_constraints.py out/excavations.sqlite
```

All of these were run after the move into this folder and gave the results in section 3.
