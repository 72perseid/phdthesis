# CRMsurv, the unofficial survey extension of CIDOC CRM

Collected 2026-10-19. Files downloaded from Zenodo record 7863145 (CC BY 4.0), untouched.

| File | md5 | What |
|---|---|---|
| CRMSurv_1.1.rdf | ecb73d264708786943e09042b8586097 | version 1.1, 2023, the one published on OntoME |
| CRMsurv_v1.0.1.rdf | 3dfb898e897075c7f890ba8bb5556c15 | earlier version, still carries UP4 to UP8 |

## Who and when

- Groningen Institute of Archaeology (Tymon de Haas, Martijn van Leusen) with Takin.solutions (Denitsa Nenova, George Bruseker).
- 2016: KNAW-DANS Small Data Project, draft extension of CRMarchaeo to field-walking survey, three Groningen survey databases mapped and archived at DANS.
- 2017 onward: "FAIR surveys" project. Paper: de Haas and van Leusen 2020, FOLD&R Survey 12, Fasti Online.
- 2022 to 2023: finalised as CRMsurv under SEMAFORA, NWO Open Science Fund. Specification 1.1 on Zenodo (10.5281/zenodo.7863486, CC BY-SA 4.0), RDF on Zenodo (10.5281/zenodo.7863145, CC BY 4.0), namespace 231 on OntoME.
- 21 March 2024: presented to the 58th CIDOC CRM SIG by Nenova. Slides on cidoc-crm.org.

## Status with the SIG

Unofficial. The 58th SIG minutes record a presentation and discussion, no decision. Points raised:
CRMsurv could extend CRMsci as well as CRMarchaeo, since UP1 enriches Observation (ties to SIG issue 579);
U5 Digitization Process Unit needs a sharper scope and may be a subclass of S21 Measurement instead;
subtyping E55 for Fabric, Ware and so on was questioned, a shallow type hierarchy was suggested.
The slide deck ends with "Incorporation into CRMarchaeo?". No later SIG decision found as of 2026-10-19.

## Classes and properties, version 1.1

| Id | Name | Subclass of | Corresponds to in CRMarchaeo |
|---|---|---|---|
| U1 | Archaeological Survey | E7 Activity | A9 Archaeological Excavation |
| U2 | Survey Collection Activity | S19 Encounter Event, S2 Sample Taking | |
| U3 | Survey Process Unit | S19 Encounter Event | A1 Excavation Processing Unit |
| U4 | Survey Surface Unit | S20 Rigid Physical Feature | A2 Stratigraphic Volume Unit |
| U5 | Digitization Process Unit | D2 Digitization Process (CRMdig), S19 | |
| U6 | Material Sample | S13 Sample, E18 Physical Thing | |
| U7 to U11 | Fabric, Function, Ware, Shape, Vessel Part | E55 Type | |

| Id | Name | Domain | Range |
|---|---|---|---|
| UP1 | has observation affecting parameter | S4 Observation | E55 Type |
| UP2 | surveyed | U3 | U4 |
| UP3 | collected | U2 | U6 |

Version 1.0.1 also had UP4 to UP8, "contains part of type fabric / function / ware / shape / vessel part", E18 to U7 to U11.
They are gone from the 1.1 RDF although the 2024 slides still show them.

## Compatibility with the files in ../

It does not load against our set as shipped. Three reasons.

| Problem | Detail |
|---|---|
| Base versions | Built on CRM 6.2, CRMsci 1.2.3, CRMarchaeo 1.4.1, CRMdig 3.2.1. Ours are CRM 7.1.3, CRMsci 3.2, CRMarchaeo 2.1.1 |
| Namespaces | It refers to CRMsci as http://www.cidoc-crm.org/cidoc-crm/CRMsci/ . CRMsci 3.2 uses http://www.cidoc-crm.org/extensions/crmsci/ . The base CRM URIs (http://www.cidoc-crm.org/cidoc-crm/) do match |
| Renamed classes | UP1 has domain S4 Observation. In CRMsci 3.2, S4 is Single Observation and the general class is S27 Observation. O19 "has found object" is now "encountered object" |
| RDFS, not OWL | Both files declare rdfs:Class and rdf:Property only, no owl:Class, no owl:Ontology header, no imports. Same as the v2 RDFS files. Protégé needs an OWL conversion with a header and owl:imports of CRM 7.1.3 and CRMsci 3.2 |

S2, S13, S19, S20 all still exist in CRMsci 3.2, so the superclasses survive. CRMdig D2 is not in our set.
A port to 7.1.3 is a small, mechanical job: convert RDFS to OWL with a header and imports, rewrite the CRMsci namespace, point UP1 at S27 or S4 as decided, drop or replace D2, and record each change.
That port, with its decision log, is a legitimate piece of the thesis.

## What the 2020 paper says that the ontology does not

Open issues the authors name and which still matter for a Turkish survey profile:

- Survey Site against Survey Unit: a unit is declarative space, a site is a material concentration. Collecting from each has to be modelled differently. A unit can become a site.
- Collecting as sampling: CRMsci's Sample is an amount of matter from a material substantial, not a bag of objects. U6 Material Sample is their answer.
- The empty bag: a systematic collection that found nothing. Negatives are unresolved in CRM.
- Record taking is broader than any one CRM class: measurement, attribute assignment, type assignment, production of images.
- Coverage is a dimension, Visibility was first modelled as a condition state and later became the observation-affecting parameter UP1.

## Why it matters here

- It is the only extension anyone has written for survey. Citing it and porting it beats inventing a survey profile from CRMsci alone.
- Its motive is FAIR survey data, in those words, from 2016. The same framing as the thesis. The Dutch group is the obvious reference group and possibly a contact.
- Their three mapped survey databases and the Groningen archive at DANS are the closest existing precedent for mapping finished survey records such as Karaburun.
