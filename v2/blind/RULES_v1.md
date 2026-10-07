# Rules for a blind test

Version 1, written on 2026-09-29, before the paper of the second blind test was drawn.
The fingerprint of this file is in `RULES.sha256`. A test is valid only if the fingerprint still matches.

## 1. Order of work

| Step | What | Rule |
|---|---|---|
| 1 | Fingerprint the files in `../db/` | They must be identical after the test |
| 2 | Draw the paper | Python `random.seed(20260930)`, `random.choice` over the sorted file names in `kst_paper_split`, without the front matter and without papers 12, 13, 14 and 18 |
| 3 | Two readers list the statements, each alone | Neither has seen the tables, the first test or the other reader's list |
| 4 | Freeze both lists with fingerprints | No statement is added, removed or reworded afterwards |
| 5 | Reader A's list is the list of the test | Reader B's list is used only to measure agreement. Decided here, before reading |
| 6 | Build an empty database from the unchanged files | |
| 7 | The loader tries every statement and gives it one outcome by section 4 | |
| 8 | A second judge gives outcomes to a sample, alone | 150 statements, drawn with `random.seed(7)`. The judge has the tables and these rules, and not the loader's outcomes |
| 9 | Report by section 6 | |

Nothing in `../db/` is changed during a test, whatever the result.

## 2. How a paper is cut into statements

**R1. Unit.** A statement is one subject, one property and one value.

**R2. Split.** A sentence that gives several properties or several values gives several statements.
"The wall is 12 m long and built of limestone" is two. "Coins and lamps were found in room 3" is two.

**R3. One fact once.** A fact that the paper repeats is listed once, at its first place.

**R4. Finds and samples.** Each find gets one statement for each of these that the paper gives:
kind, find number, place of finding, position inside that place, elevation, count, material, condition, each measurement, period, figure, and the work in which it was found.
When one code covers several kinds of find, each kind is a find of its own.

**R5. People.** Each person or body gets one statement for each of these that the paper gives:
role in the work, title, office, affiliation, identifier. Thanks are one statement per person or body thanked.
E-mail addresses are never listed.

**R6. Measurements.** "a x b" without names is one statement with both values. Each named measurement is one statement.

**R7. Hedges and denials.** The hedge is kept in its own field, in the words of the paper. A denial is marked.
A question mark after a word is a hedge on that word.

**R8. Who says so.** Filled only when the paper attributes the statement to somebody other than its authors.

**R9. Citations.** Each cited publication is one statement, tied to the sentence it is cited for.
Each entry of the bibliography is one statement.

**R10. Figures and tables.** Each caption is one statement. Each cell of a printed table is one statement.
Each mention of a figure in the text is one statement. Images are not read.

**R11. No outside knowledge.** Nothing is added that the paper does not say. Terms stay in the language of the paper.

**R12. Unclear text.** It is listed and marked as unclear. It is not guessed.

**R13. Group.** The reader gives each statement exactly one group from section 3.

## 3. Groups

Every statement belongs to one group. The group is given by the reader and is not changed by the loader.

| Group | Contents | In the core scope |
|---|---|---|
| DOC | The paper itself, its authors, the bibliography, citations | yes |
| STRUCT | Headings, page headers, "see annex" | no |
| PEOPLE | Team members and specialists: role, affiliation, identifier | yes |
| ADMIN | Thanks, permits, funding, offices and titles of officials, employment of workers | no |
| WORK | What was done, where, when, by which method, with which tools | yes |
| PLACE | Location of the site, places, squares, distances, coordinates, elevations of points | yes |
| BUILT | Buildings, walls, layers, pits, graves: kind, position, relations to each other | yes |
| FIND | Finds and samples, by rule R4 | yes |
| MEASURE | Measurements of buildings and layers | yes |
| DATE | Periods, years, laboratory dates | yes |
| INTERP | Interpretations, identifications of function, comparisons | yes |
| LAB | Analyses, conservation, restoration: steps, substances, results | yes |
| FIGURE | Captions and mentions of figures | yes |
| DESCR | Praise, judgement and general description without a fact that can be checked: "important", "strategic", "unique" | no |
| HISTORY | General history that is not about the fieldwork | no |

Two shares are reported: over all statements, and over the core scope.
Whether ADMIN belongs to the scope of the thesis is the user's decision. The report gives the figures both ways.

## 4. Outcomes

### 4.1 The six outcomes

| Outcome | Name | Rule |
|---|---|---|
| A | typed, complete | Subject, property, value, hedge, denial and attribution are all stored in columns, declared relations, declared attributes and standard codes |
| B | typed, part lost | The value is stored as in A. A named part is lost or weakened. See 4.3 |
| C | own term | The column or relation exists. The term is not in the list and became an own code |
| D | own structure | It needed an own attribute or a raw property of the ontology |
| E | text only | It is kept only as free text in a remark |
| F | not stored | The database refused it and no weaker place was found, or there is no place at all |

**R14. The worst part decides.** A statement gets the worst outcome of its parts. The order from best to worst is A, B, C, D, E, F.

**R15. Really stored.** An outcome other than F is given only after the row is written to the database without error.

**R16. Refusals are kept.** If the database refuses the first try and a weaker place works, the outcome is that of the weaker place, and the refusal is noted.

### 4.2 Terms

**R17. Exact match.** A term counts as a standard code only if it equals the code or one of its labels, ignoring upper and lower case and spaces at the ends.
No stemming, no translation, no "close enough". "kandil parçası" is not "kandil".

**R18. No splitting of terms.** The loader does not take a term apart. "kandil parçası" is not stored as kind "kandil" with condition "parça".

### 4.3 What makes a B

| Case | Example |
|---|---|
| The hedge cannot be stored in the place used | "generally" on a column without a claim |
| Precision is lost | a day stored as a year |
| A qualifier is lost | "around and inside", "important", "in the north" |
| An entity holds only a name, with no kind from a list | position "C3" inside a square |
| A compound is stored as one | "T23/2-3-4" as one place |
| The link goes to the thing and not to the sentence | a citation |
| Parts of a name are not separated | university, faculty, department in one name |
| The direction of a relation had to be turned | "lies below" stored as "overlies" is **not** a loss. It stays A |

### 4.4 Classes

**R19.** The loader takes the class from this table and from nowhere else.

| What | Class |
|---|---|
| The site as a whole | E27 |
| Building, wall, floor, pit, grave, oven, channel, any built feature | E25 |
| Layer, fill, deposit | A2 |
| Surface between layers, cut | A3 |
| Find made by people | E22 |
| Bone, plant remain, shell | E20 |
| Sample | S13 |
| Person | E21 |
| Institution, team, group | E74 |
| Place, square, trench, region, point | E53 |
| Period | E4 |
| Excavation project or season | A9 |
| Excavation of a trench or unit | A1 |
| Taking of a sample | S2 |
| Analysis, laboratory dating | S4 |
| Restoration, conservation | E11 |
| Any other work | E7 |
| Report, book, article | E31 |
| Photograph, drawing, plan | E36 |
| Plan of future work | E29 |

**R20. Second class.** Allowed in one case only: a built feature that stands in a stratigraphic relation gets A8 as second class.
No second class is given to make a refused entry pass.

### 4.5 What the loader may not do

**R21.** No change to `../db/`. **R22.** No statement is reworded to make it fit.
**R23.** No statement is left out. Each of them has an outcome in the file of outcomes.
**R24.** Where two places are possible, the loader takes the better outcome and notes the other.

## 5. Agreement

| Measure | How |
|---|---|
| Readers, by count | Statements per group, reader A beside reader B |
| Readers, by content | Share of reader A's statements that reader B also has: same printed page, same value after removing spaces and case, and subjects that share a word of four letters or more |
| Judges | On the sample of 150: share of equal outcomes, and Cohen's kappa over the six outcomes |
| Judges, coarse | The same with A and B joined, and C and D joined |

Disagreements are listed. The loader's outcomes are not changed after the judge has been seen.

## 6. What the report must contain

1. The paper, the seed, and the three fingerprints: rules, lists, database files before and after.
2. Outcomes A to F, over all statements and over the core scope.
3. Outcomes per group.
4. For finds: the share of finds whose statements are all A, and all A or B.
5. Every statement with outcome D, E or F, grouped by what is missing.
6. Own terms by list.
7. Hedges kept and lost. Denials kept and lost.
8. The measures of agreement, and the list of disagreements.
9. Checks on what was stored: data, graph against the ontology, columns that do not reach the graph.
10. Deviations from these rules, if any, each with its reason.

## 7. Known limits of these rules

- Readers and second judge are language models. No archaeologist takes part.
- The groups of section 3 are mine. Another set of groups would give other shares per group.
- Rule R17 is strict. It measures the lists as shipped, not what a careful curator could match.
- The share over all statements still depends on how many finds a paper lists.
