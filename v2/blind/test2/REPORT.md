# Blind test 2

Done on 2026-09-29 by the rules in `../RULES.md`, which were written and frozen before the paper was drawn.
The database was not changed.

## 1. Paper and fingerprints

| Item | Value |
|---|---|
| Paper | Number 19, "Antalya İli Elmalı İlçesi Hacımusalar Höyük Kazısı 2024 Yılı Çalışmaları", B. Arıkan. Printed pages 279 to 294 |
| Kind of site | A mound with layers from the Late Chalcolithic to the Byzantine period. Geophysics, two excavation areas, a church |
| Seed | 20260930 |
| Rules | `../RULES.sha256`, 18:33. Checked after the test: matches |
| Reader A's list | `readerA/statements.sha256`, 18:43. 563 statements |
| Reader B's list | `readerB/statements.sha256`, 18:42. 595 statements |
| Files in `../../db/` | `db_before.sha256`. Checked after the test: identical |
| Loader's outcomes | `outcome.sha256`, frozen before the second judge was started |

| File | Contents |
|---|---|
| `outcome.csv` | Every statement with its outcome, where it went, and the note. Opens in Excel |
| `load.py` | The loader. Every decision is written in it |
| `judge.json` | The second judge's outcomes for 150 statements |
| `hacimusalar.sqlite`, `view/`, `hacimusalar.ttl` | What was stored |
| `run.txt` | Output of the last run |

## 2. Outcomes

| Outcome | All 563 | Core scope, 516 |
|---|---|---|
| A typed, complete | 196, 34.8 % | 193, 37.4 % |
| B typed, part lost | 56, 9.9 % | 54, 10.5 % |
| C own term | 96, 17.1 % | 91, 17.6 % |
| D own structure | 52, 9.2 % | 48, 9.3 % |
| E text only | 144, 25.6 % | 130, 25.2 % |
| F not stored | 19, 3.4 % | 0, 0.0 % |

**Typed and complete: 37.4 percent of the core scope. The target is 95.**

Only A is a figure on which the two judges agree. See section 8. B and E cannot be told apart reliably with the present rules.

## 3. Outcomes per group

| Group | Statements | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| WORK | 155 | 45 | 32 | 8 | 6 | 64 | 0 |
| BUILT | 87 | 24 | 7 | 21 | 9 | 26 | 0 |
| FIND | 80 | 25 | 4 | 34 | 7 | 10 | 0 |
| PLACE | 41 | 6 | 1 | 14 | 4 | 16 | 0 |
| MEASURE | 37 | 16 | 3 | 3 | 11 | 4 | 0 |
| FIGURE | 33 | 31 | 0 | 0 | 0 | 2 | 0 |
| INTERP | 32 | 22 | 1 | 3 | 0 | 6 | 0 |
| PEOPLE | 29 | 11 | 0 | 7 | 11 | 0 | 0 |
| DATE | 18 | 11 | 6 | 1 | 0 | 0 | 0 |
| DOC | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| LAB | 2 | 0 | 0 | 0 | 0 | 2 | 0 |
| ADMIN, outside the core | 20 | 3 | 2 | 5 | 4 | 6 | 0 |
| STRUCT, outside the core | 19 | 0 | 0 | 0 | 0 | 0 | 19 |
| DESCR, outside the core | 7 | 0 | 0 | 0 | 0 | 7 | 0 |
| HISTORY, outside the core | 1 | 0 | 0 | 0 | 0 | 1 | 0 |

| Group | Share of A |
|---|---|
| FIGURE | 94 % |
| INTERP | 69 % |
| DATE | 61 % |
| MEASURE | 43 % |
| PEOPLE | 38 % |
| FIND | 31 % |
| WORK | 29 % |
| BUILT | 28 % |
| PLACE | 15 % |

## 4. Finds

| Measure | Value |
|---|---|
| Finds in the paper | 34 |
| Finds whose statements are all A | 3 |
| Finds whose statements are all A or B | 3 |
| Finds with at least one statement kept as text only | 9 |

The first statement of almost every find is its kind, and the kind is almost never in the list.

## 5. What did not go in

### 5.1 F, not stored: 19

All 19 are structure of the printed document: headings, page headers, column headings of the table. None is in the core scope.

### 5.2 E, text only: 144

| Statements | Kind | Examples |
|---|---|---|
| 29 | Position relative to something else | "west of trench C4b9", "right beside the cistern", "toward the apse" |
| 27 | Steps and states of the work | "first the trench was brought down to the floor of the pit", "excavated least so far", "will continue" |
| 17 | Aim, reason, expected result | "to find the thickness of the cultural fill", "to save labour and time" |
| 13 | Counts and sizes given in words | "very many", "more than a dozen", "much smaller", "very shallow", "a few rows" |
| 11 | Denials | see 5.5 |
| 47 | Others | what a layer contains in general, on what an interpretation is based, protection with a cover, position inside a photograph, audience of an event |

### 5.3 D, own structure: 52

| Statements | What the paper says | What is missing |
|---|---|---|
| 27 | Count of people in a group, elevation of a point, area and size of a trench, length of a survey line | **Refused by the database.** A place or a group cannot carry a measurement. 27 refusals, all of this kind |
| 6 | Shape: circular, oval, rectangular prism | Shape of a thing |
| 4 | "in situ", preserved part | State of finding |
| 5 | Title, office and address of a person | As in the first test |
| 3 | Workmanship, surface treatment | How a thing was worked |
| 2 | Electrical resistance of a layer | A property measured by geophysics |
| 2 | The locus from which a trench was started | **The locus. The paper names it, and the database has no place for it** |
| 3 | Order in time of two works, a second place for a thing | A raw property of the ontology was needed |

### 5.4 C, own term: 96

| Statements | List | Examples |
|---|---|---|
| 32 | Kinds of things | çöp çukuru, kerpiç dolgu, at figürini, tezgâh ağırlığı, seramik parçaları |
| 18 | Kinds of measurement | opening level, closing level, "a x b", spacing of electrodes |
| 12 | Roles | kazı başkanı yardımcısı, Kültür ve Turizm Bakanlığı temsilcisi |
| 12 | Materials | bakır, pişmiş toprak, kireç, orta boy taşlar, spolia |
| 9 | Condition | oldukça sert, iyi korunmuş, oldukça korozyona uğramış |
| 6 | Units | month, day, row of stones |
| 7 | Others | method ERT, function, species, surface find, reasoning by building style |

Two of these are near misses of the exact match: "kazı başkanı yardımcısı" against the label "başkan yardımcısı", and "Kültür ve Turizm Bakanlığı temsilcisi" against "bakanlık temsilcisi".

### 5.5 B, typed with a part lost: 56

| Statements | What is lost |
|---|---|
| 22 | Day and month. Years are whole numbers. The table of trenches has 14 dates |
| 10 | An entity holds only a name, with no kind from a list |
| 7 | Several periods in one name, or "from" and "until" not told apart |
| 17 | A qualifier: "begins at", "further north", "was exposed", "either or", "permitted by" |

## 6. Hedges and denials

| | In the paper | Kept in the database | Text only or not stored |
|---|---|---|---|
| Hedges | 63 | 51 | 12 |
| Denials | 14 | 1 | 12 |

One statement is both hedged and denied. It kept the hedge and lost the denial.

**Denials are the weak point.** The one that was kept is "the trenches did not reach the Early Bronze Age levels", because a relation exists to deny.
The others deny a property: the fill is not homogeneous, the walls give no plan, no notable find came out. There is nothing to attach the denial to.

## 7. Checks on what was stored

| Check | Result |
|---|---|
| Problems in the stored data | 0 |
| Statements in the graph | 3,478 |
| Statements in the graph against the ontology | 0 |
| Columns with data that do not reach the graph | 0 of 75 |

## 8. Agreement

### 8.1 The two readers

| Measure | Value |
|---|---|
| Statements, reader A and reader B | 563 and 595 |
| Reader A's statements that reader B also has | 451 of 563, 80.1 % |
| Reader B's statements that reader A also has | 454 of 595, 76.3 % |
| Same group, where the statement matches | 430 of 451, 95.3 % |
| Hedged statements | 63 and 55 |
| Denials | 14 and 14 |

The match asks for the same value in the same words. Two readers who word a value differently count as a miss. So 80 percent is a lower bound.

Both readers found the same errors in the paper, each alone. See section 10.

### 8.2 The two judges, on 150 statements

| Grouping of outcomes | Equal | Kappa |
|---|---|---|
| Six outcomes | 56.0 % | 0.45 |
| A and B joined, C and D joined | 64.7 % | 0.43 |
| A against everything else | 90.7 % | 0.79 |
| A, then C with D, then B with E and F | 78.0 % | 0.67 |

| Outcome | Loader | Second judge |
|---|---|---|
| A | 33.3 % | 32.0 % |
| B | 9.3 % | 36.7 % |
| C | 17.3 % | 16.7 % |
| D | 10.7 % | 10.0 % |
| E | 27.3 % | 4.7 % |
| F | 2.0 % | 0.0 % |

**The judges agree on A, C and D. They do not agree on B and E.**

In 27 cases I gave E and the judge gave B. The cause is one line of the rules.
Rule 4.3 lets an entity that "holds only a name" count as B. The judge used this for aims, reasons and positions:
the aim "to find the thickness of the fill" became an entity with that sentence as its name, linked by a declared relation.
I kept such sentences as remarks. Both readings follow the rules as written. The rules are at fault.

The judge also named ten places where the rules allow two outcomes. They are in the judge's hand-back and concern, above all,
where to put a measurement that the database refuses on a place.

### 8.3 What can be relied on

| Figure | Reliable |
|---|---|
| About a third of the statements are typed and complete | yes. Both judges, 33 and 32 percent |
| About a quarter to 28 percent need own terms or own structure | yes. Both judges, 28 and 27 percent |
| The rest, about 40 percent, is lost in part or kept as text | yes as a sum |
| How that 40 percent splits between "part lost" and "text only" | no |

## 9. Deviations from the rules

| # | Deviation | Reason |
|---|---|---|
| 1 | The loader was run twice. The first run gave 18 false refusals | A mistake in my loader: it wrote the year before the scale. Corrected before the outcomes were frozen and before the judge was started. The database was not touched |
| 2 | The second judge had the text of the paper | For context. The rules did not forbid it and did not foresee it |
| 3 | The content measure for readers was computed both with and without the subject | The rules ask for the first. The second is given in `run` output only |

The outcomes of the loader were not changed after the judge was seen.

## 10. Errors in the paper, found by the readers

Both readers reported these, each alone. They are stored as printed.

| Finding | Detail |
|---|---|
| Figure numbers in the text do not match the captions | From Resim 6 or 7 onward the text is shifted by one against the captions |
| Size of the mudbrick block | 35x3x12 cm in the text, 35x35x12 cm in the caption |
| Excavated volume | 120 m3 in the text, 120.78 in the table |
| Depth at which the geological layers begin | 15 m in one sentence, 12 m in the next paragraph |
| Opening date of trench E5c5 | 12.08.2024, before the start of the work on 29.08.2024 |

## 11. Beside the first test

The two tests cannot be compared by their headline figures.

| | Test 1, Zerzevan | Test 2, Hacımusalar |
|---|---|---|
| Rules | none written beforehand | frozen beforehand |
| Statements | 1,500 | 563 |
| Share of statements from lists of finds | 69 % | 14 % |
| "Typed", as counted then | 72.3 % | |
| "Typed" without those that lost a part | 59.2 % | |
| A, typed and complete | | 34.8 % |
| A and B | | 44.8 % |
| Term matching | exact | exact |
| Second class to make an entry pass | used once | forbidden |

The second paper is mostly narrative: what was done, where, why, and what it may mean. The first was mostly a list of finds.
The database is good at lists and weak at narrative.

Gaps seen in both tests:

| Gap | Test 1 | Test 2 |
|---|---|---|
| Day and month | 2 | 22 |
| Measurement on a place or a group | 3 | 27 |
| Position relative to something else | 19 | 29 |
| Title and office of a person | 32 | 4 |
| "a x b" without names | 5 | 9 |
| Kinds of things missing from the list | 115 | 32 |
| A thing in two places | 3 | 1 |

New in test 2: the locus, shape, denial of a property, counts in words, aims and reasons, steps of work.

## 12. Limits

1. Readers and second judge are language models. No archaeologist took part.
2. The loader is mine. I know the tables and wrote the rules.
3. One paper. Two tests together are two papers.
4. The rules have a gap between B and E. A second version is needed before a third test.
5. The readers did not see the plans and photographs.
