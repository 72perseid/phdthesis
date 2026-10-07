# Third paper test: Sinekkaya Mağarası 2024

Paper 13 of the volume, picked at random (seed 1790682424), printed pages 197 to 208.
A Palaeolithic cave excavation. The first two papers were a classical city and a mound.

## Result in one line

The database did not hold. It refused 91 fields of 9 kinds. Four new tables and three new columns were needed.
After the change all three papers load, and the two earlier graphs are unchanged.

## Baseline: the database as it stood

| Refused field | Times | What the paper says there |
|---|---|---|
| `finds.part_of` | 63 | A cell of the count table belongs to the total of 677 pieces |
| `finds.dating_certainty` | 20 | "Neolitik?", "OP-ÜP?": hedged or alternative periods |
| `features.dating_certainty` | 1 | Hearth, "probably the last 50 to 60 years" |
| `strata.dating_certainty` | 1 | Unit F1.8, "probably Holocene" |
| `activities.sources` | 2 | Literature cited for the discovery and the 2023 season |
| `activities.excavated` | 1 | 871 buckets of 10 litres were dug |
| `activities.produced` | 1 | Looting created the spoil deposit X |
| list `references` | 1 | Bibliography, 3 entries |
| list `records` | 1 | 3D model and 1/50 plan made on site |

A tenth problem was not refused. The tables accepted `part_of` on a deposit, and the graph builder ignored it.
The round trip check could not see this, because both graphs lost it the same way.
`db/audit_fields.py` now tests every field by removing it and checking that the graph changes.

The old pipeline without the database built a graph from the same record with no error and passed validation.
It dropped all of the above silently. The database is what made the loss visible.

## What changed

| Change | Where | CIDOC CRM path |
|---|---|---|
| Certainty of a dating | column `dating.certainty` | E13 Attribute Assignment typed with certainty. No plain P10 is written |
| Find belongs to a counted assemblage | column `find.part_of` | P46i forms part of |
| Unit belongs to a layer | builder only | P46i forms part of |
| Work that created a deposit | link `produced` | A4 Stratigraphic Genesis, AP7 produced, A8 |
| Amount excavated | `dimension` rows on an excavation unit | A1, AP1 produced, S11 Amount of Matter, P43 |
| Cited literature | tables `reference`, `cited_for` | E31 Document, P70 documents |
| Documentation made on site | tables `documentation`, `documentation_depicts` | E73 Information Object, P94i, P67 |

Two of these paths came from the ontology lookup table in the database, not from memory.
P43 has dimension cannot start from an activity, so the amount dug had to go through S11 Amount of Matter.

Rules: R4 changed, R17 and R18 added. Questions: CQ14, CQ15, CQ16 added.

## After the change

| Check | Seleukeia | Yumuktepe | Sinekkaya |
|---|---|---|---|
| Rows in the database | 329 | 693 | 881 |
| Statements in the graph | 1,802 | 3,667 | 5,028 |
| Lost between record and graph | 0 | 0 | 0 |
| Graph changed by the new version | no | no | new |
| Fields stored but missing from the graph | 0 | 0 | 0 |
| Rule violations | 0 | 0 | 0 |
| Warnings | 0 | 4 | 2 |
| Questions answered, of 16 | 8 | 13 | 13 |

## Migration count so far

| Paper | Site type | New tables or lists | New fields |
|---|---|---|---|
| 1 Seleukeia Sidera | classical city | baseline | baseline |
| 2 Yumuktepe | mound | 4 lists | about 20 marked in `schema.md` |
| 3 Sinekkaya | cave | 2 lists, 4 tables | 5 |

The count for paper 2 is the number of `v2` marks in `schema.md`. It includes optional fields, so the two rows are not measured the same way yet.

The number is falling but it is not zero. Three papers are not enough to say the schema has settled.

## What the paper itself gets wrong

| Finding | Detail |
|---|---|
| Tablo 2 does not add up | Blade row sums to 156, printed 158. Columns "belirsiz", "Neo-ÜP?", "Neolitik?" are each off by one. Cells sum to 676, grand total 677 |
| Volume and mass disagree | 871 buckets of 10 litres is 8,710 litres. The paper gives 0.871 tonnes |
| Citation year | Text cites "Dinçer vd., 2025". The bibliography lists the same paper as 2024 |

All three are stored as printed, with a note. None was corrected.

## Still lost, even now

These are in the paper and ended up only in free-text notes, or nowhere.

| What | Example | Why it matters |
|---|---|---|
| Ages in years before present | cave lion, 450,000 to 14,000 years ago | The year columns hold calendar years only |
| Method details | 2 mm dry sieve, décapage, brush only | There is a type for the work but no place for its parameters |
| Negative results | in situ layers were not reached | Already a known gap since paper 2 |
| Part of an assemblage | "some tools are burnt" | A condition applies to a whole row or not at all |
| Skeletal element | teeth, jaw, finger bones | Only in the label |
| Vernacular taxon names | mağara aslanı | Only the scientific name is stored |
| Internal errors of a table | the four sums above | Stored as text, cannot be queried |
| Link from a single find to its table row | the Gravettian point | The paper does not say which row counts it |
| Coordinates | none given in the paper | Still no geometry in the database |

48 rows of this paper carry a note. Notes are where the schema gives up, so this number should be watched.

## Weak points of the model that this paper exposed

- Dating runs through E12 Production. That is wrong for bones and natural stones, which were not produced.
  It was already wrong for the plant remains of paper 2. It is not fixed yet.
- The count table became 60 find rows. That works, but a table of counts is a different kind of thing
  from a find, and real excavation data will be mostly such tables.

## Limits of this test

- I extracted the record and I know the schema. Someone who does not know it would produce a different record.
- E-mail addresses printed in the paper were left out on purpose.
- The record is in `data/sinekkaya_2024.json`, made by `tools/make_sinekkaya_record.py`.
  Only Tablo 2 was read by program and checked against the page image.
