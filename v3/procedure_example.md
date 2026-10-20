# The instance-level procedure, with one worked example

Written 2026-10-18 for the question "what algorithm decides the class of an object and how it is described".
The rules below are not new. They are collected from `v2/blind/RULES.md` (R1 to R29),
`v2/design.md` section 3 (P1 to P12) and `v1/cidoc/extraction_prompt.md`.
What is new here is the order, and the marking of which steps are mechanical and which are judgments.

## The procedure

| Step | Question | Rule | Kind |
|---|---|---|---|
| 0 | Cut the text into statements: one subject, one property, one value | R1 to R4, R6 | mechanical |
| 1 | Is the subject an entity? Only a thing, place, person, group, work, period, document or image. Not an aim, reason, judgment, or a position in words | R25 | judgment, but narrowed by a closed list |
| 2 | Which class? Look it up in the 19-row table by what the thing is in field practice. No reasoning over CRM scope notes. Second class only for a built feature in a stratigraphic relation (A8) | R19, R20 | mechanical |
| 3 | For each property: observation or conclusion? A hedge word, an identification, a dating, a function is a conclusion. A conclusion never becomes a plain value. It becomes a claim with a belief value | P7, prompt rule 2, R7 | judgment, reducible to a marker list |
| 4 | Which path? One CRM path per property kind, from the path table. Kind goes to P2 has type, material to P45 consists of, measurement to P43 has dimension, and so on. If the ontology allows several, one was chosen and logged | P11 | mechanical |
| 5 | Which value? Exact match to the code list gives a standard code. No match gives an own code, scoped to the dataset. No stemming, no splitting, no translation. Hedge in its own field. Attribution only if someone other than the author says it | R17, R18, R7, R8 | mechanical |
| 6 | Events that exist only to connect, such as the finding of an object in a unit, are not stored. They are generated in the graph from the stored link | P8 | mechanical |
| 7 | If step 1 or 3 needed a decision, write one row in the decision log | P12 | mechanical |

Two steps are judgments. Both are the target of the hand annotation in this folder:
step 1 by extending the closed list of what may be an entity,
step 3 by collecting the Turkish markers of a conclusion
("olduğu düşünülmektedir", "muhtemelen", "?", "olabileceği", "değerlendirilmektedir", "olasılıkla").

## Worked example

Hacımusalar 2024 report, page 286, used in blind test 2. One sentence:

> Kazılardan çıkan küçük buluntular arasında oldukça korozyona uğramış bakır sikkeler ve takı (bilezik?),
> demirden imal edilmiş liturji (ayin) objeleri, pişmiş topraktan boncuk gibi etütlük sayılacak buluntular vardır.

**Step 0, cut.** Four finds: sikkeler, takı, liturji objeleri, boncuk. Rule R4 gives each one a statement
for every item the sentence supplies: kind, material, condition, identification, place of finding.
The scope of "korozyona uğramış bakır" is unclear: does it cover takı as well? Rule R12: list it, mark it unclear, do not guess.
Reader A did exactly that.

**Step 1, entity.** All four are things. Entities. "etütlük sayılacak" is a registration status, not a thing;
it is a value, not an entity. Whether it is a typed attribute of a find is open and belongs in the decision log.

**Step 2, class.** "Find made by people" in the R19 table gives E22 Human-Made Object for all four.
A bead of fired clay is still E22. No second class.

**Step 3, observation or conclusion.**

| Statement | Decision | Why |
|---|---|---|
| sikkeler, kind, sikke | observation | plain noun |
| sikkeler, material, bakır | observation | |
| sikkeler, condition, oldukça korozyona uğramış | observation, with degree | "oldukça" is a qualifier. The loader put it through a claim with belief true so the words survive |
| takı, identified as, bilezik | conclusion | the question mark. Claim with belief probable |
| liturji objeleri, material, demir | observation | |
| boncuk, material, pişmiş toprak | observation | |
| all four, found in, Merkezi Kilise kazıları | observation | |

**Step 4, path.** kind to P2 has type. material to P45 consists of. found in to the find context link.
identified as and condition go through the claim table, which the mapping turns into CRMinf belief
and an assertion on the object.

**Step 5, value.** Exact match against the shipped lists.

| Value | List | Match | Outcome |
|---|---|---|---|
| sikke | thing_type | yes | A |
| bakır | material | no | C, own code |
| oldukça korozyona uğramış | condition | no | C, own code |
| bilezik | thing_type | no | C, own code, hedge kept |
| liturji (ayin) objeleri | thing_type | no | C, own code |
| demir | material | yes, "iron" | A |
| pişmiş toprak | material | no | C, own code |
| boncuk | thing_type | yes, "bead" | A |
| Merkezi Kilise kazıları | find context | yes, it is an A1 unit | A |

**Step 6, events.** No "finding event" is stored. The graph builder generates it from the find context link.

**Step 7, log.** Two rows: "etütlük" status left out, reason: no attribute defined;
"bakır" scope over takı unclear, reason: sentence structure.

**Result in the graph**, for the bead, as it stands in `v2/blind/test2/hacimusalar.ttl`:

```turtle
<urn:fieldwork:entity:10f34979-...> a crm:E22_Human-Made_Object ;
    rdfs:label "boncuk" ;
    crm:P2_has_type <urn:fieldwork:code:thing_type/bead> ;
    crm:P45_consists_of <urn:fieldwork:code:material/hacimusalar-2024/pişmiş toprak> .
```

The kind is a standard code, so it is comparable across excavations. The material is an own code,
scoped to this dataset, so it is not, until "pişmiş toprak" is added to the material list.
That one row is the whole difference between outcome A and outcome C for this find.

## What this shows

- Class assignment is a table lookup, not reasoning. The table has 19 rows. That is deliberate:
  an excavator can apply a table, nobody in the field will read CRM scope notes.
- Most of the loss is not in classes or paths. It is in step 5, the vocabulary. Four of the nine values
  in this sentence failed only because a Turkish word was not in a list.
- The two judgment steps are small and can be made smaller by the hand annotation: a longer entity list, a marker list for conclusions.
- A tool without a language model can run steps 0 and 2 to 7 if the person types the statement in parts.
  Step 0 on free prose and step 3 on unmarked hedges are where a model, or a person, is still needed.
