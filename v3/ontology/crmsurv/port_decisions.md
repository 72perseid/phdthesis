# Porting CRMsurv 1.1 to CRM 7.1.3 and CRMsci 3.2: who decides what

Written 2026-10-19. The port has mechanical steps and modelling decisions. The decisions are the domain person's.
Each answer becomes one row of the decision log: item, choice, reason, date, person.

Revised 2026-10-19: no survey records are in hand yet, so the decisions are answered on theory and on the practice of Mediterranean and Anatolian survey as published. Each answer is marked provisional and re-checked when the first real unit arrives.

## Mechanical, no meaning involved

| Step | What |
|---|---|
| M1 | Convert rdfs:Class and rdf:Property to owl:Class, owl:ObjectProperty, with rdfs:label and rdfs:comment kept |
| M2 | Add an owl:Ontology header with a version IRI and owl:imports of CIDOC_CRM_v7.1.3.owl and CRMsci_v3.2.owl |
| M3 | Rewrite http://www.cidoc-crm.org/cidoc-crm/CRMsci/ to http://www.cidoc-crm.org/extensions/crmsci/ |
| M4 | Add the ported file to catalog-v001.xml so Protégé resolves it locally |
| M5 | Check every superclass, domain and range still exists in the imported files |

## Decisions, answered on theory for now

| # | Question | Options | What each implies |
|---|---|---|---|
| D1 | Where do conditions that affect what a walker can see belong: to each single act of observing, or to the observation as a whole? CRMsci 3.2 split the class CRMsurv used into S4 Single Observation and S27 Observation | S4, S27, or declare on S27 and let S4 inherit | Think of a visibility score. Is it recorded once per walker per pass, or once per unit per visit? In most Mediterranean protocols it is per unit per visit, which is the whole observation, not the single act |
| D2 | Is a survey unit a thing or a place? CRMsurv says a thing: a plot of ground, subclass of S20 Rigid Physical Feature. The 2020 paper admits units are often declared grid cells with no material identity, so a place, and only sites are material concentrations | U4 as physical feature; U4 as E53 Place; both, with site as E27 | In CRM you can remove something only from a thing, and you can encounter something only at a place. A grid cell drawn on a map is a place. A field with a wall and a scatter is a thing. Turkish surveys use both: ministry-style site lists are things, systematic tract walking is places. The profile probably needs both, with a rule for when a unit is promoted to a site |
| D3 | Is a bag of sherds a sample? Statistically yes, a sample of the surface record. In CRMsci a sample is an amount of matter taken from a material substantial, not a set of objects. CRMsurv invented U6 Material Sample to bridge this | Accept U6; or drop it and model the bag as E19 objects encountered and removed by an S19 event | U6 keeps the sampling meaning, which matters wherever a protocol collects a percentage of the surface. The E19 route is plainer and needs no new class, but loses the link to coverage. Answer depends on whether Turkish surveys record collection fractions at all, which is a question for the field |
| D4 | How is absence recorded? A unit walked by protocol with no finds is a real result, and a unit never walked is not the same thing | collection with zero members; observation with observed value zero; store nothing and infer | CRM has no negatives. Observed value zero on the observation stores the fact without inventing an empty thing, and keeps the difference between "walked, nothing" and "not walked". This matters for any density map |
| D5 | Are fabric, ware, shape, function and vessel part kinds of classes or kinds of vocabulary? CRMsurv made them subclasses of E55 Type. The SIG called that project-specific vocabulary dressed as ontology | keep; drop and use plain E55 with lists; keep as a shallow type hierarchy | The v2 design already answered this for everything else: terms are rows in lists, not classes. Keeping them would make ceramics the one domain where the vocabulary is baked into the ontology. Drop, unless compatibility with Groningen data is wanted later, and then a mapping of list to class is enough |
| D6 | Is recording with an instrument, such as GPS, drone or geophysics, a digitisation or a measurement? CRMsurv made it a digitisation process from CRMdig. The SIG said it looks like a measurement | drop; redeclare as subclass of S21 Measurement with types for GPS, drone, geophysics | A GPS fix is a position determination, S23, already in CRMsci. A drone orthophoto is a production of an image, E12 and E36. Geophysics is a measurement. None needs CRMdig. Drop U5 and use what CRMsci and base already have |
| D7 | Is collecting an encounter, a sampling, or both? CRMsurv made U2 a subclass of both S19 Encounter Event and S2 Sample Taking | keep both; keep S19 only | Follows D3. If the bag is a sample, collecting is sampling. If the bag is objects, collecting is encountering and removing |
| D8 | Whose ontology is the port? Keep the U and UP identifiers and the takin.solutions namespace, or mint our own | keep with attribution; new namespace | Keeping makes the port traceable and citable. A new namespace is honest if any class changes meaning, which D2, D5 and D6 will cause. Likely answer: new namespace, each class annotated with the CRMsurv class it derives from |

## Order

1. Answer D2 first. It decides D3, D4 and D7.
2. Answer D5 and D6 next. They decide which imports the header needs (M2).
3. D1 and D8 last.
4. Then the mechanical steps, then open in Protégé and annotate the two test units by hand.

## Test cases, when records arrive

Until then, the test case is the published description of a Turkish systematic survey: how units are defined, whether collection fractions are recorded, whether visibility is scored, and how absence is noted. The Araştırma Sonuçları Toplantısı volumes are the source for that.

- Later: one Karaburun unit with finds, one without, one Tokat unit. Each provisional answer is re-checked against them.
