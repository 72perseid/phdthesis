# Version 2 design, draft 1

Written on 2026-09-29. Sections 1 to 11 are the draft. Section 4.8 on periods was added at the user's request.
Sections 4.4 and 4.6 were revised after reading CRMinf and CRMgeo.

**Section 12 reports the first build and its test, done the same day.** Where the build differs from the draft, section 12 is right.

Read first: `../v1/REPORT.md` for what failed, `literature_review.md` part 5 and `reading_notes.md` section 8 for the sources.

## 1. The design in one page

**Aim.** One database structure that is fixed, that follows the CIDOC CRM family module by module,
and that holds at least 95 percent of what an excavation records in typed form.
The remainder is stored too, in the same structure, without a new table.

**Idea.** The structure has five layers. Only the top layers change, and they are rows of data.

| Layer | Contents | Who changes it | How often |
|---|---|---|---|
| 1 Ontology | Classes, properties, domains and ranges, read from the official files | nobody. Replaced when a new ontology version is adopted | years |
| 2 Core and modules | 37 tables. Each module follows one part of the ontology | the maintainer, by a counted and published change | target: never after the freeze |
| 3 Declared lists | Relation types, attribute definitions, code lists, each with its path | the maintainer | per release |
| 4 Templates | Sheets for specialists: lithics, fauna, ceramics, coins. Rows that point at declared attributes | the maintainer, later a community | cheap and frequent |
| 5 Own additions | The excavator's own codes, own attributes, and statements with any ontology property | the excavator | any time |

**What the excavator sees.** Sheets that look like a spreadsheet. They are generated from layers 3 and 4.
The excavator never sees a class or a property.

**What a language model does.** It fills values into sheets. It does not choose classes.
For layer 5 it may propose a property, and the database checks the proposal against domain and range.

**What is new against version 1.**

| Version 1 | Version 2 |
|---|---|
| Structure derived from papers | Structure derived from the ontology by a written procedure. Papers are test material |
| The report is the root | The dataset of an excavation is the root. A report is one source |
| A new kind of fact needs a new column | A new kind of fact is a row in layer 3, 4 or 5 |
| Four mechanisms for who says so and how sure | One table, `claim` |
| Mapping in program code | Mapping is data that the program executes |
| Types as free text | Code lists, with the excavator's own code beside the standard code |
| No geometry, calendar years only | Geometry table. Time with a stated scale |

## 2. Sources of the design

| Decision | Taken from |
|---|---|
| Ontology stored as tables, links checked against it | OpenAtlas |
| Only one direction of a property is stored | OpenAtlas |
| Classes become tables, subclasses become types | ADED |
| Fixed types plus generic stores | SIKB0102 |
| Every row has its own identifier, the identifier from the source system, and a remark | SIKB0102 |
| Required only where a value exists in the worst case | SIKB0102 |
| Own code beside standard code. Codes carry version, date and state | SIKB0102 |
| A link layer between a find and its context | SIKB0102 |
| Typed stratigraphic relations | iDAI.field, SIKB0102, version 1 |
| Typed tables beside generic rows | Wilkinson 2006 |
| Subclass rows extend the parent row one to one | Vysniauskas and Nemuraite 2009 |
| Every column-or-link choice is a recorded human decision | Hornung and May 2013 |
| Mapping as executable data | W3C R2RML |
| Output checked by rules | SHACL, as in version 1 and MASA |
| Dataset description, licence, embargo | PARTHENOS guide to FAIR |
| A period is a definition by a named source, with place and years | PeriodO |
| Domain and range check on proposed statements | OpenAtlas. Hariri, Jean and Baron for the use with a model |

## 3. The translation procedure

This is the part that was not found in the literature. It turns one ontology module into tables.
The ontology has almost no cardinality rules, so several steps are human decisions. Each decision is logged.

| Step | Rule |
|---|---|
| P1 | Take the classes and properties of the module from the official file. Nothing is added from memory |
| P2 | A class becomes a table when its instances have their own identity in an excavation archive and carry properties that the parent does not have |
| P3 | Any other class becomes a value in the `class` column of the parent's table |
| P4 | A subclass table extends the parent row one to one. It never repeats the parent's columns |
| P5 | A property with at most one value per subject in practice becomes a column |
| P6 | A property with several values becomes a declared relation type or a declared attribute. It does not become a table |
| P7 | A property whose value is a conclusion is never a column. It goes through `assertion` or `dating`, with a claim |
| P8 | An event that exists only to connect two things is not stored. The mapping creates it in the graph. It is stored only when something is said about the event itself |
| P9 | One direction of each property is stored. The inverse is generated |
| P10 | A column is required only if a value exists in the worst case |
| P11 | Every column, relation type and attribute has exactly one path. If the ontology allows several, one is chosen and the reason is logged |
| P12 | Every decision from P2 to P11 is a row in a decision log: item, choice, reason, date, person |

P5 and P6 need knowledge of practice. That knowledge comes from precedents, not from the pilot papers:
the field lists of SIKB0102 and the core list of iDAI.field. Both came from many real projects.

Size of the task, counted from the files used in version 1:

| Ontology | Classes | Properties, both directions | File in hand |
|---|---|---|---|
| CIDOC CRM 7.1.3 | 76 | 309 | yes |
| CRMarchaeo 2.1.1 | 10 | 59 | yes |
| CRMsci 3.2 | 28 | 77 | yes |
| CRMinf 1.2.1, April 2026 | 14 | 52 | yes |
| CRMgeo 2.0.1, May 2026 | 9 | 33 | yes |
| Total | 137 | 530 | |

Both new files are marked stable. Both are built on CIDOC CRM 7.1.3, and CRMinf on CRMsci 3.2. These are the versions already in use, so the five files fit together.
About half of the properties are inverse directions, which rule P9 does not store.

## 4. Modules and tables

Eleven modules, 37 tables. The count is part of the draft and can change until the freeze.

| # | Module | Follows | Tables | Count |
|---|---|---|---|---|
| A | Ontology and mapping | the official files | `ontology_source`, `ontology_term`, `ontology_subclass`, `mapping` | 4 |
| B | Dataset | FAIR principles, E73 Information Object | `dataset`, `dataset_actor` | 2 |
| C | Core | CIDOC CRM | `entity`, `identifier`, `actor`, `place`, `period`, `activity`, `participation`, `thing`, `dimension` | 9 |
| D | Vocabulary | E55 Type | `code_list`, `code`, `own_code` | 3 |
| E | Sources and documentation | E31 Document, E73, E36 Visual Item | `source`, `passage`, `media`, `about` | 4 |
| F | Excavation | CRMarchaeo | `context`, `find_context` | 2 |
| G | Science | CRMsci | `sample`, `analysis` | 2 |
| H | Claims | CRMinf, E13 Attribute Assignment | `claim`, `claim_basis`, `assertion`, `dating` | 4 |
| I | Space | CRMgeo | `geometry` | 1 |
| J | Generic stores | any property of the loaded ontologies | `relation_type`, `relation`, `attribute_def`, `attribute_value` | 4 |
| K | Templates | none. They arrange declared attributes | `template`, `template_field` | 2 |

A module can be left out. An excavation with no laboratory work has empty tables in module G and nothing else changes.

### 4.1 Core

| Table | Holds | Main classes | Notes |
|---|---|---|---|
| `entity` | One row for every identifiable thing in any table | all | Identifier, class, dataset, identifier in the source system, label, remark. Generic stores point here, so every link has a real foreign key |
| `identifier` | Any number or code that names an entity | E42 Identifier | Inventory number, permit number, ORCID, find number. With a type |
| `actor` | People and groups | E21 Person, E74 Group | No e-mail addresses |
| `place` | Sites, areas, trenches, squares, rooms, museums | E53 Place | With `part_of` |
| `period` | Period definitions: name, years, place, and who defined it | E4 Period | Linked to PeriodO. See section 4.8 |
| `activity` | Seasons, excavation of a unit, sampling, analysis, survey, restoration, looting | E7 Activity and its subclasses, A9, A1, S2, S4 | Class column. Place, time, continued activity |
| `participation` | Who took part in what role | P14 carried out by, with a role | |
| `thing` | Finds, assemblages, boxes, samples, structures | E18 Physical Thing and its subclasses | Class column, type code, material, `part_of`, `kept_in` |
| `dimension` | Counts and measurements of anything | E54 Dimension | Kind, value, unit, measured by which activity |

Two points answer failures of version 1.

- **Counts.** A row of a count table is an assemblage in `thing` with a count in `dimension`.
  The printed total is a second dimension on the parent assemblage. A total that does not match its parts is found by a query.
- **Time.** Every pair of years carries a scale: CE, BP or calibrated BP. Ages before present are stored as printed.

### 4.2 Excavation

| Item | Form | Ontology |
|---|---|---|
| `context` | Table. Deposit, interface or feature, by class | A2 Stratigraphic Volume Unit, A3 Stratigraphic Interface, A8 Stratigraphic Unit, E26 Physical Feature |
| `find_context` | Table. Which thing was found in which context, place or activity, how it was collected, where exactly | A7 Embedding, AP17 to AP19, S19 Encounter Event |
| Stratigraphic relations | Declared relation types | AP11 has physical relation to, AP13 has stratigraphic relation to, with a type |
| Time relations between contexts | Declared relation types | AP22 to AP28 |
| What an excavation unit removed | Declared relation type | AP5 removed part or all of |
| Amount dug | `dimension` on the activity | AP1 produced, S11 Amount of Matter |
| How a context formed | Not stored. Created by the mapping | A4 Stratigraphic Genesis, AP7 produced |
| Grouping of contexts into a phase or a building | Declared relation type, with a claim | A6 Group Declaration Event |

The relation list starts from the union of three lists: version 1 with 8 types, iDAI.field with 8, SIKB0102 with 12.

The ontology has no class for a trench, a plane or a grid square. They are places with a type.
This keeps the module independent of one field method, which the Dutch standard is not.

### 4.3 Science

| Item | Form | Ontology |
|---|---|---|
| `sample` | Table. Extends a row of `thing`. Taken from what, by which activity, amount | S13 Sample, S2 Sample Taking |
| `analysis` | Table. Extends a row of `activity`. Method, laboratory, laboratory code | S4 Single Observation, S21 Measurement, S6 Data Evaluation |
| Which samples an analysis used | Declared relation type | |
| Numeric results | `dimension`, measured by the analysis | |
| Dates from a laboratory | `dating`, based on the analysis | |
| Identifications, such as a species | `assertion`, based on the analysis | |

### 4.4 Claims

This module replaces the four mechanisms of version 1. It was checked against the file of CRMinf 1.2.1.

| Table | Holds | CRMinf |
|---|---|---|
| `claim` | The act of stating something: who, when, of which kind, by which method, with which belief, in which source and passage | I1 Argumentation, I2 Belief |
| `claim_basis` | What the claim rests on: another claim, a source, an analysis, a comparison | J1 used as premise, J7 is based on evidence from |
| `assertion` | The content of a conclusion: subject, property from a declared list, value | I17 One-Proposition Set, with J30 has domain, J31 has range, J32 has property type |
| `dating` | The content of a date: subject, what was dated, period or years with scale | the same, with a time value |

The draft had these four tables before the file was read. The file confirms them and adds four columns.

| Column | Values | CRMinf | Why |
|---|---|---|---|
| `claim.kind` | inferred, adopted from a source, recorded | I5 Inference Making, I7 Belief Adoption, E13 | "We think" and "Smith 2019 says, and we follow" are different acts |
| `claim.belief` | true, probable, possible, false | J5 holds to be | Replaces the certainty of the draft. The value false is new |
| `claim.method` | code list: stratigraphic position, typological comparison, laboratory measurement, calibration, and others | I3 Inference Logic, J3 applied | The ontology asks how the conclusion was drawn |
| `claim_basis.basis_claim` | another row of `claim` | J1 used as premise | A premise is a belief. So a claim can rest on a claim |

Three consequences.

1. **Negative statements have a place.** The ontology allows a belief with the value false, and names negation as a use.
   "The bedrock was not reached" is an assertion with the belief false. Decision 6 is closed.
2. **Chains of claims can be followed.** The phase of a building rests on the date of a layer, which rests on a laboratory date.
   A query can list everything that falls when the laboratory date is revised. The ontology names this as the purpose of the class.
3. **A citation is a claim of its own kind.** Version 1 stored cited literature as a link. Here it is a claim adopted from a source.

Rules:

1. `assertion` and `dating` rows always have a claim. Rows of `relation`, `attribute_value` and `find_context` may have one.
2. A row without a claim is a record of the team that owns the dataset.
3. Only a claim with the belief true is written to the graph as a plain fact. This is the rule of version 1, now in one place.
4. Two claims about the same subject and property may disagree. Both are kept. A query lists the disagreements.
5. `dating` names what was dated: the making, the use, the deposition, the death of an organism, the formation of a layer.
   The mapping picks the path from that. This removes the error of version 1, where every date ran through a production event.

What is left out of CRMinf on purpose: the classes for the provenance and the intended meaning of a text, I10 and I13 to I16.
They serve the study of written sources. A statement that needs them goes to level 3.

Open:

- The value of a proposition must be an entity in the ontology. A value that is plain text has no direct path. Text values may need a type or a note.
- CRMsci has its own class for inference, S5. CRMinf has I5. One of the two must be chosen for the path, by rule P11.
- The list of belief values is mine. The ontology names true, false and "somewhere in between" and fixes no list.

### 4.5 Generic stores and templates

| Table | Holds | Check at entry |
|---|---|---|
| `relation_type` | Declared relation types, each with module, path, allowed classes on both ends | |
| `relation` | A link between two entities. The property is a declared type, or any property of the loaded ontologies | Both ends must fit the domain and range |
| `attribute_def` | Definition of an attribute: name, class it belongs to, value type, unit, code list, path, owner | |
| `attribute_value` | A value of a defined attribute on an entity | Class of the entity, value type, code list |
| `template` | A sheet, such as lithics by raw material | |
| `template_field` | Which attributes and columns the sheet shows, in which order, with which label in Turkish and English | |

Every statement in the database is at one of four levels.

| Level | Where it is stored | Comparable across excavations |
|---|---|---|
| 1 Typed | A column, or a declared relation type | yes |
| 2 Template | A declared attribute | yes |
| 3 Own | An attribute defined by the excavator, a raw ontology property, or an own code without a standard code | within the excavation only |
| 4 Text | A remark | no |

A level 3 item that many excavations use is a candidate for level 2 in the next release.
Promotion changes one row. The stored values do not move.

**Lesson from the Dutch evaluation.** Depots could not read what excavators had put into the generic stores.
So a rule is added: every row of levels 2 and 3 must appear in a generated sheet and in the graph.
A test removes each row in turn and checks that both outputs change, as `audit_fields.py` did in version 1.

### 4.6 Dataset, vocabulary, sources, space

| Module | Points |
|---|---|
| Dataset | Title, excavation, season, rights holder, licence, access level, embargo date, version, checksum, method, abbreviations, known gaps. The embargo can follow the publication right of the director |
| Vocabulary | A code has list, label in Turkish and English, parent, link to a published vocabulary, version, date, state. `own_code` keeps the excavator's term and points at a standard code when one fits |
| Sources | A report, a notebook, a publication. `passage` is a page, figure or table in a source. `media` is a drawing, photograph, model or file. `about` links a passage or a media item to the entities it shows or describes |
| Space | See below |

**Space, checked against the file of CRMgeo 2.0.1.**

The ontology separates two things. The real extent of a trench or a wall is one thing. The coordinates that somebody measured are another, and they only approximate the first.

| Item | Form | CRMgeo |
|---|---|---|
| The real place of a trench, a context, a find | the row in `place`, `context` or `thing` | SP2 Phenomenal Place |
| Measured coordinates | a row of `geometry`: entity, coordinates as text in WKT, coordinate system, precision, measured by which activity | SP6 Declarative Place, Q10 place is defined by, Q11 approximates place |
| Coordinate system | code on the geometry row | SP4 Spatial Coordinate Reference System, Q9 |
| A local site grid | a coordinate system of the excavator's own, with the fixed point it hangs on | SP4, Q8 is fixed on |
| Time scale: CE, BP, calibrated BP | the scale column beside every pair of years | SP11 Temporal Reference System, Q19 has reference event |
| Years as stated | the year columns | SP10 Declarative Time-Span, Q13 approximates time |
| The measuring itself | a row of `activity` | S23 Position Determination, from CRMsci |

Consequences:

1. One entity can have several geometries: from two surveys, or in two coordinate systems. The ontology says that a transformed geometry is a new one. So `geometry` has many rows per entity.
2. The time scale of the draft is confirmed. It is a class of the ontology, and years before present get a proper path.
3. Local grids are the hard case. Most excavations measure in their own grid. The grid needs a definition, and the link to a national system is often missing. How a local grid is stored is open.
4. Elevation has no class of its own. It is the third coordinate, or a dimension.

No table was added by either file. The count stays at 37.

### 4.7 Mapping

`mapping` has one row per column: table, column, class condition, path.
`relation_type` and `attribute_def` carry their own path.
The exporter reads these rows and nothing else. A column without a row fails the build.
The draft named R2RML as the format. The build uses a small path notation of its own. See section 12.4.

### 4.8 Periods and PeriodO

PeriodO is a public gazetteer of period definitions, at https://perio.do. Its principle is that a period name has no fixed meaning.
"Neolithic" means different years in different regions and for different authors.
So each entry is one definition: a name, the source that defined it, the place it covers, and the years.
Each entry has a permanent address.

I downloaded the dataset on 2026-09-29. A copy is in `papers/periodo_dataset_2026-09-29.json`.

| Measure | Value |
|---|---|
| Sources of definitions | 501 |
| Period definitions | 9,446 |
| Definitions whose coverage lists Türkiye | 505 |
| Definitions with a name in Turkish | 41, mostly Ottoman rulers |
| Start or end given as one year | 17,672 |
| Start or end given as an earliest and a latest year | 1,213 |

Names used in the three pilot papers, looked up by exact English name among the 505:

| Name | Definitions found | Spread of the start |
|---|---|---|
| Neolithic | 3 | 8550 BC to 7000 BC |
| Chalcolithic | 3 | 6400 BC to 4500 BC |
| Early Bronze Age | 3 | 3100 BC to 2500 BC |
| Iron Age | 4 | not compared |
| Hellenistic | 3 | 332 BC to 323 BC |
| Byzantine | 1 | AD 330 |
| Roman, Late Roman, Ottoman, Medieval | 0 | |
| Epipalaeolithic, Upper and Middle Palaeolithic | 0 | |

The search was by exact name only. Entries with a longer name, such as "Roman Imperial", were not counted.
Most of the sources found are written for the Levant, Mesopotamia or the Aegean, and list Türkiye among other countries.

**Rules for the design.**

1. A row of `period` is a definition and not a name. It holds the name as written, the language, the place covered, the source, and four years with a scale: earliest and latest start, earliest and latest end.
2. A row can carry the address of a PeriodO entry, with the kind of match: same, close, wider or narrower.
3. The excavator's own definition is always kept. The PeriodO entry is added beside it. This is the same rule as for own codes.
4. `dating` points at a row of `period`. It never holds a bare period name.
5. A period without years is allowed. Many reports name a period and give no years. The link to PeriodO then supplies years for searching, marked as borrowed.
6. Two excavations that use one name with different years stay different rows. A query shows the difference.

Rule 1 changes version 1, where a period had two years and a flag for approximate.

**What this gives the thesis.** The coverage for Türkiye is thin, above all for the Palaeolithic and in Turkish.
The period definitions collected from excavation reports could be submitted to PeriodO as a new source.
That is a contribution that does not depend on anyone adopting the database.

**Not yet checked:** whether a Turkish institution has already submitted definitions under names I did not search,
and which periodisation the Ministry systems use.

## 5. How the failures of version 1 are answered

| # | Failure in version 1 | Answer in this draft | Tested |
|---|---|---|---|
| 1 | Every new kind of fact needs a new column | Levels 2 and 3 | no |
| 2 | The mapping lives in program code | Module A and section 4.7 | no |
| 3 | Four mechanisms for a claim | Module H | no |
| 4 | Counts stored as finds | Assemblage plus `dimension` | no |
| 5 | The report is the root | `dataset` is the root. Identifiers are global, so actors and places can be matched across datasets | no |
| 6 | Types are free text | Module D | no |
| 7 | No geometry, calendar years only | Module I and the time scale | no |
| | Dating through a production event | Rule 5 in section 4.4 | no |
| | Placeholder web addresses | Identifier of the dataset plus identifier of the row. Needs an institution to give the dataset identifier | no |

## 6. First check on paper

I placed the nine kinds of refusal from the third paper into the draft by hand.
This is not a blind test. I know that paper, and the draft was written after it.

| Refused in version 1 | Times | Lands in | Level |
|---|---|---|---|
| A cell of the count table belongs to a total | 63 | `thing.part_of` and `dimension` | 1 |
| Hedged or alternative period on a find | 20 | `dating` with `claim` | 1 |
| Hedged date on a feature | 1 | `dating` with `claim` | 1 |
| Hedged date on a layer | 1 | `dating` with `claim` | 1 |
| Literature cited for an activity | 2 | `about` with `passage` | 1 |
| Amount dug | 1 | `dimension` on the activity | 1 |
| Looting created a deposit | 1 | `relation` with a declared type | 1 |
| Bibliography | 1 | `source` | 1 |
| Model and plan made on site | 1 | `media` | 1 |

The items that version 1 lost, from section 7 of its report:

| Lost in version 1 | Lands in | Level |
|---|---|---|
| Ages before present | time scale | 1 |
| Sieve mesh size | attribute on the activity | 2, if a template for sieving declares it |
| A layer that was not reached | `assertion` with the belief false | 1 |
| A condition on part of an assemblage | sub-assemblage in `thing` with `part_of` | 1 |
| Skeletal element, local animal name | code list, and `own_code` for the local name | 1 or 3 |
| Coordinates and elevations | `geometry` | 1 |
| Same person in two papers | `identifier`, and a relation of type same as | 1 |

All seven now have a place. The negative statement got one after CRMinf was read. None of this is tested.

## 7. What the 95 percent counts

Two different claims are possible. They need different evidence.

| Claim | Unit | Measure | Evidence needed |
|---|---|---|---|
| Coverage | statement | Share of statements at level 1 or 2 | About 456 statements for a margin of 2 points. Sampled across reports and sites, since statements in one report depend on each other |
| Stability | report or excavation | Share of cases that load with no change to layer 2 | Zero failures in 59 independent cases, for 95 percent with 95 percent confidence |

The volume has 26 papers. Three are used. The other 23 cannot carry the stability claim alone.
Two more volumes would be enough in number. They would still be reports and not excavation archives.

Rules for counting:

1. A statement is one subject, one property and one value, as a reader finds it in the source.
2. The list of statements is made before loading, by someone who has not seen the tables. A second reader codes a sample, and agreement is reported.
3. A statement counts as covered only if it comes back out in a sheet and in the graph.
4. Level 1 is reported apart from level 2. The contents of levels 3 and 4 are listed, not only counted.
5. Changes are counted in five classes: table or column, relation type, attribute or template, code, own addition. Only the first class breaks the claim of a fixed structure.

| Set | Papers | Use |
|---|---|---|
| Development | 13, 14, 18 | Already seen. For building and debugging |
| Test | the other 23 of the volume | Untouched until the freeze |
| Real data | the advisor's Access tables. These are survey records, not trench records | After the pilot. Kept local. Nothing published without the advisor's agreement |

**What the survey records can and cannot test.** Stated by the user on 2026-09-29.

| Part of the design | Tested by the survey records |
|---|---|
| Core, vocabulary, dataset, sources | yes |
| Space | yes, and harder than in the papers. A survey is mostly places and coordinates |
| Finds, counts, templates | yes. Surface collections are counts by unit |
| Claims, dating, periods | yes. Surface material is dated by comparison only |
| Science | only if samples were taken |
| Excavation: contexts, stratigraphic relations, find in context | no |
| Local site grid | probably not. Surveys usually work in a national or global system |

None of the five ontology files has a class for a survey. I searched all scope notes.
So a survey has no module of its own. It must fit into the core with types, relation types and templates.
This makes the survey records a test of the central claim: a new kind of fieldwork is held without a new table.

Real trench records are still missing. They need a second source.

## 8. Experiments, in order

Each is small. None needs the whole system.

| # | Experiment | Question it answers | Output |
|---|---|---|---|
| 1 | Run the procedure on CRMarchaeo by hand: 10 classes, 59 properties | Does the procedure give module F, or something else? How many decisions are human? | Decision log |
| 2 | Same for CRMsci: 28 classes, 77 properties | Does one procedure work for a second module? | Decision log |
| 3 | Write modules C, F, H and J as SQL. Load the Yumuktepe oven with its two conflicting dates, one chain of claims, and one negative statement | Does one claim mechanism hold a conflict, a chain and a negation? | Small database and one query |
| 4 | Load the Sinekkaya lithics table through a template | Do counts work as assemblages? Are the three sums found by a query? | Template rows and one query |
| 5 | Generate one sheet from a template, fill it, load it back | Can the excavator's view be generated? | One spreadsheet file |
| 6 | Write the mapping of module F in R2RML and run it with a standard tool | Is the mapping executable as data? | Graph of one paper |
| 7 | Compare the core columns with the required fields of SIKB0102 | Which worst case fields are we missing? | Table |
| 8 | Match every period of the three papers to PeriodO, by name, place and years | How many get a match, and of which kind? | Table of matches |

Freeze after experiment 8. Then the test set.

## 9. Decisions for you

| # | Decision | My recommendation |
|---|---|---|
| 1 | Take paths from the ARIADNE draft patterns and the Swiss reference models where they exist | Yes. It answers "why this path" and costs little. You decided against compatibility as a goal in version 1. This is about borrowing paths, not about compatibility |
| 2 | Which claim the thesis makes: coverage, stability, or both | Coverage as the main claim. Stability as a reported count with its confidence, without the figure of 95 |
| 3 | One file per excavation, or one central store | One file per excavation, with global identifiers, so that files can be merged later |
| 4 | Whether level 2 counts toward the 95 percent | Yes, reported apart from level 1 |
| 5 | How much of CRMinf to use | Closed by the file: argumentation, belief, one-proposition set, inference logic. The classes for text interpretation are left out |
| 6 | Negative statements | Closed by the file: belief with the value false. To be tried in experiment 3 |
| 8 | How a local site grid is stored | Open. I have no recommendation yet |
| 9 | Scope in the thesis title: excavation data, or fieldwork data with excavation and survey | Fieldwork data. The state's own inventory form, Ek-21, is one form for both |
| 10 | Where real trench records come from | Open. The user's contacts |
| 7 | Submit the period definitions from Türkiye to PeriodO | Yes, after the matching in experiment 8 |

## 10. Risks

| Risk | Why it is real | What limits it |
|---|---|---|
| The design drifts into generic rows | Relations and attributes are rows, as in OpenAtlas and the Dutch stores | Levels are measured. Level 1 is reported alone |
| Generic rows are hard to use in Access or Excel | Documented in the literature | Generated sheets. This must work from the first day |
| The procedure is not repeatable | Steps P5 to P7 are human decisions | The decision log. A second person repeats experiment 1 |
| I know the three papers | Section 6 is not blind | The test set |
| Rigidity drives users away | The earlier system of the German institute failed on it | Level 3 lets the excavator add without asking anyone |
| Level 3 is never looked at | The Dutch evaluation | The rule in section 4.5 |
| Required fields change later | The Dutch evaluation | Rule P10, fixed at the freeze |
| 37 tables is already too many | No evidence either way | Experiment 5 shows what the user really sees |

## 11. Limits of this draft

- The draft was written before any table existed. The build is in section 12.
- All class and property numbers were checked against the five files. For CRMinf and CRMgeo I read the scope notes of the terms used here, not the whole specification documents.
- The core list of iDAI.field is named as a source and was not yet compared.
- The Dutch schema studied is version 3.1.0 of 2015.
- The forms of the directive, Ek-21, Ek-11/a and Ek-4/a, are not in hand. The draft was not checked against them.
- The MUES standards paper of 2017 is missing.

## 12. Build 1 and the first test

Built and tested on 2026-09-29. Everything can be repeated with one command: `./run_pilot.sh`.
The full output of the last run is in `out/pilot_run.txt`.

### 12.1 What exists

| File | Contents |
|---|---|
| `db/schema.sql` | The 37 tables and the fixed checks |
| `db/seed/mapping.csv` | 233 rows. Every column with its meaning and its path |
| `db/seed/relation_types.csv` | 46 declared relation types |
| `db/seed/attributes.csv` | 25 declared attributes |
| `db/seed/code_lists.csv`, `codes.csv` | 27 code lists, 255 codes, labels in Turkish and English |
| `db/seed/templates.csv` | 5 templates: finds, contexts, survey units, two count tables |
| `db/fieldwork_db.py` | The program. Nine commands |
| `db/test_db.py` | The tests |
| `db/from_v1.py` | Test tool that loads the three records of version 1 |
| `db/pilot_links.csv` | 22 links from own terms to standard codes |
| `ontology/` | Six official files |
| `out/fieldwork.sqlite` | The database with the three papers. Open it with DB Browser for SQLite |
| `out/view/` | 24 tables as the excavator would see them. Open them in Excel or LibreOffice |
| `out/*.ttl` | Three graphs |

The program holds no class and no property of its own. It reads them from the tables.

| Command | What it does |
|---|---|
| `init` | Creates the tables, reads the ontology files, loads the lists, generates 68 checks from the mapping |
| `check` | Tests the mapping, the stored data and the graph. Lists dates that contradict each other and totals that do not add up |
| `graph` | Writes the graph and tests every statement against domain and range |
| `audit` | Hides each column in turn and tests that the graph changes |
| `levels` | Counts stored statements by level |
| `sheet` | Writes an empty sheet for a template |
| `fill` | Loads a filled sheet. An unknown term becomes an own code. An unknown column becomes an own attribute |
| `view` | Writes everything stored as wide tables |
| `link` | Puts standard codes beside own codes |

### 12.2 Results

| Test | Result |
|---|---|
| Wrong entries refused | 42 of 42 |
| Cases that must work | 19 of 19 |
| Statements of the three records tried | 2,164 |
| Refused by the database | 0 |
| Without a place | 0 |
| Problems in the mapping | 0 |
| Problems in the stored data | 0 |
| Statements in the graph against the ontology | 0 |
| Columns with data that do not reach the graph | 0 of 100. Five of them only steer other paths |

| Paper | Rows of entities | Statements in the graph | Own codes made |
|---|---|---|---|
| Seleukeia Sidera | 126 | 2,343 | 47 |
| Yumuktepe | 210 | 4,461 | 88 |
| Sinekkaya | 179 | 5,165 | 81 |

Stored statements by level:

| Paper | Typed | Template | Own | Text | Typed and template |
|---|---|---|---|---|---|
| Seleukeia Sidera | 88.9 % | 0.1 % | 7.8 % | 3.2 % | 89.0 % |
| Yumuktepe | 84.3 % | 0.3 % | 10.4 % | 5.1 % | 84.5 % |
| Sinekkaya | 84.3 % | 0.0 % | 8.6 % | 7.0 % | 84.3 % |

After 22 links from own terms to standard codes:

| Paper | Typed and template |
|---|---|
| Seleukeia Sidera | 90.6 % |
| Yumuktepe | 86.4 % |
| Sinekkaya | 85.1 % |

**The 95 percent is not reached.** The distance is between 4 and 11 points.

What the database found again, without being told:

| Paper | Finding |
|---|---|
| Yumuktepe | The BX oven is dated AD 1387 to 1476 by radiocarbon. Two pottery groups from it are dated to the 13th century |
| Sinekkaya | The lithics total is printed as 677. The parts sum to 676 |

### 12.3 What these numbers do not show

1. **The levels count stored rows, not statements of the paper.** Section 7 asks for a list of statements made by a reader before loading. That list does not exist yet. So this is a measure of storage, and not yet of coverage.
2. **The test is not blind.** I built the tables, I wrote the loader, and the records were extracted by me in version 1.
3. **Zero refusals came after repair.** The first load refused 50 statements in two papers and crashed on the third. The changes are in 12.5.
4. **The records are not the papers.** They already lack what version 1 lost.
5. **Page links raise the typed share.** 474 of the stored rows say only on which page something is printed. The real test must report the share with and without them.
6. **No coordinates were in the three records.** The space module was tested only with made-up data.
7. **The template level is almost empty.** Reports do not hold specialist sheets. Only real fieldwork data can test level 2.
8. **No person has used a sheet.**

### 12.4 Where the build differs from the draft

| Draft | Build | Why |
|---|---|---|
| An entity has one class | An entity can have a second class | A wall is a built feature and also a unit of the stratigraphic sequence. The ontology allows this. Without it 11 stratigraphic relations were refused |
| `activity` has a column for the work it continued | A relation type | One season continued five earlier projects. By rule P6 it cannot be a column |
| Years have a scale | Years have a scale and a mark for approximate, on period, activity and dating | The papers say "about" |
| `context` is a table of its own | `context` extends a row of `thing` | In the ontology a stratigraphic unit is a physical thing. Rule P4 |
| Mapping in R2RML | A path notation of its own, run by the program | One node must be shared between several columns. The notation can be translated to R2RML later. Not tried |
| Output checked by SHACL | Every statement checked against domain and range, read from the ontology tables | It needs no rules written by hand. SHACL is still needed for rules such as "every find has a context" |
| Attributes through one path | Two paths | The ontology lets only observable things be observed. A plan for next year is not observable |
| A relation type names one property | It can also name a path on each side | "Formed earlier than" holds between the formation events, not between the layers |
| Stratigraphic relations stored as given | One direction stored | Rule P9. The loader turns "is cut by" around |

Found on the way:

- **The ontology files do not fit together fully.** CRMarchaeo 2.1.1 names the class S4 Observation. CRMsci 3.2 gave the code S4 to another class and calls Observation S27. The program follows the name and reports it at every build.
- **A claim by several people needs a group.** `claim.made_by` holds one actor. The loader makes a group with members. This works, and it is clumsy.
- **Conclusions and records are kept apart by the database.** A relation type marked as a conclusion is refused without a claim. This is the separation of observation and interpretation that the Dutch designers asked for.
- **A count table cuts a whole in two ways,** by row and by column. Rows are parts. Columns are "counted with". Before this the sum check counted everything twice.
- **A person passed as a thing in the first test run.** In the ontology a person is a biological object. The check now sends every actor to the actor table.

### 12.5 Changes that the three papers forced

Counted by the rule of section 7.

| Class of change | Count | What |
|---|---|---|
| Table | 0 | |
| Column | 4 added, 1 removed | second class, approximate on three tables, `continued` removed |
| Path | 8 rows | second path for attributes |
| Relation type | 8 | continued, member, written by, edited by, published by, published at, lies in, counted with |
| Attribute | 1 | planned for the year |
| Code | 2 | project number, figure number |
| Own code, made by the loader | 216 | mostly kinds of things, species, roles, kinds of work |

The table count held. The column list did not. This happened on papers I already knew, so the freeze cannot be declared yet.

### 12.6 The largest lever is vocabulary

Of the 216 own codes, 97 are kinds of things and 42 are species. The lists shipped with the build are short: 35 kinds of things, no species.
The same term was made three times, once per paper: "excavation campaign".

This is not a fault of the tables. It says that code lists are the main work ahead, and that they must come from sources in Türkiye.
Candidates: the terms of the inventory form Ek-21, the museum system, the TAY inventory. None was checked.

### 12.7 Next steps, in order

| # | Step | Needs |
|---|---|---|
| 1 | Open `out/view/` and `out/fieldwork.sqlite`, and tell me what looks wrong | you |
| 2 | A reader lists the statements of one paper from the PDF, before looking at the tables | a second person, best an archaeologist |
| 3 | Load one unseen paper, not through version 1. Count refusals and changes | me |
| 4 | Table names and column names of the survey records | your advisor |
| 5 | Code lists from Turkish sources | you and me |
| 6 | Write the decision log of rule P12 for CRMarchaeo | me |
