# Literature review for version 2

Started 2026-09-29. Four searches, run separately. Status of each part is given in its heading.

Reading level of every source: **FULL** (page or paper read), **ABSTRACT**, **SNIPPET** (search result only), **UNREAD**.
A claim that rests on a SNIPPET or UNREAD source must not be used in the thesis until the source is read.

Sources read from PDF files after this review was written are in `reading_notes.md`.

Contents:

1. Platforms that put CIDOC CRM on a database (done)
2. Excavation recording systems (pending)
3. Methods: ontology to tables, generic versus typed tables, coverage (pending)
4. Türkiye (done)
5. What this means for the design (pending, written last)

---

## 1. Platforms that put CIDOC CRM on a database

### Summary

| Platform | Storage | New kind of record needs | Extensions | Stratigraphic relations |
|---|---|---|---|---|
| OpenAtlas | entity table and link table, checked against the ontology | data only, for types. Code for new classes (inferred, not verified) | none, by design | not documented |
| Arches | JSON tiles plus graph metadata, PostgreSQL | configuration | loadable | only if someone models them |
| WissKI | triple store. SQL holds only the website configuration | configuration by an administrator | any OWL ontology | only if modelled |
| ResearchSpace | triple store | configuration | CRM family | not verified |

**Closest to the version 2 proposal: OpenAtlas.** It is relational, fixed, built on the ontology and aimed at non-technical users.
Its link table is a generic statement table checked against domains and ranges that are stored as data.
It is only the generic half of our proposal. It has no typed tables and it excludes every extension.

No platform examined combines typed tables for common excavation patterns, a generic checked statement table,
and the extensions CRMarchaeo, CRMsci, CRMinf and CRMgeo. This is a statement about the systems examined. It is not proof that none exists.

### OpenAtlas (Austrian Academy of Sciences)

- **Tables** (from the published schema, R1): `model.entity` with class code, name, description, and begin and end dates as from/to pairs.
  `model.link` with property code, domain, range, type, description and dates.
  The ontology is stored as data in `model.cidoc_class`, `model.cidoc_class_inheritance`, `model.property`, `model.property_inheritance`, `model.openatlas_class`.
  Also `model.gis`, `web.hierarchy`, `web.reference_system`.
- **Ontology:** CIDOC CRM 7.1.3 per the manual (R2). The older wiki says 7.1.1 (R3).
  Extensions are left out on purpose: "no CRM extensions are used (e.g. CRMsoc or CRMarchaeo)" (R4).
- **Stratigraphy:** a stratigraphic unit is E18 Physical Thing in a hierarchy of place, feature, stratigraphic unit, artifact or human remains.
  No above or below relations and no matrix are documented (R5).
- **Uncertainty:** fuzzy dates through from/to pairs and a comment. No CRMinf. Attribution only through links to sources.
- **Vocabulary:** standard, custom and value types in hierarchies, linkable to external reference systems (R6).
- **Export:** API in Linked Places Format, GeoJSON and Linked Art, with RDF derived from these (R7).
- **Use:** THANADOS (early medieval graves), DANCEM, MEDCEM, FemCareVienna (R8). Mainly cemeteries.
  Projects related to Türkiye are historical, not excavations (R8).
- **Limits stated by its authors:** superclasses used as lowest common denominator (R4). Shortcuts that deviate from the pure ontology (R3, R4).
- **Licence:** GPL-2.0 (R9).

### Arches (Getty Conservation Institute, World Monuments Fund)

- **Tables** (R10): the schema is metadata in GraphModel, Node, NodeGroup, Edge.
  Data sits in ResourceInstance, ResourceXResource and TileModel. A tile is a JSON object per node group. Vocabulary sits in Concept, Relation, Value.
- **Ontology:** no longer bundled. Loaded from a separate repository, extensions listed in a configuration file. Enforcement is optional and applies when a graph is designed (R11).
- **Excavation:** a package for excavations exists with trench, context and special find models on CRM 7.1.3 with CRMarchaeo, CRMgeo, CRMdig (R12).
- **Export:** JSON and CSV per the page read (R13). JSON-LD seen only in a snippet (R14).
- **Use:** mostly inventories. One project uses excavation data (R15). No implementation in Türkiye is listed (R15).
- **Limits:** designing a resource model needs knowledge of the ontology. No usability study found.
- **Licence:** AGPL-3.0 (R16).

### WissKI

- The triple store is the authority. A path builder maps groups and paths to forms (R17, R18).
- Its authors state that complexity "is not reduced, but shifted from the user to the administrator", who needs to know Drupal, the semantic web and the ontology (R17).
- A 2026 project used CRM 7.1.3 with CRMarchaeo (R19, SNIPPET).

### Others, briefly

| System | Note | Read |
|---|---|---|
| ResearchSpace | triple store first, forms and templates aligned to the ontology. AGPL-3.0 (R20) | FULL for the repository |
| Geovistory and OntoME | PostgreSQL. Application profiles select a subset of classes and properties (R21, R22). History oriented | FULL, table structure not verified |
| Nodegoat | user-defined model. Explicit treatment of incomplete, conflicting and ambiguous data (R23) | FULL |
| Heurist | MySQL, user-defined record types. No CRM export found (R24) | SNIPPET, secondary source |
| pyArchInit and s3dgraphy | s3dgraphy reads pyArchInit databases and maps to CRMarchaeo and CRMinf (R26) | SNIPPET |

### Three precedents that must be read in full before any claim of novelty

| Source | Read |
|---|---|
| Crofts, "Implementing the CIDOC CRM with a relational database" (R27) | SNIPPET |
| "A Generic Database Schema for CIDOC-CRM Data Management", CEUR Vol-789 (R28) | SNIPPET |
| Hiebel 2010, relational database with GIS leading to RDF (R29) | SNIPPET |

### Ideas worth borrowing

- OpenAtlas: ontology stored as tables with foreign keys. Directed links only, no inverse properties. Dates and type on the link row. A link checker run after imports. Documented shortcuts.
- Arches: concepts kept apart from data. Extensions loaded through a configuration file.
- WissKI: forms hide the paths. One path expands into several nodes, which is the same idea as fixed rules from table to graph.
- Geovistory and OntoME: application profiles.
- Nodegoat: a taxonomy of uncertainty.

### Gaps a thesis could address

1. Stratigraphic relations as first-class relational structures mapped to CRMarchaeo.
2. Attribution, interpretation and uncertainty at statement level in SQL.
3. A documented, testable, deterministic rule set from SQL to RDF.
4. Usability evidence with non-technical archaeologists. None was found for any platform.
5. No excavation in Türkiye was found on any of these platforms. Absence of evidence only.

### References for part 1

| # | Source | Read |
|---|---|---|
| R1 | https://raw.githubusercontent.com/craws/OpenAtlas/main/install/1_structure.sql | FULL, through a summariser |
| R2 | https://manual.openatlas.eu/model/cidoc_crm.html | FULL |
| R3 | https://redmine.openatlas.eu/projects/uni/wiki/OpenAtlas_and_CIDOC_CRM | FULL |
| R4 | Richards, Eichert, Watzinger 2022, "One Ontology to Rule Them All", https://openatlas.eu/static/documents/2022-05-12_indigo.pdf | FULL |
| R5 | https://manual.openatlas.eu/entity/stratigraphic_unit.html | FULL |
| R6 | https://manual.openatlas.eu/entity/type.html | FULL |
| R7 | https://manual.openatlas.eu/technical/api.html | FULL |
| R8 | https://openatlas.eu/projects | FULL |
| R9 | https://github.com/craws/OpenAtlas | FULL |
| R10 | https://arches.readthedocs.io/en/stable/developing/reference/data-model/ | FULL |
| R11 | https://arches.readthedocs.io/en/stable/administering/ontologies-in-arches/ | FULL |
| R12 | https://github.com/mn-lab-platform/arches-for-ju-excavations | FULL |
| R13 | https://arches.readthedocs.io/en/stable/developing/reference/import-export/ | FULL |
| R14 | https://www.archesproject.org/standards/ | SNIPPET |
| R15 | https://www.archesproject.org/implementations-of-arches/ | FULL |
| R16 | https://github.com/archesproject/arches | FULL |
| R17 | Fichtner, Nasarek, Wiesing 2023, https://doi.org/10.52825/CoRDI.v1i.353 | FULL |
| R18 | https://wiss-ki.eu/node/53 | FULL |
| R19 | https://zenodo.org/records/19697410 | SNIPPET |
| R20 | https://github.com/researchspace/researchspace | FULL |
| R21 | https://github.com/geovistory/toolbox | FULL |
| R22 | Beretta, https://arxiv.org/pdf/2402.07531 | FULL for pages 1 to 20 |
| R23 | https://nodegoat.net/blog.p/82.m/42/how-to-store-uncertain-data-in-nodegoat | FULL |
| R24 | https://en.wikipedia.org/wiki/Heurist | SNIPPET |
| R25 | https://www.chnt.at/wp-content/uploads/eBook_CHNT22_Cuy_etal.pdf | SNIPPET |
| R26 | https://docs.extendedmatrix.org/projects/s3dgraphy/en/latest/ | SNIPPET |
| R27 | http://cidoc.ics.forth.gr/docs/Implementing_the_CIDOC_CRM.pdf | SNIPPET |
| R28 | https://ceur-ws.org/Vol-789/paper13.pdf | SNIPPET |
| R29 | https://cidoc-crm.org/Resources/a-relational-database-structure-and-user-interface-for-the-cidoc-crm-with-gis-integration | SNIPPET |

---

## 2. Excavation recording systems

Reading level in this part also uses **PARTIAL**: a page or a summary of the source was read, not the whole.

### Summary

None of the systems examined uses one column per fact.
All keep a small fixed core of record, category and relation, and move the variation into configuration or into attribute and value rows.
The published cost is always the same: data from different projects stop being comparable unless someone pays for mapping.

| System | Storage | New kind of record | Stratigraphic relations | Mapping to CIDOC CRM | State |
|---|---|---|---|---|---|
| iDAI.field | JSON documents, no fixed schema | configuration by the project | typed: above, below, cuts, cut by, equivalent, before, after, contemporary | none found. Links to vocabularies only | active, Apache-2.0 |
| FAIMS | attribute, key, value rows. Later JSON notebooks | a definition packet per module | not verified | none found | active, Apache-2.0 |
| ARK | items with typed fragments in MySQL | configuration per project | items link freely | not verified | inactive since 2014 per one source |
| Intrasis | user-defined classes and attributes in PostgreSQL | template edited by users | through class relations | mapped afterwards, at high cost | active, proprietary |
| Open Context | PostgreSQL with attribute and value rows | imported by editors | not reported | avoided on purpose | active, GPLv3 |
| OCHRE | items with variable and value statements, XML database | project edits its own taxonomy | containment hierarchies | own ontology, not CIDOC CRM | active, licence not stated |
| tDAR, ADS | archives. No schema imposed | depositor documents each column | none | none | active |
| Heurist | record types and fields stored as data | configuration | not verified | not verified | active, GPLv3 |

### Evidence on cost and use

| Finding | Source |
|---|---|
| The DAI's earlier FileMaker system failed on "inflexibility of the relational data model", incompatible copies and training time | [1] |
| iDAI.field's core fields were derived from usage statistics of about 50 projects | [1] |
| FAIMS made nearly 70 customisations for more than 40 projects. Most needed its own staff and each took weeks. Only two complete datasets were published | [7] |
| FAIMS users could attach vocabulary links to terms and "did not use this term-mapping capability" | [7] |
| Aligning 597 Norwegian Intrasis databases to CIDOC CRM needed analysis of 5,100 path lines | [11], [12] |
| Intrasis templates were revised every year and changed during fieldwork, which makes integration hard | [11] |
| Open Context avoids full CIDOC CRM harmonisation as "more labor and complexity" | [14] |
| ARK was built because archaeologists had to call a technician for every new field | [8] |
| Çatalhöyük in 2004 merged separate specialist Access databases into one back end and kept the familiar Access forms | [22] |
| Features that serve the researcher's own goals get used. Features that serve reuse by others get neglected | [7] |
| People who reuse data most need the collection procedures and the context | [23] |

### Recurring design patterns

| # | Pattern | Used by | Cost |
|---|---|---|---|
| 1 | Core fields plus extension layers | iDAI.field | only the core is comparable |
| 2 | Generic item plus attribute and value rows | ARK, FAIMS, Open Context, OCHRE, Heurist | hard to query in Access or Excel. Weak type checks. Tables must be derived |
| 3 | Category inheritance: a subtype inherits the fields of its parent | iDAI.field, Intrasis | none reported |
| 4 | Relations as typed links, with the matrix derived from them | iDAI.field | none reported |
| 5 | Controlled value lists plus mapping afterwards | Open Context, FAIMS, iDAI.field | skilled editorial labour. Users skip it |

### Gaps

- No independent usability study with non-technical archaeologists was found for any system. All evaluations are by the developers.
- No system examined combines a fixed relational schema, a built-in mapping to CRMarchaeo, and ease of use at the level of Access or Excel.
- Specialist counts and measurements have no shared structure across systems.
- Drift of a project's configuration over time is documented only for Intrasis.

### Not accessed

Sobotkova et al. 2016, "Measure Twice, Cut Once". Kansa, ISAW Papers 7. Schloen and Schloen 2014 and their 2023 book.
Nothing was read for Holly Wright, Julian Richards or Costis Dallas.
The tDAR help pages and the ADS Guides to Good Practice could not be opened.

### References for part 2

| # | Source | Read |
|---|---|---|
| 1 | Cuy et al. 2019, CHNT 22, https://www.chnt.at/wp-content/uploads/eBook_CHNT22_Cuy_etal.pdf | FULL |
| 2 | Field Desktop manual, https://raw.githubusercontent.com/dainst/idai-field/master/desktop/src/manual/manual.en.md | PARTIAL |
| 3 | Roe 2026, comparison of systems, https://joeroe.io/2026/08/03/archaeological-information-systems.html | PARTIAL, a blog |
| 4 | https://github.com/dainst/idai-field | PARTIAL |
| 5 | Ballsun-Stanton et al. 2018, SoftwareX, https://github.com/FAIMS/FAIMS-Mobile-Flexible-open-source-software-for-field-research/blob/master/faims.md | PARTIAL |
| 6 | https://github.com/FAIMS/FAIMS3 | PARTIAL |
| 7 | Ross et al., JCAA, https://doi.org/10.5334/jcaa.96 | PARTIAL |
| 8 | Eve and Hunt 2008, CAA 2007, https://proceedings.caaconference.org/files/2007/09_Eve_Hunt_CAA2007.pdf | FULL |
| 9 | https://en.wikipedia.org/wiki/Archaeological_Recording_Kit | PARTIAL, secondary |
| 10 | https://www.intrasis.com/what-is-intrasis/ | PARTIAL |
| 11 | Katsianis et al., Internet Archaeology 64, https://doi.org/10.11141/ia.64.12 | PARTIAL |
| 12 | Ore 2022, https://doi.org/10.5281/zenodo.7108712 | ABSTRACT |
| 13 | https://www.intrasis.com/ | PARTIAL |
| 14 | Kansa and Kansa, Internet Archaeology 71, https://doi.org/10.11141/ia.71.3 | PARTIAL |
| 15 | Kansa, ICHIM 2007, https://www.archimuse.com/ichim07/papers/kansa/kansa.html | SNIPPET |
| 16 | https://github.com/ekansa/open-context-py | SNIPPET |
| 17 | Prosser and Schloen, "Unlocking Legacy Data", https://www.austriaca.at/0xc1aa5576_0x003bca70.pdf | pages 39 to 50. Year not verified |
| 18 | https://voices.uchicago.edu/ochre/ontology/ | PARTIAL |
| 19 | https://tdar-arch.atlassian.net/wiki/spaces/TDAR/pages/557210/Getting+Familiar+with+tDAR | PARTIAL |
| 20 | https://archaeologydataservice.ac.uk/help-guidance/instructions-for-depositors/files-and-metadata/ | PARTIAL |
| 21 | https://github.com/HeuristNetwork/heurist | PARTIAL |
| 22 | Ridge and May 2004, http://www.catalhoyuk.com/archive_reports/2004/ar04_32.html | PARTIAL |
| 23 | Faniel et al. 2013, https://www.oclc.org/research/publications/2013/context-archaeological-data-reuse.html | SNIPPET |
| 24 | Faniel et al. 2018, https://doi.org/10.1017/aap.2018.2 | ABSTRACT |
| 25 | Huggett 2018, https://doi.org/10.1017/aap.2018.1 | SNIPPET |
| 26 | Huvila et al. 2022, https://kula.uvic.ca/index.php/kula/article/view/221 | SNIPPET |

---

## 3. Methods

Reading level in this part also uses **FULL\***: the full text was fetched but read only through an automated summary. Treat details with care.

Blocked during this search: Springer, HAL, MDPI, PMC, OpenAlex.

### Summary

| Idea in the version 2 proposal | State in the literature | Reuse or open |
|---|---|---|
| Generic statement table checked against the ontology | Done by OpenAtlas and by Jannaschk et al. 2011 | reuse |
| Typed tables beside a generic table | Wilkinson 2006 describes exactly this for RDF storage | reuse and cite |
| Export from SQL to RDF by declarative mapping | W3C R2RML, 2012. Ontop is mature and used in archaeology | reuse |
| SQL first, CIDOC CRM afterwards, for excavations | Done by the Norwegian ADED project on 597 databases | established practice |
| One fixed path per fact | Draft patterns only. No ratified excavation profile | partly open |
| A written, repeatable procedure from the ontology to typed tables | not found | open |
| A measured coverage figure for any schema built on the ontology | not found | open |
| A language model that fills a fixed relational schema in archaeology | not found | open |

### 3.1 Relational implementations of CIDOC CRM

| Source | What it says | Read |
|---|---|---|
| Jannaschk et al. 2011 [1] | Generic schema of five tables: entity, entity attribute, relationship, relationship attribute, role. The authors say it is "not useful for data-intensive science", cannot express complex cardinality, and does not yet handle the class hierarchy | FULL |
| OpenAtlas [2] | Essentially two tables. The ontology is parsed into the database. Inverse properties are dropped | FULL\* |
| Hiebel 2010 [4] | Relational structure with GIS | ABSTRACT |
| "Implementing the CIDOC CRM with a relational database" [6] | Exists. Authors and year not verified | SNIPPET |

Existing relational systems for the ontology are almost all generic. The typed layer is what would set version 2 apart.

### 3.2 Deriving tables from an ontology

| Source | What it says | Read |
|---|---|---|
| Hornung and May 2013 [7] | Classes become tables, functional properties become columns, many-to-many properties become link tables. A property can be single-valued on one class and multi-valued on another, so the derivation needs reasoning | FULL, first half |
| Vysniauskas and Nemuraite 2009 [8] | One table per class, subclass as a one-to-one relation, constraints in metadata tables | FULL, partial |

**Consequence:** CIDOC CRM has almost no cardinality rules and has deep multiple inheritance.
The decision whether a property is a column or a link table cannot come from the ontology.
It must come from the written procedure and be recorded as a human decision.

### 3.3 Mapping standards and tools

| Tool | Status | Use with CIDOC CRM or archaeology | Read |
|---|---|---|---|
| R2RML [10] | W3C Recommendation, 27 September 2012 | basis of Ontop mappings | FULL\* |
| Direct Mapping [10] | W3C, no customisation | not suitable for CRM paths | through [10] |
| RML [11] | community specification, not a Recommendation | none verified | SNIPPET |
| Ontop [12], [13] | mature, open source, answers SPARQL from SQL | ArSol, MASA, SEAD | SNIPPET and FULL\* |
| X3ML and 3M [18] | FORTH, used in ARIADNEplus | expects XML input, not SQL | SNIPPET |

Katsianis et al. [15] rate mapping tools in archaeology as prototypes with "rapid development and little consolidation".

### 3.4 Projects that went from SQL to CIDOC CRM

| Project | What they did | What they report | Read |
|---|---|---|---|
| ADED, Norway [15], [19], [20] | 597 Intrasis databases into PostgreSQL with spatial support | Path table of 5,100 lines. Normalisation took less than a month of manual work. Classes mapped to CRM classes, **almost all subclasses mapped to types** | FULL and ABSTRACT |
| MASA, France [15], [21] | OpenRefine, vocabulary server, Ontop, SHACL, GraphDB | A deliberately small generic model | FULL and ABSTRACT |
| Hiebel, Austria [22], [23] | Spreadsheets into PostgreSQL, then mapping tools | "Intensive effort in data structuring and cleaning". No figures | ABSTRACT and FULL\* |
| SEAD, Sweden [16] | Ontop over an existing database | no paper found | FULL\* |

### 3.5 Generic rows against typed tables

| Source | What it says | Read |
|---|---|---|
| Dinu and Nadkarni 2007 [25] | Generic rows fit sparse data with many attributes, and many classes with few instances. Mixed designs are recommended. The simple schema is paid for with complex metadata | ABSTRACT |
| Wilkinson 2006 [26] | Property tables "augment but do not replace the triple store". Gain: better query planning. Cost: "some loss in flexibility" | FULL, first pages |
| Abadi et al. 2007 [27] | Property tables suffer from empty cells, multi-valued attributes, and unions across tables | FULL\* |
| Karwin, SQL Antipatterns [28] | Lists generic rows as an antipattern | SNIPPET |

### 3.6 Application profiles and patterns

| Source | What it says | Read |
|---|---|---|
| Katsianis et al. 2023 [15] | The ARIADNEplus group looked for an excavation profile. Result: draft patterns, rated as early prototypes. No ratified profile | FULL |
| Bruseker et al. 2025 [30] | Method of reference data models: models, collections, fields. The Swiss infrastructure has 14 models and 279 fields. Motive: the ontology allows several valid paths for one fact | FULL\* |
| Linked Art 1.0 [31] | Subset of CRM 7.1.3 for museums. No excavation coverage | FULL\* |

### 3.7 Measuring coverage

| Source | What it says | Read |
|---|---|---|
| Brewster et al. 2004 [32] | Fit between an ontology and a domain, measured on a corpus | SNIPPET |
| Brank et al. [33] | Four families of evaluation: gold standard, application, data-driven, human | SNIPPET |
| Monfardini et al. 2023 [34] | Of 63 engineers, 92.1 percent use competency questions for scope and 82.5 percent for evaluation. Guidance is limited | FULL, partial |

No source was found that gives a sample size for a claim of schema coverage.

Calculation made for this review, not taken from the literature:

| Claim | Needs |
|---|---|
| At least 95 percent of cases succeed, with 95 percent confidence | zero failures in 59 independent cases |
| Coverage is 95 percent, within 2 points either way | about 456 statements |

Statements inside one report are not independent of each other. Sampling must be by report and by site.

### 3.8 Language models with a fixed ontology, 2023 to 2026

| Source | What it says | Read |
|---|---|---|
| Hariri 2025 [37] | Three conditions: unguided, full ontology, curated subset. The curated subset with examples was best and reduced invented content, but may "omit low-frequency concepts" | FULL |
| Hariri, Jean, Baron 2025 [36] | Read from the PDF. See `reading_notes.md` | FULL |
| ASOS-CRM [38] | Retrieval of candidate classes per column, then checking each candidate triple against domain and range. Paper read from the PDF. See `reading_notes.md` | FULL |
| Marketakis et al. 2026 [39] | Models generate X3ML mappings. Average accuracy 0.53. Argues for explicit mappings over direct generation of RDF | FULL, partial |
| Schimmenti et al. 2025 [41] | F1 of 0.96 to 0.99 for metadata, 0.7 to 0.8 for entities | ABSTRACT |
| Boukhers et al. 2026 [42] | 637 archaeological records, 86 percent of slots linked | ABSTRACT |

Constraining the model improves precision in all of these.
"The model fills values only" is stricter than any of them and was not found published for archaeology.

### References for part 3

| # | Source |
|---|---|
| 1 | Jannaschk, Rathje, Thalheim, Förster, "A Generic Database Schema for CIDOC-CRM Data Management", CEUR Vol-789, https://ceur-ws.org/Vol-789/paper13.pdf |
| 2 | OpenAtlas manual, https://manual.openatlas.eu/model/cidoc_crm.html |
| 3 | OpenAtlas, Heritage 3(4), https://doi.org/10.3390/heritage3040077 (authors not verified) |
| 4 | Hiebel 2010, https://cidoc-crm.org/Resources/a-relational-database-structure-and-user-interface-for-the-cidoc-crm-with-gis-integration |
| 5 | Arches, https://cidoc-crm.org/Resources/arches |
| 6 | https://www.researchgate.net/publication/260363113_Implementing_the_CIDOC_CRM_with_a_relational_database (not verified) |
| 7 | Hornung and May, OWLED 2013, https://ceur-ws.org/Vol-1080/owled2013_3.pdf |
| 8 | Vysniauskas and Nemuraite, https://isd.ktu.lt/it2009/material/Proceedings/OCM/OCM_1.pdf |
| 9 | OWLMap, https://www.researchgate.net/publication/311394567 |
| 10 | R2RML, https://www.w3.org/TR/r2rml/ |
| 11 | Iglesias-Molina et al., ISWC 2023, https://doi.org/10.1007/978-3-031-47243-5_9 |
| 12 | Calvanese et al. 2017, https://doi.org/10.3233/SW-160217 |
| 13 | Xiao et al. 2019, https://doi.org/10.1162/dint_a_00011 |
| 14 | Marlet et al., CAA 2015, https://hal.science/halshs-01321014 |
| 15 | Katsianis et al. 2023, Internet Archaeology 64, https://doi.org/10.11141/ia.64.12 |
| 16 | https://github.com/humlab-sead/sead-vkg |
| 17 | Lefrançois et al. 2017, https://doi.org/10.1007/978-3-319-58068-5_3 |
| 18 | Marketakis et al. 2017, https://doi.org/10.1007/s00799-016-0179-1 |
| 19 | Matsumoto and Uleberg 2021, https://doi.org/10.11141/ia.58.29 |
| 20 | Ore 2022, https://doi.org/10.5281/zenodo.7108712 |
| 21 | Hivert, Marlet, Markhoff 2026, https://doi.org/10.5281/zenodo.19452803 |
| 22 | Hiebel 2022, https://doi.org/10.5281/zenodo.7108589 |
| 23 | Hiebel et al. 2023, https://doi.org/10.11141/ia.64.8 |
| 24 | https://github.com/wxwilcke/pakbon-ld |
| 25 | Dinu and Nadkarni 2007, https://doi.org/10.1016/j.ijmedinf.2006.09.023 |
| 26 | Wilkinson, HPL-2006-140, https://www.hpl.hp.com/techreports/2006/HPL-2006-140.html |
| 27 | Abadi et al., VLDB 2007, https://www.vldb.org/conf/2007/papers/research/p411-abadi.pdf |
| 28 | Karwin, https://pragprog.com/titles/bksqla/sql-antipatterns/ |
| 29 | ARIADNEplus workshop report, https://ariadne-infrastructure.eu/wp-content/uploads/2022/09/Ariadneplus_deliverable_ExcavationModellingWorkshop_report_v1.pdf |
| 30 | Bruseker et al. 2025, https://doi.org/10.5334/johd.282 |
| 31 | https://linked.art/model/ |
| 32 | Brewster et al., https://aclanthology.org/L04-1476/ |
| 33 | https://www.semanticscholar.org/paper/c15e3ad08e22705bacdd8aa102765cbd5a7ff62e |
| 34 | Monfardini et al. 2023, https://doi.org/10.1007/978-3-031-47262-6_3 |
| 35 | https://en.wikipedia.org/wiki/Rule_of_three_(statistics) |
| 36 | Hariri, Jean, Baron, https://doi.org/10.1007/978-3-032-02049-9_6 |
| 37 | Hariri, https://ceur-ws.org/Vol-4099/ER25_DC_hariri.pdf |
| 38 | https://github.com/lias-laboratory/asos-crm |
| 39 | https://users.ics.forth.gr/~tzitzik/publications/Tzitzikas-2026-MappingSETN.pdf |
| 40 | https://doi.org/10.1145/3748522.3779763 |
| 41 | https://arxiv.org/abs/2511.10354 |
| 42 | https://arxiv.org/abs/2608.23263 |

---

## 4. Türkiye

### Summary

The gap is real for excavation data standards. The sentence "there is nothing in Türkiye" is wrong as worded.
Version 1 missed a Turkish PhD thesis, several Turkish articles, a Ministry portal of 2025,
and a clause in the directive that already requires digital submission "for a database to be created".

### Publications missed in version 1

| Source | What it adds | Read |
|---|---|---|
| Atalan Çayırezmez, N. (2023), *Türkiye'de Dijital Arkeolojik Veri Yönetimi*, PhD, Ankara Üniversitesi | The most direct source for the thesis topic. Policy level. See `reading_notes.md` | chapters 1 (part), 5.1, 6, 7 read from the PDF |
| Sahar, İ. (2025), "Arkeolojik Kazı ve Yüzey Araştırması Çalışmalarında Dijital Arkeoloji Uygulamaları: Türkiye'de Yöntemsel Gelişmeler", MASROP E-Dergi 19.2, 17-34 | Author works in the Ministry's excavations department. Says storage, backup, archiving and sharing are problematic and standard protocols are needed. Describes the new portal | FULL for the relevant sections |
| Özgüner, N. P. (2021), "Arkeolojide Dijitalleşme ve Türkiye'de Arkeoloji Eğitimi", TARE 1, 117-142 | Digital courses exist but are not systematic across departments | ABSTRACT |
| İşler, V. and Özgüner, N. P. (eds) (2022), *Arkeolojide Bilişim Teknolojileri* | Turkish textbook with a data management section | UNREAD |
| Özbal, R. and Arslan, A., "Arkeolojik Araştırmaların Veri Paylaşımıyla Desteklenmesi", TAG-Türkiye proceedings | Says digitisation of excavation data has had too little attention. Year not verified | SNIPPET |
| Dişli, M. and Tonta, Y. (2023), "Veri Olarak Kültürel Miras Koleksiyonları", Türk Kütüphaneciliği 37(3), 191-214 | 26 interviews. No Turkish cultural institution offers collections in machine-actionable form | ABSTRACT |
| Atalan Çayırezmez, Çit and Wright (2025), Internet Archaeology 67 | Reports are submitted to the Ministry on CD or external hard drive | summary only |
| Akçay, T. (2024), *Dijital Arkeoloji Stratejisi*; Atakuman et al. (2024), *Arkeolojide Çok Disiplinli Yaklaşımlar* | Cited by Sahar 2025 | UNREAD |

### National systems

| System | Holds | Public | Standard |
|---|---|---|---|
| MUES | Movable objects in museums. An excavation module was "in progress" in 2021 | no | none published |
| TUES | About 10,000 protected areas and 100,000 monuments and buildings. Registration data | web GIS | not verified |
| Kazı ve Araştırma Yönetim Portali, kazilar.kultur.gov.tr, 2025 | Permits, documents, process, GIS | no, login only | data model not verified |
| TAY Project | Settlements with bibliography, online since 1998 | yes | no excavation records |
| BIAA digital repository | Archive of a British institute | yes | FAIR, controlled vocabularies |
| Koç University digital collections | Over 210,000 digitised items | yes | archival images, not structured data |
| iDAI.field | Excavation recording tool, first developed with Pergamon. Turkish interface | open source | see part 2 |

### Legal basis

Verified in the text unless stated otherwise.

| Text | Article | Content |
|---|---|---|
| Law 2863 | 41 | All movable finds go to a state museum at the end of each season |
| Law 2863 | 43 | Publication right belongs to those who direct the excavation. A scientific report is due each season. If season reports are not published within two years and final reports within five, the right passes to the Ministry |
| Regulation | 9(ı), 9(j) | Finds are delivered by inventory. Report within three months with a photograph of each inventoried find and plans |
| Regulation | 11 | Publication rights belong to the directors |
| Directive, 2024 copy | 9(1)(çç) | "Oluşturulacak veri tabanında yer almak üzere, araştırma çalışmalarına ilişkin tüm bilgi, belge, fotoğraf, çizim ve diğer tüm dokümanlar ... dijital ortama aktarılarak Genel Müdürlüğe gönderilir." |
| Directive, 2024 copy | 12(1)(f) | Failure to send these is grounds for not renewing the permit |
| Directive, 2024 copy | 9(1)(ss) | A project website or social media account needs Ministry permission |
| Directive, 2024 copy | 12(4) | Transfer to a new director covers protection and legal obligations only |

Limits of this reading:

- Only articles 41 and 43 of the law were read. Ownership of documentation was not looked for in the rest of the law.
- The directive mentions the excavation archive several times and never defines its content, format or custody.
- No clause on handing over documentation was found. This was a keyword search of the main text. The annexes were not checked.
- The approval date and number of the 2024 directive come from a summary and are not verified.

### Named projects

| Project | System | Openness |
|---|---|---|
| Çatalhöyük | Central SQL Server database since 2004, replacing spreadsheets on personal computers (SNIPPET) | Online database. Zooarchaeology on Open Context and Zenodo |
| Kaymakçı | Fully born-digital recording (Roosevelt et al. 2015) | not verified |
| Gordion | Digital Gordion, custom MySQL | not verified |
| Pergamon | iDAI.field, datasets in the DAI repository | licence not verified |
| Troy | Research data community at Tübingen | not verified |
| Kerkenes | Archive site with reports | not verified |

ARIADNE has entries for 71 projects in Türkiye, per Internet Archaeology 58.

### Standards and networks

- No Turkish institution or excavation was found that implements CIDOC CRM or CRMarchaeo.
- ARIADNEplus: the only institution in Türkiye is the BIAA, an associate partner. It is a British institute.
- SEADDA: Türkiye takes part. Management committee members are Nurdan Atalan Çayırezmez and Eray Dökü.

### The thesis claims against the evidence

| Claim | Verdict | Basis |
|---|---|---|
| Only narrative reports are shared, data stays with teams | supported | Internet Archaeology 58, section 2 |
| Excel and Access dominate | no source found | Only one anecdote from Çatalhöyük before 2004 |
| No national standard or tool | partly | No data standard or guideline. A rule, a planned database and a portal exist |
| Poor handover between directors | gap in the rules only | No study of actual data loss found |
| Almost all archaeologists are non-technical | overstated | Training is uneven. One university opened a digital archaeology option in 2019 |
| Sharing data brings citations | shown in other fields | Piwowar and Vision 2013: 9 percent more citations. No study found for archaeology |

### Suggested wording for the thesis

"Türkiye has national inventory systems for museum objects (MUES) and immovable heritage (TUES), a site inventory (TAY),
and since 2025 a Ministry portal for excavation permits and reporting. The directive requires digital submission of documentation,
but no published data model, metadata standard, controlled vocabulary or archiving guideline defines what excavation data must contain
or how it is kept and handed over. Project databases remain isolated."

### To do

1. Obtain and read the 2023 PhD thesis of Atalan Çayırezmez.
2. Present the Excel and handover claims as the thesis's own evidence or as hypotheses. A short survey of excavation teams would supply the evidence.
3. Soften the claim about non-technical archaeologists to uneven and non-systematic digital training.
4. Read the whole of Law 2863 for ownership of documentation.

### References for part 4

| Source | Link |
|---|---|
| Arbuckle et al. 2014, PLoS ONE 9(6): e99845 | https://opencontext.org/about/bibliography |
| ARIADNEplus associate partners | https://ariadne-infrastructure.eu/associate-partners/ |
| Atalan Çayırezmez, Hacıgüzeller, Kalaycı 2021, Internet Archaeology 58 | https://doi.org/10.11141/ia.58.20 |
| Atalan Çayırezmez, Çit, Wright 2025, Internet Archaeology 67 | https://doi.org/10.11141/ia.67.1 |
| BIAA digital repository | https://digitalrepository.biaa.ac.uk/projects |
| Çatalhöyük database | https://www.catalhoyuk.com/research/database |
| Colavizza et al. 2020 | https://doi.org/10.1371/journal.pone.0230416 |
| Digital Gordion | https://www.penn.museum/sites/gordion/archaeology/digital-gordion/ |
| Dişli and Tonta 2023 | https://doi.org/10.24146/tk.1317445 |
| Huggett 2018 | https://doi.org/10.1017/aap.2018.1 |
| iDAI.field | https://github.com/dainst/idai-field |
| İşler and Özgüner 2022 | https://turkarkeolojienstitusu.org/yayinlar/arkeolojide-bilisim-teknolojileri/ |
| Kazı portal | https://kazilar.kultur.gov.tr/ |
| Koç University digital collections | https://librarydigitalcollections.ku.edu.tr/en/ |
| Law 2863 | https://www.mevzuat.gov.tr/mevzuatmetin/1.5.2863.pdf |
| Marwick and Pilaar Birch 2018 | https://faculty.washington.edu/bmarwick/PDFs/Marwick-and-Pilaar-Birch-2018-Data-Citation-AAP.pdf |
| METU digital archaeology option | https://www.tuba.gov.tr/tr/duyurular/dijital-arkeoloji-yuksek-lisans-opsiyonu |
| MUES | https://mues.ktb.gov.tr/ |
| Özbal and Arslan | https://www.academia.edu/11468633/ |
| Özgüner 2021 | https://doi.org/10.54930/TARE.2021.4 |
| Piwowar and Vision 2013 | https://doi.org/10.7717/peerj.175 |
| Roosevelt et al. 2015 | https://www.tandfonline.com/doi/full/10.1179/2042458215Y.0000000004 |
| Sahar 2025 | https://dergipark.org.tr/tr/download/article-file/5277140 |
| SEADDA CA18128 | https://www.cost.eu/actions/CA18128/ |
| TAY | http://tayproject.org/veritab.html |
| TUES | https://tues.kultur.gov.tr/tues/ |
| Directive, 2024 copy | https://aritweb.org/wp-content/uploads/2024/10/2024-Yonerge-Tr.pdf |
| Regulation | https://mevzuat.gov.tr/File/GeneratePdf?mevzuatNo=5318&mevzuatTur=KurumVeKurulusYonetmeligi&mevzuatTertip=5 |

---

## 5. What this means for the design

### 5.1 Where the proposal stands

The building blocks of version 2 exist. The combination does not, as far as these four searches reached.

| Part of the proposal | Status |
|---|---|
| Ontology stored as tables, links checked against it | exists: OpenAtlas |
| Generic statement table | exists: OpenAtlas, Jannaschk et al. |
| Typed tables beside the generic one | exists as an architecture: Wilkinson. Not found for this ontology |
| Mapping from SQL to RDF as executable data | exists: R2RML |
| SQL first for excavations | exists: ADED |
| Fixed structure for the extensions CRMarchaeo, CRMsci, CRMinf | not found |
| Procedure from ontology to typed tables | not found |
| Measured coverage | not found |
| Model fills a fixed relational schema | not found for archaeology |
| Independent usability test with non-technical archaeologists | not found for any system |
| Anything of this in Türkiye | not found |

### 5.2 Every field system chose flexibility. Version 2 chooses the opposite

All field recording systems examined let each project configure its own fields.
They report the same cost: data from different projects cannot be compared without expensive mapping afterwards.
Version 2 accepts some rigidity at entry in order to get comparable data without that mapping.

The risk is documented too. The German institute's earlier relational system failed on inflexibility.
The residue table and templates stored as data are the answer to that, and they must work from the first day.

### 5.3 Design decisions the literature supports

| Decision | Taken from |
|---|---|
| Store the ontology as tables and check links by foreign key | OpenAtlas |
| Store directed links only. Generate inverse properties at export | OpenAtlas |
| Map classes to tables and **subclasses to types** | ADED |
| Typed stratigraphic relations: above, below, cuts, cut by, equivalent to, before, after, contemporary with | iDAI.field |
| A subtype inherits the fields of its parent | iDAI.field, Intrasis |
| Write the mapping in R2RML so that the program executes it | W3C |
| Validate the output with SHACL | MASA, and version 1 |
| Record every column-or-link decision as a human decision in the procedure | Hornung and May |
| Give excavators generated views, because generic rows are hard to query in Access or Excel | documented cost of generic rows |
| Check our core fields against the iDAI.field core list, which came from about 50 projects | Cuy et al. 2019 |

### 5.4 One decision to revisit

In version 1 the user decided that compatibility with ARIADNE and Linked Art is not a goal.
The draft patterns of the ARIADNE group and the reference data models of Bruseker et al. exist to solve the same problem as version 2: one path per fact.
Taking paths from them where they exist costs little and answers the question "why these paths".
It would also raise the score on the working group's questions, where version 1 reached 2 or 3 of 17.
This is the user's decision.

### 5.5 Objections to expect, and the answer available today

| Objection | Answer | Strength of the answer |
|---|---|---|
| Why not use OpenAtlas or Arches? | OpenAtlas excludes the extensions and has no stratigraphic relations. Arches needs an administrator who knows the ontology | good |
| The 95 percent has no precedent | True. It needs a sampling plan and a confidence interval | weak until the plan is written |
| The ontology has no cardinalities, so the procedure contains human choices | True. Record each choice and its reason | moderate |
| Fixed schemas drift. ADED's templates changed every year | Templates are data in version 2. Only the core is fixed | untested |
| The statement table is generic rows, with weak checks | It is checked against domain and range. It holds only the residue | moderate |
| The residue may hold the rare facts that matter most | True. Report what is in the residue, not only how much | must be built into the test |
| Three papers from one volume do not generalise | True. Version 1 was exploration | weak until more papers and real data |
| Typed tables have empty cells and multi-valued properties | True. Known cost, accepted | moderate |

### 5.6 Reading list, in order

| # | Source | Why |
|---|---|---|
| 1 | Atalan Çayırezmez 2023, PhD thesis | Read in part on 2026-09-29. Chapters 2 to 4 remain |
| 2 | Katsianis et al. 2023, Internet Archaeology 64 | The state of excavation data integration in Europe, and the ADED and MASA experience |
| 3 | ARIADNEplus workshop report, annex B | The draft patterns for excavations |
| 4 | Bruseker et al. 2025 | Method of reference data models |
| 5 | Jannaschk et al. 2011 | The generic relational schema and its stated limits |
| 6 | Wilkinson 2006 | The hybrid architecture |
| 7 | Cuy et al. 2019 | iDAI.field, used in Türkiye |
| 8 | Ross et al., FAIMS | What non-technical users did and did not use |
| 9 | Sahar 2025 | The Ministry's view |
| 10 | Hariri 2025, and the two Springer chapters | Both chapters read on 2026-09-29 |
| 11 | "Implementing the CIDOC CRM with a relational database" | Must be read before any claim of novelty |

### 5.7 Limits of this review

- Four searches in one day. Not a systematic review.
- Many sources were read only as abstract, snippet or automated summary. The reading level is marked for each.
- Several publishers blocked access.
- Statements that something was "not found" mean not found by these searches.
- Some sources are dated 2026 and could not be cross-checked.
