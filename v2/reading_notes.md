# Reading notes for version 2

Written 2026-09-29. Sources read from the files in `papers/`.
This file complements `literature_review.md`, which was built from web searches.

| Source | File | What was read |
|---|---|---|
| Atalan Çayırezmez 2023, PhD thesis | `792023.pdf`, 447 pages | Contents, aims and method (1.2 to 1.4), legislation (5.1), all of chapter 6, all of chapter 7, data management plan. Keyword search over the whole text |
| Hariri, Jean, Baron 2025, DEXA | `978-3-032-02049-9.pdf`, printed pages 83 to 97 | In full |
| Hariri, Jean, Baron 2026, DaWaK, ASOS-CRM | `978-3-032-34896-8.pdf`, printed pages 261 to 269 | In full |
| Excavation directive, 2024 copy | `yonerge_2024.pdf`, 32 pages | By keyword. Annex forms are not in the file |
| Atalan Çayırezmez, Hacıgüzeller, Kalaycı 2021 | `ia.58.20.pdf`, 17 pages | In full |

Not read in the thesis: chapters 2, 3 and 4, sections 5.2 to 5.4, annexes 1 to 13.

---

## 1. Atalan Çayırezmez 2023, *Türkiye'de Dijital Arkeolojik Veri Yönetimi*

### What the thesis is

| Point | Content |
|---|---|
| Discipline | Information and records management, Ankara Üniversitesi. Not archaeology |
| Aim | Assess the state of digital archaeological data management in Türkiye and propose a policy and model |
| Problem statement | No national policy and model exists for managing digital archaeological data on a common platform |
| Hypothesis | A comprehensive policy and model should be developed |
| Method | Document analysis and content analysis. No survey, because data collection fell in the pandemic |
| Material | 29 articles of Internet Archaeology 58, Ministry correspondence from the BIAA archive, directives, web sites, 13 excavations of Ankara Üniversitesi from 2019 to 2021 |
| Interviews | A few personal conversations, named in the text. Not a systematic set |
| Scope | Excavations and surveys run by universities. Rescue excavations by museums are left out |

**The thesis states its own limit.** Section 1.4 says that methods of data collection in archaeology,
and the different ways of managing the collected data, could not be treated in detail, because the methods vary and time was limited.
That is the level at which version 2 works.

### What it recommends (chapter 7)

| # | Recommendation |
|---|---|
| 1 | Interoperability between actors |
| 2 | A common metadata standard, for example Qualified Dublin Core |
| 3 | A common terminology, controlled vocabularies, a Turkish thesaurus |
| 4 | Use of an ontology. CIDOC CRM should be translated into Turkish and actors informed |
| 5 | Persistent identifiers for actors, projects and terms |
| 6 | A common data aggregation platform set up by the Ministry |
| 7 | University open archives adapted to hold archaeological data |
| 8 | Trusted data archives |
| 9 | Work on digital rights: licences, embargo, restricted access |
| 10 | Long-term preservation |
| 11 | Awareness and training |
| 12 | Digital skills for archaeologists |
| 13 | Open source software encouraged |
| 14 | Funding. Data management should be a required and budgeted part of an excavation |

All of these are at the level of policy, metadata and infrastructure.
None proposes a structure for the content of excavation data: contexts, finds, samples, relations.
CRMarchaeo is named four times in the whole text, as description.

### Evidence useful for our claims

| Our claim | What the thesis offers | Strength |
|---|---|---|
| Data stays with the team | Eskiyapar director, interview of 20 March 2022: no database or information system. Archive kept at home or in the office. Data on a personal computer, external drives and cloud. 1 to 3 TB per season. A fault in an external disk caused access problems | one case, first hand |
| Data stays with the team | A thesis on Eskiyapar cites images as "Sipahi private archive" | one case |
| Data stays with the team | Of 13 Ankara Üniversitesi excavations, 5 have no web site. One has data on its site, closed | 13 cases |
| Data stays with the team | Of 167 projects in 2017 to 2019, 76 percent of foreign and 43 percent of Turkish projects publish information on a web site | from the 2021 article |
| The state asks for data and does not define it | The Ministry has asked for archive material since the 1990s. In 2001 it announced a database. The medium changed from slides to diskette, CD, DVD and hard disk. The thesis concludes that with no clear statement on formats, no standards and no database, the data cannot be managed | document analysis |
| Reports are an incomplete picture | Özgüner 2015: published survey reports do not match the number of permitted projects. Not every project presents, reports come late, several years are merged into one report | cited, a PhD thesis |
| Handover | Directors change over the life of an excavation. Alacahöyük has had five. A database was commissioned for it in 2014 and nothing is accessible | shows the situation, not a loss |
| No identifiers | Excavations have no stable number. Names differ from year to year in the Ministry lists. From 2021 a project number appears on permits | document analysis |
| Excel and Access dominate | Nothing | none |
| Archaeologists are non-technical | Recommends training. No measurement | none |
| Data is common heritage | Özdoğan 2001, p. 117: the documents of the past should not be the monopoly of any researcher or institution. A scholar has the right to a monopoly only on their own ideas and interpretations | a citable statement by a senior Turkish archaeologist |
| Publication right | It lasts five years from the end of the permit, then passes to the Ministry | as the thesis reads the law |

### Excavation databases in Türkiye described in the thesis

| Project | System | Open | What it shows for our design |
|---|---|---|---|
| Çatalhöyük | Central database, more than 1,000 related tables, 9.3 million rows. Everything is linked through the unit number | Reports and images yes, database no | Specialisms needed their own databases. One source concludes that a general database for management and analytical databases for analysis are both needed |
| Sagalassos | PostgreSQL, later with spatial data. Analog until 2006 | no | Users entered the same value in different ways, for example "4th Century AD" and "4th cent. AD". CIDOC CRM is planned, not done |
| Kaymakçı | Central PostgreSQL, MS Access forms, Android applications | not stated | Access forms over a central database are already in use in Türkiye |
| Arslantepe | PostgreSQL with PostGIS, Python modules. 4,858 features, 2,290 items, 7,486 objects, 22,166 documents | no | "Stratigraphic unit" is used for layers and for activities. The project uses its own definitions |
| Alacahöyük | Commissioned from a company in 2014 | nothing accessible | |
| Teos | Excavation and coin databases under construction | inscriptions only | |
| Juliopolis | Uses the Koç Üniversitesi archive infrastructure | partly | |

Four of these use PostgreSQL. None publishes its schema, as far as the thesis reports.
Each built its own structure. This is the situation that the fixed design of version 2 addresses.

### Things to obtain because of this thesis

| Item | Why |
|---|---|
| Directive annex Ek-21, "Kazı/Yüzey Araştırması Envanter Fişi" | The state's own form for an inventoried find. Version 2 must be able to hold every field of it |
| Directive annexes Ek-11/a and Ek-4/a | Final report form and application form of the director. They show what the state expects as structure |
| Directive annex Ek-16 | The only handover form. It is for the Ministry representative |
| Thesis annex Ek-3 | Table of what the Ministry asked for, by year |
| Thesis annex Ek-8 | Diagram of the data produced by archaeological research |
| Gürleyen 2020, PhD thesis, KoSeKA model | Survey of 22 institutions. Reports that institutions do not know CIDOC CRM |
| Özgüner 2015, PhD thesis | Evidence that the report series is incomplete |
| Özdoğan 2001 | Source of the statement on monopoly over documents |

### Local actors named in the thesis

Companies that offer services or software for excavations: GEOim, ArkeoLab, Regio, Hermes Danışmanlık, Somun İnşaat, Arkeo Teknik, FieldTech.
The thesis author also tried Kobo Toolbox for excavation forms.

### How the thesis and version 2 relate

| | Atalan Çayırezmez 2023 | Version 2 |
|---|---|---|
| Question | What should Türkiye do about archaeological data? | How should the content of an excavation be structured? |
| Level | Policy, metadata, identifiers, archives | Tables for contexts, finds, samples, relations, claims |
| Method | Document and content analysis | Design from the ontology, test on data |
| Ontology | Recommends CIDOC CRM, translated | Implements it, hidden behind tables |
| User in mind | Ministry, universities, archives | The excavator |

The thesis asks for a standard, a terminology, an ontology and identifiers. Version 2 is one way to deliver the second half of that list.
The two do not compete. Version 2 should cite the thesis as the statement of the need.

### Questions for the meeting in November

1. The thesis says data collection and management methods could not be treated in detail. Does she know of anyone in Türkiye working at that level now?
2. What does the Ministry portal of 2025 store: documents, or structured data? Is its data model written down anywhere?
3. Has the database announced in the directive, article 9, been built? Who defines what goes into it?
4. Which annex forms of the directive are filled in practice, and does anyone use the data from them?
5. She recommends translating CIDOC CRM into Turkish. Has that started? Would Turkish labels for a working subset be useful to her?
6. From her contact with excavation directors: what do teams use to record data? Is there anything behind the impression that it is mostly Excel?
7. Does she know of a case where data was lost or became unreadable when a director changed?
8. Would the national contacts in the European network be a route to test data from an excavation?
9. Were the data of her thesis published, as the data management plan intended? Where?

---

## 2. Hariri, Jean, Baron 2025: "Towards Automating RDF Extraction for Archaeological Knowledge Graphs with LLMs"

### What they did

| Point | Content |
|---|---|
| Site | Hypogée des Dunes, Poitiers. One site |
| Input | Four CSV tables: stratigraphic units (182 rows), facts (80), lapidary inventory (68), stone and geology (68). French |
| Text | Excluded, "due to the absence of a validated reference RDF dataset" |
| Task | The model writes triples in JSON-LD directly, 20 rows at a time |
| Conditions | No ontology in the prompt, full ontology, subset chosen by a domain expert |
| Examples | None, one, or three. The examples come from the same dataset |
| Models | GPT-4o, Llama 3.1, Mistral 7B |
| Ontology | CIDOC CRM. The extensions are named in the introduction. The later paper lists them as future work |

### Results as printed

Precision in percent, GPT-4o.

| Condition | No example | One example | Three examples |
|---|---|---|---|
| Full ontology, facts list | 17.0 | 76.3 | 88.1 |
| Subset, facts list | 19.0 | 85.0 | 90.2 |
| Full ontology, lapidary inventory | 16.5 | 77.2 | 89.3 |
| Subset, lapidary inventory | 18.0 | 84.8 | 91.0 |

Score on competency questions, GPT-4o with the subset and three examples: 88.5 percent.

### Reading of the results

| Observation | Consequence |
|---|---|
| Without an example, precision is below 20 percent even with the ontology in the prompt | The examples carry the result, more than the ontology |
| With three examples, the subset beats the full ontology by about 2 points | The headline finding rests on a small difference. No variance or repeated runs are reported |
| Examples and test data come from the same site | Nothing is shown about a second site |
| The number of competency questions is not given. Who built the reference set is not described | The scores cannot be checked |
| The subset "may miss useful information if their corresponding classes were excluded" | The same risk as our residue |
| Errors came from the source tables, for example "US12-US14" read as one unit | Messy cells are a problem of entry, which a database can refuse |
| The authors note that the model struggles with entries such as "possibly from Chamber II, dating uncertain" | Hedged statements are unsolved there. Version 1 has a rule for them |
| Nothing ensures that two chunks use the same path for the same kind of fact | Comparability is not measured |

---

## 3. Hariri, Jean, Baron 2026: "ASOS-CRM: Automated Semantic Scoping for CIDOC CRM Population"

### What they did

| Step | Content |
|---|---|
| Stage 1 | Each class and property is turned into a vector from its label, scope note and example. Each table column is turned into a vector from its header, sample values and an optional description by an expert. The nearest classes and properties are retrieved |
| Stage 2 | Every candidate triple is checked against the domain and range of the property. Invalid ones are dropped. If none is left, the search widens |
| Output | A subset of the ontology for that dataset, given to the model as in the first paper |
| Data | The same four tables |

### Results as printed

Averages over the four datasets, in percent.

| Method | Model | Precision | Recall | Competency questions |
|---|---|---|---|---|
| Manual subset | GPT-4o | 90.6 | 79.8 | 88.5 |
| Feng et al. | GPT-4o | 86.1 | 73.9 | 82.6 |
| ASOS-CRM | GPT-4o | 91.2 | 80.4 | 89.1 |
| ASOS-CRM | Llama 4 | 85.3 | 73.2 | 79.2 |

### Reading of the results

| Observation | Consequence |
|---|---|
| About 95 percent of the triples retrieved by similarity fail the domain and range check | Strong support for checking every statement against the ontology, as our residue table does |
| The scope was generated with column descriptions written by an expert. For petrography they are called essential | Expert work is reduced, not removed |
| The evaluation accepts "different but valid representations" | Several paths for one fact are accepted. The problem named by the ARIADNE working group is left open |
| The scope is built per dataset | Two datasets can get two different subsets |
| The gain over the manual subset is 0.6 points | Equal, within any reasonable error |
| Nine pages. Benchmarks and carbon figures are in the repository | Details must be taken from the code |
| Future work: CRMarchaeo and CRMsci | The extensions are not covered yet |

---

## 4. Their approach and version 2, side by side

| | Hariri, Jean, Baron | Version 2 |
|---|---|---|
| Who chooses classes and properties | The model, from a subset | Nobody at entry. They are fixed in the schema |
| What the model does | Writes triples | Fills values, and proposes properties only for the residue |
| Where the ontology check happens | Before the prompt, to build the subset | In the database, on every residue statement |
| Same path for the same fact | Not required | Required by design |
| Input | Tables of one site | Tables of any excavation. Reports as a pilot |
| Extensions | Future work | Part of the design |
| Hedged statements | Noted as a difficulty | One claims mechanism |
| User | Someone who can review triples | An excavator who sees tables |
| Measure | Precision, recall, competency questions | Coverage, schema stability, the working group's questions |

### What version 2 can take from them

| Idea | Use in version 2 |
|---|---|
| Check of domain and range as a filter | Already planned for the residue table. Their 95 percent figure is the argument for it |
| Column descriptions by an expert | The plain-word meaning we store for every column plays the same role |
| Similarity between a column and ontology text | Use it to match the columns of an excavator's spreadsheet to our fixed columns. The target is then a short list of columns, not hundreds of classes |
| Small local models | Relevant for unpublished data that must not leave the institution |
| Carbon figures | A measure that a committee in engineering may ask for |

The third row is a possible point of cooperation. Their method answers a question that version 2 will have
as soon as real spreadsheets arrive: which of our columns does this column belong to?

---

## 5. The excavation directive, 2024 copy

File: `papers/yonerge_2024.pdf`, 32 pages, downloaded from the ARIT web site. Main text read by keyword. The annex forms are not in this file, only their list.

| Article | Content | Note |
|---|---|---|
| 9(1)(çç) | Final report on form Ek-11/a-b within three months. All information, documents, photographs, drawings and publications are sent in digital form "oluşturulacak veri tabanında yer almak üzere" | Future tense: a database to be created. The system is not named |
| 9(1)(çç) | A director who does not send them cannot apply or renew the next year | |
| 9(1)(ü) | Finds from surveys are delivered to the museum with an inventory list and inventory form | |
| 13(1)(ö) | The Ministry representative records museum-grade movable finds on inventory forms (Ek-21) day by day, in two copies | The form is filled by the representative, not by the team |
| 13 | A new representative takes over with the handover form Ek-16 | Handover of the representative's duty only |

The word MUES does not occur in the directive text.

User's own knowledge, 2026-09-29: the system behind this is MUES and it is live. The directive text neither confirms nor contradicts this.
The thesis of Atalan Çayırezmez cites a 2013 paper on MUES that she co-wrote, so she can settle the question.

Still to obtain: the annex forms themselves, above all Ek-21, Ek-11/a and Ek-4/a. The Ministry web sites could not be reached from this machine.

---

## 6. Atalan Çayırezmez, Hacıgüzeller, Kalaycı 2021: "Archaeological Digital Archiving in Turkey"

File: `papers/ia.58.20.pdf`, 17 pages, Internet Archaeology 58. Read in full on 2026-09-29.
This is the article that version 1 rested on.

### Statements that can be cited

| Topic | What the article says | Section |
|---|---|---|
| Ownership of finds | All immovable and movable cultural assets are state property, protected under article 63 of the Constitution | 1 |
| What is submitted | Reports go to the General Directorate by post, on DVD or portable hard drive, in common text and image formats | 2 |
| Report templates | The guidelines "consist of templates providing only the main section titles" | 2 |
| Whole archive | "there is no practice of submitting entire archives of fieldwork documentation". A selection is sent | 2 |
| Central database | The General Directorate "aims to collect this information in a central database, an ongoing initiative" | 2 |
| Excavation archive | The directive refers to excavation archives without guidelines on how they must be curated, documented and cared for by the director "who is responsible for them" | 2 |
| Web sites | Since 2020 a project web site with finds and scientific data needs permission | 2 |
| MUES | Central database for movable objects in museums, with modules for excavation, exhibition, restoration and conservation. In 2021 the excavation and exhibition modules were "in progress" | 3 |
| Project databases | Thirty years of digital fieldwork led to "individual databases as closed systems, i.e. data silos" | 5 |
| Cause | "limited investment in high-quality metadata creation and data modelling using standard ontologies such as CIDOC CRM" | 5 |
| Guidelines | "there are no good guidelines for best practice and standards for archaeologists working in Turkey" | 5 |

### Figures

| Measure | Value |
|---|---|
| University excavations 2017 to 2019 | 167, of which 134 Turkish and 33 foreign |
| Projects with a web site | 83, of which 62 official and 21 unofficial |
| Foreign projects with a web site | 76 percent |
| Turkish projects with a web site | 43 percent |
| Web sites with a bibliography | 48, of which 26 give access to the publications |
| Web sites with an image gallery | 45, none with traceable identifiers |
| Web sites with a database | 5, of which 2 give direct access |
| Projects with entries in ARIADNE | 71 |
| Projects in Open Context | 11, almost all through specialist studies |
| Association between having a web site and having open data | below 0.2 |

### What it means for version 2

- The sentence on data silos and missing data modelling is the closest published statement of the gap that version 2 addresses. It comes from the person who knows the Ministry systems.
- The article confirms that MUES has an excavation module. The user reports that it is now live. What it stores from an excavation, and in what structure, is the question to settle.
- The director is responsible for the excavation archive, and nothing says how. This is the legal opening for a tool that serves the director first.
- Two of our three pilot sites are in the article's list, both without a web site: Seleukeia Sidera and Yumuktepe. Sinekkaya began in 2023 and is not listed.
- Ownership is stated for cultural assets. The article does not say who owns the documentation.

### Other papers by the same author to obtain

| Paper | Why |
|---|---|
| Atalan Çayırezmez, Aygün, Boz 2017, "Setting National Standards for the National Museum Inventory System of Turkey (MUES)", CIDOC conference | The data standards of MUES, presented to the CIDOC community |
| Atalan Çayırezmez, Çit, Wright 2025, Internet Archaeology 67 | Her most recent statement |
| Atalan Çayırezmez 2020, Heritage Turkey 10 | The BIAA repository |

---

## 7. PARTHENOS guide to the FAIR principles, Turkish edition

File: `papers/2020714_VeriYönetimiFAIR_Parthenos_SelfPrint.pdf`, 12 pages, July 2020, https://doi.org/10.5281/zenodo.3937149. Read in full on 2026-09-29.
Twenty principles for data producers and for archives. The thesis of Atalan Çayırezmez builds its table 24 on it.

### What the guide covers and what it does not

The guide is about datasets and the archives that hold them: identifiers, metadata, access, licences, formats.
It does not say how the content of an excavation should be structured.
So it guides the part of version 2 that packages and shares a dataset. It does not guide the tables for contexts and finds.

### The twenty principles against version 1 and version 2

| # | Principle | Version 1 | Who can meet it | Planned for version 2 |
|---|---|---|---|---|
| 1 | Invest in people and infrastructure | not applicable | institution | no |
| 2 | Use persistent identifiers | failed. Placeholder addresses | tool and institution | a column for the identifier of the dataset and of each record |
| 3 | Cite research data | absent | tool | a generated citation line for the dataset |
| 4 | Use persistent author identifiers | partly. ORCID column with a format check | tool | keep, add other identifier types |
| 5 | Choose a suitable metadata schema | absent. The ARIADNE catalogue test found 10 of 19 fields held | tool | dataset description table, exportable to a catalogue schema |
| 6 | Choose a trusted archive | absent | institution | no. Türkiye has no certified archive |
| 7 | State accessibility clearly | absent | tool | access field on the dataset |
| 8 | Apply an embargo where needed | absent | tool | embargo date on the dataset |
| 9 | Use standard exchange protocols | partly. RDF output, no endpoint | tool and institution | RDF export by the W3C mapping standard |
| 10 | Documented machine interfaces | absent | institution | no |
| 11 | Use open, well-defined vocabularies | failed. Types are free text | tool | vocabulary tables with links to published vocabularies |
| 12 | Document the metadata model | met. Every column has a meaning and a path | tool | keep |
| 13 | Use interoperable data standards | met for the ontology | tool | keep. Study the Dutch standard named in the guide |
| 14 | Build processes that raise data quality | met. 12 of 12 wrong entries refused | tool | keep. This is the core of the design |
| 15 | Use formats that last | mostly. SQLite, Turtle, CSV | tool | keep, add CSV export of every table |
| 16 | Document data systematically | partly. Gaps and printed errors are recorded | tool | method, abbreviations and known gaps stored with the dataset |
| 17 | Follow file naming rules | not applicable so far | tool | a rule for attached files |
| 18 | Use common file formats | absent. No spreadsheet export | tool | export to xlsx and CSV |
| 19 | Protect data integrity | absent | tool | version number and checksum on export |
| 20 | State the licence for reuse | absent | tool | licence and rights holder on the dataset |

Counted over the 17 principles that a tool can influence: version 1 meets 3, partly meets 4, and fails or lacks 10.

### Consequences for the design

1. **A dataset module is needed.** One table that describes the dataset as a whole: identifier, title, authors with identifiers, rights holder, licence, access, embargo date, version, checksum, method, known gaps. Principles 2, 3, 5, 7, 8, 16, 19 and 20 are met by filling it.
2. **The embargo is the argument for excavators.** Principle 8 allows the description to be public while the data stays closed for a stated time. The publication right of a director lasts five years from the end of the permit. A tool that shares the description now and the data after the embargo asks nothing that the law does not already grant.
3. **Principle 14 is already the strongest part of the design.** The guide's own example is to pick a date from a calendar and not type it. The database does this for every column.
4. **Principle 11 confirms failure 6 of version 1.** Types must come from vocabulary tables.
5. **The Dutch standard SIKB0102 must be studied.** The guide names it as the good example for archaeology. It is a national exchange standard for excavation data, which is what Türkiye lacks. The literature review saw it only as a search snippet.

### Limit

Meeting the principles makes a dataset findable and reusable as a file. It does not make two datasets comparable.
Comparability comes from the fixed paths, which the principles do not ask for.

---

## 8. SIKB0102, the Dutch exchange standard for excavation data

Studied on 2026-09-29 from primary sources.

| Source | File or link | Read |
|---|---|---|
| Schema and code lists, version 3.1.0, 2015 | `papers/sikb0102_v3.1.0_xsd_and_codelists.zip` | Analysed by program: every type, field and code list |
| Boasson and Visser 2017, Studies in Digital Heritage 1(2), 206 to 224, DOI 10.14434/sdh.v1i2.23262 | `papers/boasson_visser_2017_sikb0102.pdf` | In full |
| Evaluation for Forum Standaardisatie, 2022, chapter 3 | `papers/forum_standaardisatie_2022_evaluation.pdf` | Chapter 3 in full |
| Forum Standaardisatie, page on the standard | https://www.forumstandaardisatie.nl/open-standaarden/sikb0102 | Through a summary |
| SIKB pages on the standard | https://www.sikb.nl/datastandaarden/sikb0102-archeologie | Through a summary |
| Converter to linked data, pakbon-ld | https://github.com/wxwilcke/pakbon-ld | Description and ontology file. Last change 2016 |

The schema studied is version 3.1.0. The current version is 4.4, of 23 August 2024. The differences were not studied.

### 8.1 What it is

| Point | Content |
|---|---|
| Purpose | One format in which an excavator hands over data to a finds depot, the national archive and the national register |
| Origin | It began as a digital packing slip for finds delivered to a depot. "Pakbon" means packing slip |
| Form | XML, built like a relational database: every object once, with its own identifier, linked by references |
| Manager | SIKB, a foundation. Changes are decided twice a year by a board after work in expert groups |
| Status | On the Dutch list of open standards under "apply or explain" since 2 February 2016 |
| Timeline | Introduced in 2010. Required by the depots from 2016. In 2022 adoption was still incomplete |
| Users | 30 parties on the manager's list in 2022. The national archive named 24 organisations that send it |
| Cost | Yearly subscription in 2022: 292 euros for a municipality or company, 1,162 for a province, 2,641 for the national agency |
| Relation to CIDOC CRM | None in the standard. A university project mapped it to CIDOC CRM with the English Heritage extension in 2016 |

The designers write that the CRMarchaeo model "would have benefitted from our experience".

### 8.2 The fixed part: 38 types

| Group | Types | Count |
|---|---|---|
| Project and people | project, organisation, person, name, address, contractor, authority, project location, register number | 9 |
| Field structure | trench, plane, grid square, segment, feature, filling, structure, borehole, spoil, site | 10 |
| Link layers | observation, find context | 2 |
| Finds and samples | field find, find, sample | 3 |
| Storage | box, packaging unit | 2 |
| Documentation | drawing, photograph, document, file, digital medium, dossier | 6 |
| Space | location geometry, height measurement | 2 |
| Generic stores | attribute, attribute type, object relation, code reference | 4 |

Every type inherits from one base type with three things: its own identifier, the identifier it had in the source system, and a free remark.

Required fields are few. The designers define them as "the minimum set of attributes that is always present, even in a worst case excavation scenario".
A find needs a material category, an artefact type, a link to its field find, and three yes or no fields. Count, weight and period are optional.

### 8.3 The generic part: three stores

| Store | What it holds | Fields |
|---|---|---|
| Attribute store | Any extra attribute on any standard object. The attribute is defined once, then values refer to the definition | Definition: name, class it belongs to, value type, description. Value: whole number, decimal, text, yes or no, or reference |
| Relation store | Any relation between any two objects | Object 1 and its class, object 2 and its class, relation type, remark |
| Code reference | The excavator's own code beside the standard code | Own code, own description, own code list, standard code, link to the previous version |

Relation types in version 3.1.0, twelve in all: associated with, identical to, younger than, older than, lies above, lies below, lies against, part of, cut by, cuts, recorded on, recording of.

This is the architecture discussed for version 2: fixed types for what is common, a generic store for the rest, definitions of extra attributes kept as data.
It has been in national use for over ten years.

### 8.4 Code lists

24 lists with 6,969 codes in version 3.1.0. Each code carries a version, a date and a state, so a withdrawn code can be recognised.

| List | Codes |
|---|---|
| Artefact type | 2,891 |
| Place | 2,496 |
| Municipality | 424 |
| Map sheet | 302 |
| Complex type | 222 |
| Contractor | 159 |
| Structure type | 86 |
| Material category | 74 |
| Feature type | 62 |
| Period | 59 |
| Document type | 49 |
| Acquisition | 27 |
| Sample type | 26 |
| Collection method | 21 |
| Relation type | 12 |
| Context type | 11 |
| Eight further lists | 48 |

The code lists are kept in a data file, not in the schema. The designers give the reason: with thousands of codes the schema "explodes".

### 8.5 Design decisions and the reasons given

| Decision | Reason given by the designers |
|---|---|
| Keep the original level of detail beside a harmonised view | Harmonising alone loses the detail that matters for interpretation |
| Separate observation from interpretation | Observed data must stay available for a new interpretation |
| A link layer between feature and plane, called observation | One feature is seen in several planes. Excavators solved this in two incompatible ways |
| A link layer between find and its context, called find context | Finds are collected in different ways and attach to different kinds of object |
| Internal identifiers for all links | Numbers in excavation databases carry meaning, and the meaning differs between systems |
| A generic relation store | "Not every relationship can be foreseen". A link table for each would make the number of tables explode |
| A generic attribute store | "It would be impossible to be complete", and excavators cannot be forced to rewrite their coding system |
| The excavator's own codes beside the standard codes | "The typical code book is incomplete", by definition, since research produces new insight |
| Geometry inside the dataset | Links to separate spatial files cannot be checked |
| Versions on codes and on datasets | The national code lists change every year |

The paper also lists habits in excavation databases that made mapping hard: tables not normalised, keys made of numbers joined by dots,
dummy objects such as a feature numbered 999999 for finds from the spoil heap, and numbers that carry meaning.
The advisor's Access tables should be checked for the same habits.

### 8.6 What the 2022 evaluation found

| Finding | Source text in short |
|---|---|
| The standard ended a situation in which every depot had its own demands | section 3.2.2 |
| Nobody interviewed wants to go back to typing data in by hand | section 3.2.5 |
| The codes are adequate for running a depot and too general for anything else. They cannot be used during excavation, where people identify far more precisely | section 3.2.2 |
| The standard does not help synthesis. The detail travels in the original reports and tables, and finding it means reading documents | section 3.2.2 |
| **Depots cannot read the relations. They cannot read the excavators' own codes either** | section 3.2.2 |
| The lack of detail hinders acceptance by researchers and by depots | section 3.2.2 |
| Excavators must deliver in the format, and not all depots can read it | section 3.2.3 |
| Large firms managed. Implementations in Microsoft Access by small firms work badly with the depots' systems | section 3.2.3 |
| Municipal depots adopt little. They were left out of the first talks and lack money for software | section 3.2.3 |
| Little software exists. The market is small and the many relations need specialist knowledge | section 3.2.3 |
| Working groups often drop a proposed change because the cost is expected to be too high | section 3.2.4 |
| Making a field required later forces excavators to complete old projects by hand | section 3.2.4 |
| Changes in code lists cause problems. The protocol has to be separated from the codes | section 3.2.4 |
| Depots must support several versions at once, one of them 3.1 to 4.3 | section 3.2.4 |

The designers had warned in 2017 that excavators might send less than before, because converting everything takes more effort than sending files as they are.

### 8.7 The standard beside version 1 and the plan for version 2

| Topic | SIKB0102 | Version 1 | Plan for version 2 |
|---|---|---|---|
| Fixed types plus generic stores | yes | no | yes |
| Extra attributes defined as data | yes | no | yes, as templates |
| Own codes beside standard codes | yes | no | to add |
| Versions on codes | yes | no | to add |
| Stratigraphic relation types | 12, in the relation store | 7 | to extend |
| Link layer between find and context | yes | no. A find points at one feature and one deposit | to add |
| Several observations of one context | yes | no | to add |
| Boxes and packaging | yes | no | to add. Needed for delivery to a museum |
| Drawings, photographs, files | yes, each a type | one table added for paper 3 | to extend |
| Geometry and heights | yes | no | to add |
| Project administration | yes | partly | to extend |
| Who made a claim, and how sure | no. One free text field for interpretation on a filling | yes | one claims module |
| Laboratory results | no. Only the sample | yes | keep |
| People and their roles in the work | named persons in fixed roles | yes | keep |
| Cited literature | document type only | yes | keep |
| Periods with years | codes only | yes | keep |
| CIDOC CRM behind every field | no | yes | yes, executable |
| Checked against an ontology | no | yes | yes |
| Independent of one excavation method | no. Built on trench, plane, feature, filling | partly | required |

### 8.8 What to take

1. The three generic stores, with the same fields.
2. One base type for everything: own identifier, source identifier, remark.
3. Required fields only where a value exists even in the worst case. This is how a fixed design stays usable.
4. The excavator's own code kept beside the standard code. Nobody has to give up their own terms.
5. Code lists as data, each code with version, date and state.
6. The two link layers, observation and find context.
7. Types for box, packaging, drawing, photograph and file.
8. The relation list, to be merged with the list of iDAI.field.

### 8.9 What to do differently

| Weakness of the standard | Consequence for version 2 |
|---|---|
| What goes into the generic stores is written and never read | Every generic entry must appear in the generated views and in the graph. Coverage has to be measured as what a user can get out, not as what was stored |
| Codes too general for use in the field | The tool must be useful during excavation, with the excavator's own detail. The harmonised code is added, not substituted |
| It serves the receiver and not the excavator | The excavator's own benefit comes first: handover, own queries, own reports |
| No claims, no uncertainty, no laboratory results | These are modules in version 2 |
| Tied to the Dutch field method | The core follows CRMarchaeo, which does not assume one method |
| No ontology | The mapping is part of the design |
| Required fields added later broke old projects | Decide the required fields once, and keep them minimal |
| Small firms on Access fitted badly | The Access and Excel users are the main users in Türkiye. They are the test case, not the exception |

### 8.10 What it means for Türkiye

| The Netherlands | Türkiye |
|---|---|
| Finds must be deposited within two years, or the permit can be withdrawn | Finds go to the museum at the end of each season. Documentation goes to the General Directorate within three months, or the permit is not renewed |
| Each depot had its own demands until the standard | Report templates give section titles only |
| The packing slip for the depot became the national data standard | The inventory list and form Ek-21 for the museum could play the same part |
| A foundation outside the state manages the standard with the sector | No such body was found |
| Six years from introduction to obligation, twelve to partial adoption | |

The Dutch standard succeeded by attaching itself to an obligation that already existed.
The same kind of obligation exists in Türkiye, and the form of what must be delivered is not defined.

### 8.11 Limits of this study

- The schema studied is from 2015. Nine years of changes are not covered.
- The documentation of the standard in Dutch was not read, only the schema, the designers' paper and the evaluation.
- Whether the standard fits the recording systems used on excavations in Türkiye was not tested. No dataset was converted.
- The evaluation rests on interviews with eight experts.

---

## 9. Sources for a vocabulary in Turkish

Checked on 2026-09-29, after three blind tests showed that missing terms are the largest single gap.
Files of the tests against Wikidata: `vocabulary/wikidata_sparql.json`, `vocabulary/wikidata_taken_apart.json`.

### 9.1 TAY, Türkiye Arkeolojik Yerleşmeleri

Read from the site http://www.tayproject.org: the database page, both search forms, the help page, one settlement record, seven period records, one radiocarbon record.

| Point | Finding |
|---|---|
| What it is | An inventory of settlements. One record per settlement, one sub-record per period of that settlement |
| Technique | FileMaker served as web pages. No download, no interface for programs, no linked data |
| Licence | "Copyright ©1998 TAY Projesi" on the pages. No statement on reuse was found |
| Finds | Free text under fixed headings. No list of kinds of finds |

Controlled lists that the forms show:

| List | Values |
|---|---|
| Kind of settlement, prehistoric | Düz Yerleşme, Höyük, Kaya Sığınağı, Mağara, Mezarlık Alanı, Yamaç Yerleşmesi, Atölye, Tepe Üstü Yerleşme, Diğer. In records also Tekil Buluntu Yeri and Dağınık Buluntu Yeri |
| Kind of settlement, Greek and Roman | Çiftlik, Gözetleme Kulesi, İşlik, Kale, Karakol, Kent, Konut, Köprü, Köy, Kutsal Alan, Liman, Mezar, Nekropolis, Taş Ocağı, Tekil Buluntu, Tümülüs, Yol |
| Region | Marmara, Ege, İç Anadolu, Karadeniz, Doğu Anadolu, Akdeniz, Güneydoğu Anadolu |
| Age | Paleolitik/Epipaleolitik, Neolitik, Kalkolitik, İlk Tunç, Orta-Son Tunç, Demir Çağları, Yunan-Roma, Bizans |
| Sub-period, seen in records | Çanak Çömlekli, İTÇ II, İTÇ III |
| Method of research | Yüzey Araştırması, Kazı |
| Ancient region | Karia, Pisidia |

Headings inside a period record, seen in seven records:
Tarihçe, Araştırma ve Kazı, Tabakalanma, Buluntular, Mimari, Çanak Çömlek, Kil, Yontmataş and others by material, Kemik/Boynuz, İnsan Kalıntıları, Hayvan Kalıntıları, Bitki Kalıntıları, Mezarlar, Diğer, Kalıntılar, Yorum ve tarihleme.

Columns of the radiocarbon table: Lab No, GÖ with plus and minus, Malzeme, Tabaka, MÖ1 SDa, MÖ1 SDb, MÖ2 SDa, MÖ2 SDb, Açıklama.

What TAY gives the design:

| Use | How |
|---|---|
| Kinds of site | About 28 terms in Turkish, used nationally for 25 years. Can be the list for the kind of a site |
| Periods | The ages come with a definition and years on the database page. They can be entered as period definitions with TAY as the source. TAY is not in the PeriodO dataset |
| Identity of a site | The TAY number of a settlement can be stored as an identifier, to link an excavation to the national inventory |
| Headings of finds | A first level for kinds of finds, by material |
| Radiocarbon table | Its columns fit the `dating` table with laboratory code, error and two calibrated ranges. The design has one range |

Any reuse of TAY terms or numbers needs a question to the project about permission.

### 9.2 Other sources checked

| Source | Turkish | Open | Finding |
|---|---|---|---|
| Getty Art and Architecture Thesaurus | **5 concepts** have a Turkish label, of about 56,700 | yes, ODC-By | Counted by query on the Getty endpoint. Not usable for Turkish as it stands |
| Wikidata | yes | yes, CC0 | See 9.3 |
| Çambel, Arsebük, Kantman, *Çok Dilli Arkeoloji Terimleri Sözlüğü* | yes, with other languages | no. A printed book | Groups: excavation method, geology, materials, architecture, kinds of settlement, cemetery, stone tools, pottery, metal, seals. The closest thing to a national term list. Written by archaeologists of prehistory |
| PACTOLS, iDAI thesaurus | not verified | yes | Turkish coverage was not checked |

Not found: any open, structured vocabulary of archaeological terms in Turkish.

### 9.3 Test against Wikidata

The terms that the three blind tests could not match were looked up in Wikidata by their Turkish label or alias. Terms of up to three words.

| List | Terms | Found as written | Share |
|---|---|---|---|
| Kinds of things | 117 | 26 | 22 % |
| Materials | 19 | 5 | 26 % |
| Species | 7 | 7 | 100 % |

Then the 91 kinds of things that were not found were taken apart: plural ending removed, "parçası" and "kalıntısı" removed, head noun taken.

| Step | Found |
|---|---|
| As written | 26 of 117 |
| After taking the term apart | 69 more |
| Not found either way | 22 |

Not found either way, among others: ok ucu, çöp çukuru, tezgâh ağırlığı, çuvaldız, amphora, kâse, hayvan kemiği, insan kemiği.

Limits of this test:

- A label that exists is not proof of the right meaning. "at" is the horse and also other things. "kap", "oda", "tipi" are general words.
- The terms come from three reports. They are not a sample of Turkish archaeology.

### 9.4 What follows

1. **The terms in reports are phrases, not terms.** "kandil parçası" is a lamp and the state fragment. "tam firnisli tabaklar" is a plate, a surface treatment and a plural. Rule R18 of the blind tests forbids taking them apart, so they all count as own terms. The rule measures the list as shipped. It does not measure what a sheet with separate columns for kind, state and count would reach.
2. **A kind of find needs at least two fields:** the kind, and the part or state. With that, most of the unmatched terms fall on a short list of head nouns.
3. **No source can be taken over whole.** A list in Turkish has to be built: head nouns from the reports, checked against the printed dictionary, linked to Wikidata and the Getty thesaurus where a concept exists.
4. **This is a contribution of its own**, like the period definitions for PeriodO: an open list of archaeological terms in Turkish does not exist.
