# Report record format (JSON, version 3) → CIDOC CRM

`build_graph.py` reads one JSON record per paper. The record is flat and
archaeologist-readable; the builder adds the CRM event structure.
Every `id` is a short slug, unique within the record; cross-references use
those slugs. `pages` are the printed page numbers of the volume.

Version 2 is a superset of version 1: a v1 record builds unchanged.
Fields marked **v2** were added after the second paper (Yumuktepe) could not
be expressed in v1.

## Top level

| Key | Meaning |
| --- | --- |
| `base_uri` | namespace of this paper's entities |
| `shared_uri` **v2** | namespace shared by all papers, holds `vocab/`, `type/` and the volume; default: parent of `base_uri` |
| `schema_version` **v2** | `2` |

## Lists

| Key | Item fields | Becomes in CRM |
| --- | --- | --- |
| `document` | `id, title, language, authors[], pages, published, documents, source_file, volume{id,title,editor,publisher,isbn}` | E31 Document + E33 Linguistic Object; E65 Creation; volume E31 (shared); **v2**: `documents` → P129 is about (the reported campaign, entry point of the queries) |
| `actors[]` | `id, class (E21_Person / E74_Group), label, orcid?, member_of?, note?` **v2**`, pages?` | E21 / E74; ORCID → E42; `member_of` → P107 |
| `places[]` | `id, label, type?, within?, note?` **v2**`, pages?` | E53 Place; P2; P89 falls within |
| `periods[]` | `id, label, begin?, end?, within?` **v2**`, approx?` **v2**`, pages?` | E4 Period; P4 → E52; `within` → P9i forms part of |
| `features[]` | `id, class (E27_Site / E22_Human-Made_Object / E25_Human-Made_Feature), label, identifier?` **v2**`, type?, part_of?, location?, period(s)?, dating_by?` **v2**`, dimensions[]?, comparanda[]?` **v2**`, note?, pages?, figures?` | physical thing; P46; P53; P43; `identifier` → E42 typed "context code" |
| `strata[]` | `id, class (A2_Stratigraphic_Volume_Unit), label, identifier?` **v2**`, at_feature, period?` **v2**`, dimensions[]?` **v2**`, note?, pages?` | CRMarchaeo A2; P53 at the feature's place |
| `relations[]` **v2** | `id, from, to, type (cuts / destroys / overlies / fills / abuts / contemporary with), certainty?, by?, note?, pages?` | AP11 has physical relation to, both ends also typed A8 Stratigraphic Unit; plus E13 carrying the relation type, certainty and page. `contemporary with` → `kst:contemporaryWith` |
| `activities[]` | `id, class (A9_Archaeological_Excavation / A1_Excavation_Processing_Unit / E7_Activity), type, label, timespan{begin,end,approx?}?, carried_out_by[{actor,role}], took_place_at[]?, at_feature?, also_at[]?, part_of?, continued[]?, investigated?, removed[]?, used[]?, purpose_of?, identifier?, note?, pages?, figures?` | E7 (+A9/A1); P4 (inherited from the nearest dated ancestor); P14 + PC14 roles; P7; P9; P134; AP3; AP5; P16; P20. **v2**: `timespan` is optional, an undated earlier campaign gives a SHACL warning, not a failure |
| `plans[]` **v2** | `id, label, planned_for?, about[], place?, note?, pages?` | E29 Design or Procedure; P67 refers to; `kst:plannedFor`. Announced work is never an E7 Activity |
| `finds[]` | `id, class (E22 / E20_Biological_Object), label, type, taxa[]?` **v2**`, identified_by{by[],via}?` **v2**`, count?, material?, period(s)?, dating_by{by[],via}?` **v2**`, found_by, at_feature?, from_stratum?, condition?, depicts?, inscribed?, dimensions[]?, comparanda[{label,refs}]?` **v2**`, note?, pages?, figures?` | physical thing + S19 Encounter Event; A7 Embedding; `taxa` → P2 to E55 with broader term "taxon"; `dating_by` / `identified_by` → E13 naming who said so and how they know; `comparanda` → P130 shows features of |
| `samples[]` **v2** | `id, label, material_type, taxa[]?, taken_from, taken_during, pages?` | S13 Sample; S2 Sample Taking (O3 sampled from, O5 removed, P9i part of the excavation unit) |
| `analyses[]` **v2** | `id, type, label, samples[], result{begin,end}, dates?, by[]?, concluded_by[]?, note?, pages?` | S4 Single Observation (O8 observed sample, O9 property type, O16 observed value → E52). If `dates` is given: E5 Event "use phase" of the dated thing with that E52, and an E13 (P17 was motivated by the observation) stating the conclusion |
| `interpretations[]` | `id, about, assigned, by[], basis?, pages?` | E13 Attribute Assignment typed "interpretation" |
| `figures[]` | `id?` **v2**`, kind?` **v2** `(Resim / Şekil / Plan / Harita), number, caption, depicts[], page` | E36 Visual Item; P106i; P138. v1 records reference figures by number, read as `resim-N` |

## Version 3 additions (third paper, Sinekkaya)

The record is loaded into the database (`db/schema.sql`) before the graph is built. Unknown fields are refused.

| Key | Item fields | Becomes in CRM |
| --- | --- | --- |
| `dating_certainty` on features, strata, finds, samples | `uncertain` / `one of` | the dating exists only as E13 typed with the certainty; no plain P10 |
| `part_of` on finds and strata | id of the assemblage or layer | P46i forms part of |
| `produced[]` on activities | ids of deposits the work created | A4 Stratigraphic Genesis, AP7 produced |
| `excavated[]` on activities | dimensions of the soil dug | AP1 produced S11 Amount of Matter, P43 |
| `sources[]` on any item | `ref, pages?` | cited E31 Document (or its passage) P70 documents the item |
| `references[]` | `id, citation, year?, note?, pages?` | E31 Document typed "cited publication" |
| `records[]` | `id, type, label, scale?, made_by?, depicts[], note?, pages?, figures?` | E73 Information Object; E65 Creation inside the activity; P67 refers to |
| `figures[].kind` | also `Tablo` | as before |

## Conventions

- **Years** are historical years as strings; BC years are negative (`"-2580"` = 2580 BC).
  The builder writes `kst:beginYear` / `kst:endYear` as integers (used for comparison) and
  P82a / P82b as `xsd:dateTime` in ISO astronomical numbering (2580 BC → `-2579`), zero-padded to four digits.
- **Dimensions**: `{type, value, unit}` or `{type, min, max, unit}`; `approx: true` for "yaklaşık". Depths below the datum are negative values of type "depth below datum".
- **Figure references** on items are figure ids (`"resim-3"`, `"sekil-1"`).
- **Provenance**: every entity gets P70i is documented in the report and `kst:sourcePage` per page.
- **URIs**: `<base_uri><kind>/<id>`; E55 Types and the project vocabulary live under `<shared_uri>`.
  `example.org` is a placeholder and must become a persistent namespace before publication.

## Known gaps (not expressible yet)

- Ages in years before present; method parameters (mesh size); skeletal elements; vernacular taxon names.
- A condition that applies to part of an assemblage.
- Dating of bones and natural stones runs through E12 Production, which is the wrong class for them.

- Negative evidence ("no Early Bronze Age layer was found by earlier excavations").
- Multi-step arguments from literature (cultural influence, regional comparison) beyond a single E13.
- Coordinates and geometry; absolute elevations (depths are relative to an unstated datum).
- Reconciliation of actors, places and periods across papers: only types and the volume are shared.
- Laboratory metadata for radiocarbon (lab code, uncalibrated age, calibration curve) when a paper gives it.
