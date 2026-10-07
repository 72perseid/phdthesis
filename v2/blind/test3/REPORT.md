# Blind test 3

Done on 2026-09-29 by version 2 of the rules, `../RULES.md`, written and frozen before the paper was drawn.
The database was not changed.

## 1. Paper and fingerprints

| Item | Value |
|---|---|
| Paper | Number 8, "İznik Hisardere Nekropolü 2024 Yılı Kazı Çalışmaları", Ekin Meriç, Öz, Koparal, Kutbay, Köse. Printed pages 115 to 132 |
| Kind of site | A Roman necropolis under an early Byzantine basilica. Graves, skeletons, a ceramics report by trench, conservation, anthropology |
| Seed | 20261001 |
| Rules, version 2 | `../RULES.sha256`, 19:32. Checked after the test: matches |
| Reader A's list | `readerA/statements.sha256`, 19:41. 679 statements |
| Reader B's list | `readerB/statements.sha256`. 693 statements |
| Files in `../../db/` | `db_before.sha256`. Checked after the test: identical |
| Loader's outcomes | `outcome.sha256`, frozen before the second judge was started |

| File | Contents |
|---|---|
| `outcome.csv` | Every statement with group, form, outcome, place and note. Opens in Excel |
| `load.py` | The loader |
| `judge.json` | The second judge's outcomes for 150 statements |
| `hisardere.sqlite`, `view/`, `hisardere.ttl` | What was stored |
| `run.txt` | Output of the last run |

## 2. Outcomes

| Outcome | All 679 | Core scope, 622 |
|---|---|---|
| A typed, complete | 240, 35.3 % | 235, 37.8 % |
| B typed, part lost | 58, 8.5 % | 50, 8.0 % |
| C own term | 190, 28.0 % | 186, 29.9 % |
| D own structure | 41, 6.0 % | 41, 6.6 % |
| E text only | 134, 19.7 % | 110, 17.7 % |
| F not stored | 16, 2.4 % | 0, 0.0 % |

**Typed and complete: 37.8 percent of the core scope. The target is 95.**

This time the two judges agree on all six outcomes. See section 8.

## 3. Lists against prose

Each statement was marked by the reader as coming from a list or from prose. Core scope only.

| Outcome | From lists, 270 | From prose, 352 |
|---|---|---|
| A typed, complete | 42.6 % | 34.1 % |
| B typed, part lost | 14.8 % | 2.8 % |
| C own term | 34.1 % | 26.7 % |
| D own structure | 3.3 % | 9.1 % |
| E text only | 5.2 % | 27.3 % |

| Reading | From lists | From prose |
|---|---|---|
| Reaches a typed place, with or without own term | 91.5 % | 63.6 % |
| Ends as text | 5.2 % | 27.3 % |

**Lists almost never fail. Prose fails in more than a quarter of the cases.**
What holds lists back is not structure. It is vocabulary: a third of all list statements needed an own term.

By group, the same picture:

| Group | Lists: A | Lists: text only | Prose: A | Prose: text only |
|---|---|---|---|---|
| FIND | 38 % | 0 % | 45 % | 12 % |
| DATE | 52 % | 0 % | too few | |
| MEASURE | 58 % | 0 % | 47 % | 0 % |
| BUILT | 31 % | 23 % | 7 % | 31 % |
| LAB | 14 % | 29 % | 8 % | 52 % |
| WORK | 35 % | 15 % | 8 % | 71 % |

Measurements do well in both forms. Work done and built things do badly in prose.

## 4. Outcomes per group

| Group | Statements | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| FIND | 154 | 63 | 10 | 67 | 6 | 8 | 0 |
| BUILT | 121 | 12 | 4 | 51 | 17 | 37 | 0 |
| WORK | 72 | 11 | 12 | 7 | 2 | 40 | 0 |
| DATE | 64 | 33 | 12 | 18 | 0 | 1 | 0 |
| MEASURE | 54 | 28 | 7 | 17 | 2 | 0 | 0 |
| LAB | 53 | 6 | 3 | 22 | 1 | 21 | 0 |
| PEOPLE | 29 | 12 | 2 | 4 | 11 | 0 | 0 |
| INTERP | 26 | 26 | 0 | 0 | 0 | 0 | 0 |
| FIGURE | 25 | 25 | 0 | 0 | 0 | 0 | 0 |
| PLACE | 17 | 13 | 0 | 0 | 2 | 2 | 0 |
| DOC | 7 | 6 | 0 | 0 | 0 | 1 | 0 |
| DESCR, outside the core | 22 | 0 | 0 | 0 | 0 | 22 | 0 |
| STRUCT, outside the core | 16 | 0 | 0 | 0 | 0 | 0 | 16 |
| ADMIN, outside the core | 11 | 4 | 2 | 3 | 0 | 2 | 0 |
| HISTORY, outside the core | 8 | 1 | 6 | 1 | 0 | 0 | 0 |

**Built things are the weakest group: 10 percent typed and complete.** This is a necropolis, and the graves are its main content.

## 5. Finds

| Measure | Value |
|---|---|
| Finds in the paper | 72 |
| Finds whose statements are all A | 5 |
| Finds whose statements are all A or B | 6 |

As in the second test, the kind of a find is almost never in the list.

## 6. What did not go in

### 6.1 F, not stored: 16

All are headings and page headers. None is in the core scope.

### 6.2 E, text only, core scope: 110

| Statements | Kind | Examples |
|---|---|---|
| 40 | Work: steps, aims, reasons, decisions | "the two covers on the west were opened", "it was decided to keep it closed", "to find the western limit of the basilica" |
| 31 | Built things: position, relation or state in words | "40 cm inside the north section", "surrounded by a row of bricks", "closed with a brick wall", "in the south part of the hypogeum" |
| 21 | Laboratory: steps and methods in sentences | "kept in the mixture by the packing method", "different techniques by age group" |
| 9 | Denials | see 7 |
| 9 | Others | kinds described in a sentence, counts in words such as "in small number" |

### 6.3 D, own structure: 41

| Statements | What the paper says | What is missing |
|---|---|---|
| 8 | "east-west" | Orientation of a grave or a wall |
| 11 | Title and address of a person | As in both earlier tests |
| 6 | "in heaps", "scattered", "in situ" | How a find lay |
| 6 | Masonry and workmanship | How a thing was built |
| 4 | Size and opening level of a trench | **Refused by the database.** A place cannot carry a measurement |
| 3 | Colour, form | |
| 2 | Distance between two things | |
| 1 | Sex of a skeleton | See 9, deviation 3 |

### 6.4 C, own term: 190

| Statements | List | Examples |
|---|---|---|
| 75 | Kinds of things | çatkı mezar, hipoje, kline, sanduka, tam firnisli tabak, Megara kasesi, mermer seramikleri |
| 48 | Kinds of measurement | "a x b", north-south, east-west, number of individuals, share in percent, concentration |
| 21 | Condition | tahrip olmuş, osteoartrit, hipoplazi |
| 14 | Units | bag, pair |
| 10 | Materials | tuğla, pişmiş toprak, moloz taş, çelik iskelet |
| 9 | Criteria of anthropology | epifiz kaynaşması, dental aşınma derecesi |
| 13 | Others | roles, motifs, kinds of record, methods |

The database has no word for any kind of grave except "mezar".

### 6.5 B, typed with a part lost: 58

| Statements | What is lost |
|---|---|
| 12 | "In general": the ceramics of a trench belong "in general" to a period. The whole group is dated |
| 12 | A compound of squares, such as "J-K/18", is one place |
| 10 | An entity holds only a name |
| 14 | A qualifier: "inner" length, "from the allowance", "was destroyed" stored as "was worked on" |
| 4 | Day and month |
| 6 | Others |

## 7. Hedges and denials

| | In the paper | Kept | Lost | Text only |
|---|---|---|---|---|
| Hedges | 20 | 14 | 4 | 2 |
| Denials | 10 | 1 | 0 | 9 |

The four lost hedges are measurements taken from traces of a destroyed couch. A measurement has a mark for "about" and no claim.

The nine denials that failed:

| Statements | What is denied |
|---|---|
| 3 | No skeleton and no find was found in the grave |
| 4 | The walls have no plaster. The plaster has no decoration |
| 2 | The old roofs were not sufficient. The concrete feet do not touch the ground of the site |

The first three are the most serious. "This grave was empty" is a finding. The database cannot say it, because something that was not found is not an entity.

## 8. Checks and agreement

### 8.1 What was stored

| Check | Result |
|---|---|
| Problems in the stored data | 0 |
| Statements in the graph | 4,530 |
| Statements in the graph against the ontology | 0 |
| Columns with data that do not reach the graph | 0 of 66 |

### 8.2 The two readers

| Measure | Value |
|---|---|
| Statements, reader A and reader B | 679 and 693 |
| Reader A's statements that reader B also has | 513 of 679, 75.6 % |
| Reader B's statements that reader A also has | 515 of 693, 74.3 % |
| Same form, list or prose, where the statement matches | 479 of 513, 93.4 % |
| Same group, where the statement matches | 429 of 513, 83.6 % |
| Hedged statements | 20 and 26 |
| Denials | 10 and 11 |

The readers cut the paper alike and mark list and prose alike. They differ on groups: reader B put the periods of finds under FIND, reader A under DATE.
So the figures per group depend on the reader. The figures by form depend on the reader much less.

### 8.3 The two judges, on 150 statements

| Grouping of outcomes | Equal | Kappa |
|---|---|---|
| Six outcomes | 82.0 % | 0.76 |
| A and B joined, C and D joined, E and F joined | 90.0 % | 0.84 |
| A against everything else | 92.7 % | 0.84 |
| Text only or not stored, against everything else | 95.3 % | 0.85 |

| Outcome | Loader | Second judge |
|---|---|---|
| A | 38.0 % | 36.0 % |
| B | 8.0 % | 10.7 % |
| C | 22.7 % | 24.7 % |
| D | 10.0 % | 12.0 % |
| E | 20.0 % | 16.7 % |
| F | 1.3 % | 0.0 % |

| | Test 2, rules version 1 | Test 3, rules version 2 |
|---|---|---|
| Equal on six outcomes | 56.0 % | 82.0 % |
| Kappa | 0.45 | 0.76 |

**The new rules closed the gap between "part lost" and "text only".**

Where the judges still differ, by the judge's own account:

- A tool or a deposit named by a common noun: is its kind an own term, or is a name enough? 4 cases.
- "In the south part of the hypogeum": a position in words, or a part of the building? 3 cases.
- A measurement with a qualifier such as "inner": own kind of measurement, or qualifier lost?

## 9. Deviations from the rules

| # | Deviation | Reason |
|---|---|---|
| 1 | The loader takes up to four words as a term and more as a sentence | The rules do not say what a term is. Without a limit, any sentence could become an own code. The limit is mine and was set before the judge was started |
| 2 | One rule of the loader was corrected after the first run | "MS 3.-4. yy." was marked as several periods in one name. It is one span of years. Corrected before the outcomes were frozen |
| 3 | The loader missed two declared attributes | The list has `sex` and `skeletal_element`. The loader used an own attribute for the sex of a skeleton. The judge found the declared one. By the rules the outcome stays as frozen. It should have been A |

Deviation 3 matters for one result of the earlier tests. I reported that no declared attribute was ever used. In this paper two of them fit, and I did not use them.

## 10. Errors in the paper, found by the readers

Both readers reported these, each alone.

| Finding | Detail |
|---|---|
| Resim 4 and 5 are swapped | The text and the captions name opposite hypogea |
| Funding of squares E-15 and E-16 | Ministry allowance on page 115, Geleceğe Miras Projesi on page 123 |
| Count of çatkı graves | 10 in the conclusion, 11 in the descriptions |
| Count of hypogea | 7 in the conclusion, 5 described |
| Plaque-covered graves in E-15 | Two stated, one described |
| Bronze coins | 3 found, 6 handed to conservation |
| Square J-15 | In the ceramics list, not among the excavated squares |
| Team | 14 people stated on page 115, five more named later |

One was found by reader B alone: page 117 says the sanduka grave held no skeleton, page 122 says skeletons from the sanduka grave were examined.

## 11. The three tests together

| | Test 1, Zerzevan | Test 2, Hacımusalar | Test 3, Hisardere |
|---|---|---|---|
| Kind of site | military settlement | mound | necropolis |
| Rules | none beforehand | version 1 | version 2 |
| Statements | 1,500 | 563 | 679 |
| A, core scope | not measured | 37.4 % | 37.8 % |
| C and D, core scope | not measured | 26.9 % | 36.5 % |
| B, E and F, core scope | not measured | 35.7 % | 25.7 % |
| Judges equal | not measured | 56 % | 82 % |

Two papers of different kinds, two sets of readers, and the same share of typed and complete statements: 37 to 38 percent.

Gaps seen in all three tests:

| Gap | Test 1 | Test 2 | Test 3 |
|---|---|---|---|
| Kinds of things missing from the list | 115 | 32 | 75 |
| Position relative to something else | 19 | 29 | about 30 |
| "a x b" and other unnamed sizes | 5 | 9 | about 20 |
| Measurement on a place | 3 | 27 | 4 |
| Title, office, address of a person | 32 | 5 | 11 |
| Day and month | 2 | 22 | 4 |

Seen in tests 2 and 3: denials of a property or of a find, shape and form, how a find lay, counts in words, steps and decisions of the work.

New in test 3: orientation, masonry, shares in percent, criteria of anthropology, an empty grave.

## 12. Limits

1. Readers and second judge are language models. No archaeologist took part.
2. The loader is mine. I know the tables and wrote the rules.
3. Three papers from one volume of one year.
4. Figures per group depend on the reader.
5. The readers did not see the plans and photographs.
