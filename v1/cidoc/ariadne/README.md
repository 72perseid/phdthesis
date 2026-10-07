# ARIADNE review and compatibility check (2026-09-29)

Question: how does ARIADNE handle excavation data, and is what we produced compatible with it?

## Sources read

| Source | What it is |
| --- | --- |
| AO-Cat v1.2, March 2023, doi:10.5281/zenodo.7818375 | specification of the ARIADNE catalogue ontology: classes, properties, obligations |
| ARIADNEplus D4.4, Final report on ontology implementation, doi:10.5281/zenodo.7636720 | application profiles; section 5 is the excavation case study |
| ARIADNEplus D4.4.12, Final Report of the Archaeological Excavation Modelling Working Group, doi:10.5281/zenodo.7377910 | report plus Annex B (semantic patterns), C (open semantic issues), D (19 questions) |
| Katsianis et al., Semantic Modelling of Archaeological Excavation Data, Internet Archaeology 64, doi:10.11141/ia.64.12 | review and roadmap |
| Richards, Joined up Thinking, Internet Archaeology 64, doi:10.11141/ia.64.3 | how aggregation worked for providers |
| Bardi et al., The ARIADNEplus Knowledge Base, CEUR-WS Vol-3741 paper 16 | the aggregation pipeline and knowledge base |

Not read in detail yet: Annex B (61 pages of patterns), only its table of contents.
The ARIADNE portal itself could not be inspected (page renders by script).

## Two levels in ARIADNE

1. Catalogue level, AO-Cat. Describes a data resource (dataset, report, record) for discovery by
   What / Where / When / Who. Fixed and stable. Providers map their metadata with the 3M / X3ML tool,
   map subject terms to Getty AAT, define periods in PeriodO, and give WGS84 coordinates.
2. Item level for excavations. No application profile exists. The working group set out to write one
   (2020-22) and decided against it; it left pattern recipes, open issues and test questions instead.

## Tests

    ../../../.venv/bin/python aocat_coverage.py ../data/yumuktepe_2024.json
    ../../../.venv/bin/python wg_questions.py ../out/seleukeia_sidera_2024.ttl ../out/yumuktepe_2024.ttl

| Test | Seleukeia Sidera | Yumuktepe |
| --- | --- | --- |
| AO-Cat mandatory fields held / derivable / missing (of 19) | 10 / 6 / 3 | 10 / 6 / 3 |
| Working group questions answered by THEIR path as written (of 17 rows) | 2 | 2 |
| Same questions answered by OUR path | 11 | 16 |

Missing for the catalogue: access rights, Getty AAT mapping, country code; also coordinates and PeriodO
links, which the portal needs for map and period search.

Item level: same ontologies, different modelling choices. Examples: they link site to things with
AP21 contains, we use part-of and location; a trench is a place for them, a feature for us; they
model the animal a bone is part of, we type the bones with the taxon; they use S3 Measurement by
Sampling, we keep S2 Sample Taking and S4 Observation apart; they link feature to period with P8i,
we go through a production event.
