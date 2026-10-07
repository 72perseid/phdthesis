# Blind test on one unseen paper

Done on 2026-09-29. The database was not changed. This report lists what did not go in.

## 1. How the test was made

| Step | What was done |
|---|---|
| 1 | The files in `../db/` were fingerprinted before the test |
| 2 | One paper was drawn at random from the papers not yet used. Seed 20260929 |
| 3 | A reader that had never seen the tables listed every statement of the paper |
| 4 | The list was frozen. Its fingerprint is in `statements.sha256` |
| 5 | An empty database was built from the unchanged files |
| 6 | Every statement was tried. Each got one outcome |
| 7 | The files in `../db/` were fingerprinted again. They are identical |

**The paper:** number 12, "Zerzevan Kalesi 2024 Yılı Çalışmaları", Coşkun, Durma and Ayus. Printed pages 181 to 196.
A Roman military settlement with a Mithras sanctuary. None of the three earlier papers is of this kind.

| File | Contents |
|---|---|
| `statements.json` | The 1,500 statements as the reader listed them |
| `outcome.csv` | One line per statement: outcome, where it went, note. Opens in Excel |
| `load_blind.py` | The loader. Every decision is written in it |
| `zerzevan.sqlite` | The database after loading |
| `view/` | What was stored, as wide tables |
| `zerzevan.ttl` | The graph |
| `run.txt` | Output of the last run |

## 2. Result

| Outcome | Meaning | Statements | Share |
|---|---|---|---|
| 1 typed | A column, a declared relation, a standard code | 1,084 | 72.3 % |
| 2 template | A declared attribute | 0 | 0.0 % |
| 3 own | Needed an own code, an own attribute or a raw property | 317 | 21.1 % |
| 4 text only | Kept only as free text in a remark | 87 | 5.8 % |
| X not stored | No place at all | 12 | 0.8 % |

**Typed and template together: 72.3 percent. The target is 95.**

The database refused nothing that was stored in the end. One kind of entry was refused and went to an own attribute: a measurement on a place.

The paper has two very different parts.

| Part | Statements | Typed | Own | Text only | Not stored |
|---|---|---|---|---|---|
| The list of finds | 1,029 | 83.4 % | 14.9 % | 1.7 % | 0 % |
| Everything else | 471 | 48.0 % | 34.8 % | 14.6 % | 2.5 % |

What was stored is sound:

| Check on the stored data | Result |
|---|---|
| Problems in the stored data | 0 |
| Statements in the graph | 6,820 |
| Statements in the graph against the ontology | 0 |
| Columns with data that do not reach the graph | 0 of 80 |

## 3. What did not go in

### 3.1 Not stored at all: 12 statements

| Statements | What | Why |
|---|---|---|
| 7 | Section headings, page header, "the annex contains" | Structure of the printed document. The database has no place for it. It is not fieldwork data |
| 4 | "Beads, lamps, unguentaria and bracelets were also documented" | Says only that a kind of find was recorded. There is no find to attach it to |
| 1 | "The Roman Empire often met the Sasanians on its eastern border" | General history |

### 3.2 Kept only as text: 87 statements

| Statements | What the paper says | What is missing in the database |
|---|---|---|
| 18 | A find lay "west of the church", "north of the cistern" | A position relative to a building. Direction and building are not data |
| 3 | Points P11, P12, P13 were the reference for levelling | A reference point is a place. "Used" needs a thing |
| 3 | The sanctuary is judged by its location, its plan, its elements in place | The basis of a claim must be an entity or another claim |
| 2 | The season ran from 09.01.2024 to 31.12.2024 | **Years are whole numbers. Day and month cannot be stored** |
| 2 | The site is 13 km from Çınar and 1 km from Demirölçek | A distance between two places |
| 5 | The team is employed by the Ministry and the municipality. Workers came through İŞKUR | Employment |
| 1 | The hall lies behind the door | A position of one built thing relative to another |
| 1 | The dental drill could not clean some places | A negative statement needs a relation to deny. Here there is none |
| 8 | Objects were weighed and measured, before and after treatment | The paper gives no values |
| 5 | Purposes: "to improve access", "to cut contact with air" | A purpose given as text |
| 1 | Plan 1 is dated 2024 | A drawing has no year of its own |
| 38 | Descriptions and judgements: "strategic", "unique", "a wide range of forms", "shows soot traces", "gives data on herding" | Free description. No structure was tried |

### 3.3 Went in only through own additions: 317 statements

**255 of the 317 are vocabulary only.** The table and the column exist. The term is missing from the list.

| Statements | List | Examples |
|---|---|---|
| 115 | Kinds of things | ok ucu, yüzük, kandil parçası, seramik parçaları, ağırşak, çivi |
| 57 | Roles | the role of a body that is thanked, Arkeolog, Restoratör, Bakanlık Yetkili Uzmanı, sponsor |
| 19 | Collection method | "yüzeyde" |
| 19 | Condition and damage | kırık durumda, malahit, irizasyon bozulma |
| 16 | Material | pişmiş toprak, klorit, bakır, seramik |
| 9 | Kinds of record | rekonstrüksiyon çizimleri, render, arazi modellemesi |
| 7 | Vocabulary statements | "çömlek is a cooking vessel" |
| 6 | Species | koyun, keçi, sığır, at, domuz, tavuk |
| 7 | Others | function, unit month, kind of work, plan of work, kind of vault |

The other 62 show a structure that is missing.

| Statements | What the paper says | What is missing |
|---|---|---|
| 21 | "Diyarbakır Valisi", "Kazılar Şubesi Müdürü" | An office that a person holds in an institution |
| 11 | "Prof. Dr.", "Doç. Dr." | An academic title |
| 5 | "1.31 x 1.28 m" | The paper does not say which is width and which is height. The kinds of measurement assume it does |
| 5 | Alcohol at 50 percent, Paraloid B72 at 45 to 50, at 3 and at 1 percent | A concentration. One substance used three ways cannot be told apart |
| 4 | Casting, forging, riveting, filigree | A technique of making |
| 3 | Stair 1 lies in squares S25/4 and S26/3 | A thing has one column for its place |
| 3 | Elevation of the reference points | **Refused by the database.** A place cannot carry a measurement |
| 2 | Depth 0.17 m in the north, 0.65 m in the south | A measurement taken at a named point of a thing |
| 8 | Orientation north to south, building technique, number of the season, second name, order in time of two works, number of steps, preserved length, a range of block numbers | One each |

### 3.4 Typed, with a part lost: 196 of the 1,084

These count as typed above. A strict count would not accept all of them.

| Statements | What is lost |
|---|---|
| 123 | The position inside a grid square, such as "C3". It is stored as a named place inside the square. The database has no kind of place for it |
| 19 | Vegetation was cleaned "around and inside" 19 buildings. The buildings are linked. "Around and inside" is lost |
| 17 | A source cited for one sentence is tied to the thing, not to the sentence |
| 9 | An affiliation is one name. University, faculty and department are not separated |
| 7 | "T23/2-3-4" is one place. It is not resolved into three squares |
| 12 | In conservation, which tool was used on which material |
| 5 | "Important" finds |
| 4 | Others |

If these 196 are not accepted as typed, the typed share is 59.2 percent.

### 3.5 Hedges

The reader marked 20 statements as hedged. 17 kept their hedge as a claim. 3 lost it: glass forms "generally" include bottles, bowls and goblets.

## 4. What the test says about the design

| # | Finding | Kind |
|---|---|---|
| 1 | The find list fits well. Code, square, elevation, count, material and figure all have a place | strength |
| 2 | Time is too coarse. An excavation season has days | gap in a column |
| 3 | A place cannot be measured. The ontology lets only things and events carry a measurement through the path used | gap in a path |
| 4 | Positions are relative in the paper: west of, behind, inside a square | gap in relations |
| 5 | A thing can lie in two places | one column too few, or a relation type |
| 6 | People have offices and titles. A state excavation report is full of them | gap in the actor table |
| 7 | Turkish find terms join kind, state and number: "kandil parçası", "seramik parçaları" | vocabulary design |
| 8 | No declared attribute was used. The 25 shipped ones did not match anything in the paper | the template level is untested |
| 9 | Conservation is a chain of steps with substances and concentrations | no module for it |
| 10 | About 4 in 10 statements outside the find list are administration, thanks and description | question of scope |

Finding 10 is a decision for the thesis, not for the database. If thanks and offices are out of scope, the shares change.

## 5. Something for an archaeologist to judge

The paper states the highest level of the excavated area as 892.444 m and the lowest as 889.444 m.
Of 118 find elevations, 74 lie above the highest and 2 below the lowest.
One find, CHP, is at 897.656 m. The highest reference point is at 895.776 m.

The two levels may describe the surface after excavation. Then there is no conflict, except for CHP.
The database stores all values as printed. A query found this.

## 6. Limits

1. **The reader is a language model, not an archaeologist.** It may have split or missed statements differently from a person.
2. **The loader is mine, and I know the tables.** Another loader would choose other classes and relations in places.
3. **The shares depend on how finely statements are cut.** The find list gives 69 percent of all statements, because each find yields about eight.
4. **One paper.** It says nothing about the 95 percent as a claim over many excavations.
5. **The reader saw the text only.** Plans and photographs were not read.
6. **Page numbers.** The task gave the reader 183 to 198, which are pages of the file. The reader used the printed numbers, 181 to 196. These are in the list.
7. **One mistake of the loader is in the data.** The site got the kind "site" from the wrong list and so made one needless own code.
