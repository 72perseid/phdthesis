# Version 3: hand annotation in Protégé

Started 2026-10-09. Aim: annotate a few finds from the KST papers by hand
against CIDOC CRM, watch the steps, and write the procedure down from that.
No database, no code until the procedure is clear.

## Files

| File | What it is |
|------|------------|
| `ontology/kst_annotation.owl` | Open this in Protégé. Empty ontology that imports the four below; individuals go here. |
| `ontology/CIDOC_CRM_v7.1.3.owl` | CIDOC CRM 7.1.3, official OWL DL implementation by FORTH-ICS (Feb 2024). 76 classes, 290 object properties, 19 datatype properties. Labels in en, de, el, fr, pt, ru, zh. |
| `ontology/CRMsci_v3.2.owl` | Scientific observation (S4 Observation, S13 Sample, S2 Sample Taking). 28 classes. |
| `ontology/CRMarchaeo_v2.1.1.owl` | Excavation (A1 Excavation Processing Unit, A8 Stratigraphic Unit, A9 Archaeological Excavation). 10 classes. |
| `ontology/CRMinf_v1.2.1.owl` | Argumentation (I1 Argumentation, I2 Belief, I4 Proposition Set). 14 classes. |
| `ontology/CRMgeo_v2.0.1.owl` | Space and time. Downloaded but **not imported** because it imports GeoSPARQL and WGS84 from the web. |
| `ontology/catalog-v001.xml` | Protégé reads it automatically; maps the `owl:imports` IRIs to the local files so nothing is fetched from the web. |

## Where the files come from

All from https://cidoc-crm.org, licence CC BY 4.0, produced by FORTH-ICS:

- CRM: https://cidoc-crm.org/versions-of-the-cidoc-crm, row 7.1.3, link "owl"
  (`https://cidoc-crm.org/owl/7.1.3/CIDOC_CRM_v7.1.3.owl`)
- Extensions: each model's version page has an "OWL" link, e.g.
  https://www.cidoc-crm.org/crmarchaeo/ModelVersion/version-2.1.1
  (`https://cidoc-crm.org/extensions/crmarchaeo/owl/2.1.1/CRMarchaeo_v2.1.1.owl`)
- Source repository: https://gitlab.isl.ics.forth.gr/cidoc-crm

Version 2 used the **RDFS** files from the same site (`v2/ontology/*.rdf`).
Those declare `rdfs:Class` and `rdf:Property` only; they were read with rdflib
in Python for domain and range checks, never opened in Protégé. The OWL files
here carry the same classes and properties, typed as `owl:Class`,
`owl:ObjectProperty` and `owl:DatatypeProperty`, which is what Protégé expects.

## Known quirk

CRMarchaeo 2.1.1 still imports CRM 7.1.2 and CRMsci 2.0 in its header. The
catalog redirects both to the 7.1.3 and 3.2 files. If Protégé complains about
an unresolved import, check that `catalog-v001.xml` sits next to the opened file.
