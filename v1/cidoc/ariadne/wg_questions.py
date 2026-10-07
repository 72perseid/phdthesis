#!/usr/bin/env python3
"""
wg_questions.py - Can our graphs answer the questions of the ARIADNEplus
Archaeological Excavation Modelling Working Group (D4.4.12, Annex D)?

For each of the 19 questions the script runs two SPARQL patterns:
  theirs  the semantic path written in Annex D, with property names updated to
          the current official releases (CRMsci 3.2, CRMarchaeo 2.1.1), and
          with the search term removed so that only the PATH is tested
  ours    the path that reaches the same information in our graphs
No inference is applied.  'rdfs' in the verdict means the two paths differ only
by a sub-property or sub-class, so an RDFS reasoner would reconcile them.

  python wg_questions.py ../out/seleukeia_sidera_2024.ttl ../out/yumuktepe_2024.ttl
"""
import logging
import sys
from rdflib import Graph

logging.getLogger("rdflib.term").setLevel(logging.ERROR)
PFX = """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX a: <http://www.cidoc-crm.org/extensions/crmarchaeo/>
PREFIX s: <http://www.cidoc-crm.org/extensions/crmsci/>
PREFIX t: <https://example.org/kst45/type/>
PREFIX kst: <https://example.org/kst45/vocab/>
"""
SITE_OURS = "?x (crm:P46i_forms_part_of|crm:P53_has_former_or_current_location/crm:P53i_is_former_or_current_location_of)+ ?site . ?site a crm:E27_Site ."
DATE_THEIRS = "?x crm:P92i_was_brought_into_existence_by/crm:P10_falls_within ?per ."
DATE_OURS = "?x crm:P108i_was_produced_by/crm:P10_falls_within ?per ."

Q = [
 ("Q1/Q4", "typed and dated objects of a site (palaeolithic blades, gallo-roman ceramic)",
  f"?site a crm:E27_Site ; a:AP21_contains ?x . ?x crm:P2_has_type ?ty . {DATE_THEIRS}",
  f"?x a crm:E22_Human-Made_Object ; crm:P2_has_type ?ty . {DATE_OURS} {SITE_OURS}",
  "site link: they use AP21 contains, we use part-of and location; dating differs only by sub-property (rdfs)"),
 ("Q2", "typed and dated features of a site (neolithic postholes)",
  f"?site a crm:E27_Site ; a:AP21_contains ?x . ?x a crm:E25_Human-Made_Feature ; crm:P2_has_type ?ty . {DATE_THEIRS}",
  f"?x a crm:E25_Human-Made_Feature ; crm:P2_has_type ?ty . {DATE_OURS} {SITE_OURS}",
  "same as Q1"),
 ("Q3", "contexts by soil texture",
  "?site a:AP21_contains ?x . ?x a a:A8_Stratigraphic_Unit ; crm:P43_has_dimension ?d . ?d crm:P2_has_type/crm:P2_has_type ?kind .",
  "?x a a:A2_Stratigraphic_Volume_Unit ; crm:P43_has_dimension ?d . ?d crm:P2_has_type/crm:P127_has_broader_term ?kind .",
  "the papers describe soil only in running text; we keep it in the label, not as a typed value"),
 ("Q5/Q6", "objects discovered during the excavation of a given year",
  "?site a crm:E27_Site ; crm:P8i_witnessed ?e . ?e a s:S19_Encounter_Event ; s:O19_encountered_object ?x ; crm:P4_has_time_span/crm:P82a_begin_of_the_begin ?b .",
  "?e a s:S19_Encounter_Event ; s:O19_encountered_object ?x ; crm:P4_has_time_span/crm:P82a_begin_of_the_begin ?b .",
  "encounter and date match; they tie the encounter to the site with P8, we tie it to a place with P7"),
 ("Q7", "objects found during an excavation led by a person",
  "?e a s:S19_Encounter_Event ; s:O19_encountered_object ?x ; crm:P14_carried_out_by ?p . ?p a crm:E21_Person .",
  "?e a s:S19_Encounter_Event ; s:O19_encountered_object ?x ; crm:P9i_forms_part_of+ ?act . ?act crm:P14_carried_out_by ?p . ?p a crm:E21_Person .",
  "we put people on the campaign, not on each encounter; the paper never says who found what"),
 ("Q8", "site located at a place",
  "?x a crm:E27_Site ; crm:P55_has_current_location ?pl .",
  "?x a crm:E27_Site ; crm:P53_has_former_or_current_location ?pl .",
  "we use the more general P53; P55 is its sub-property, so inference does not help in this direction"),
 ("Q9", "animal bones of a genus",
  "?x a crm:E20_Biological_Object ; crm:P2_has_type ?ty ; crm:P46i_forms_part_of ?ind . ?ind a crm:E20_Biological_Object ; crm:P2_has_type ?genus . ?x s:O19i_was_object_encountered_at ?e .",
  "?x a crm:E20_Biological_Object ; crm:P2_has_type ?genus ; s:O19i_was_object_encountered_at ?e . ?genus crm:P127_has_broader_term t:taxon .",
  "they model the animal as a whole the bone is part of; we attach the taxon to the bones as a type"),
 ("Q10", "objects that are parts of a feature with a given use (roman roads)",
  "?e s:O19_encountered_object ?x . ?x crm:P46i_forms_part_of ?f . ?f a crm:E25_Human-Made_Feature ; crm:P101_had_as_general_use ?use .",
  "?e s:O19_encountered_object ?x . ?x crm:P53_has_former_or_current_location/crm:P53i_is_former_or_current_location_of ?f . ?f a crm:E25_Human-Made_Feature ; crm:P2_has_type ?use .",
  "we never state general use (P101); function is a type or an interpretation"),
 ("Q11", "features of a period (burials of classical period)",
  "?x a crm:E25_Human-Made_Feature ; crm:P2_has_type ?ty ; crm:P8i_witnessed ?per . ?per a crm:E4_Period .",
  f"?x a crm:E25_Human-Made_Feature ; crm:P2_has_type ?ty . {DATE_OURS}",
  "they link feature to period directly (P8i); we go through a production event"),
 ("Q12", "features composed of typed objects (floors with mosaics)",
  "?f a crm:E25_Human-Made_Feature ; crm:P46_is_composed_of ?x . ?x a crm:E22_Human-Made_Object ; crm:P2_has_type ?ty .",
  "?f crm:P46_is_composed_of ?x . ?x crm:P2_has_type ?ty .",
  "our finds are located at features, not parts of them"),
 ("Q13", "stratigraphic units of a site belonging to a period",
  "?x a a:A2_Stratigraphic_Volume_Unit ; s:O19i_was_object_encountered_at ?e . ?e crm:P8_took_place_on_or_within ?site . ?site crm:P8i_witnessed ?per .",
  f"?x a a:A2_Stratigraphic_Volume_Unit . {DATE_OURS}",
  "we do not record an encounter event for deposits, only for finds"),
 ("Q14", "documents of an excavation created in a given year",
  "?x a crm:E31_Document ; crm:P70_documents ?e ; crm:P94i_was_created_by/crm:P4_has_time_span/crm:P82a_begin_of_the_begin ?b . ?e a s:S19_Encounter_Event .",
  "?x a crm:E31_Document ; crm:P70_documents ?e ; crm:P94i_was_created_by/crm:P4_has_time_span/crm:P82a_begin_of_the_begin ?b . ?e a s:S19_Encounter_Event .",
  "identical path; the report is the only document, figures are visual items"),
 ("Q15", "items with a measured value",
  "?x s:O19i_was_object_encountered_at ?e ; crm:P39i_was_measured_by ?m . ?m a crm:E16_Measurement ; crm:P40_observed_dimension ?d . ?d crm:P2_has_type ?kind .",
  "?x s:O19i_was_object_encountered_at ?e ; crm:P43_has_dimension ?d . ?d crm:P2_has_type ?kind ; crm:P90_has_value ?v .",
  "we attach the dimension to the thing; they insert the measuring activity"),
 ("Q16", "features inside trenches",
  "?x a crm:E25_Human-Made_Feature ; crm:P46i_forms_part_of ?site ; crm:P53_has_former_or_current_location ?pl ; s:O19i_was_object_encountered_at ?e . ?pl crm:P2_has_type ?trench .",
  "?x a crm:E25_Human-Made_Feature ; crm:P46i_forms_part_of ?tr . ?tr crm:P2_has_type t:trench .",
  "for them a trench is a place; for us it is a feature that contexts are part of"),
 ("Q17", "samples and what they contain (legume seeds)",
  "?site a crm:E27_Site ; s:O3i_was_sampled_by ?st . ?st a s:S2_Sample_Taking ; s:O5_removed ?x . ?x a s:S13_Sample ; s:O25_contains ?c . ?c crm:P2_has_type ?ty .",
  "?st a s:S2_Sample_Taking ; s:O3_sampled_from ?src ; s:O5_removed ?x . ?x a s:S13_Sample ; crm:P2_has_type ?ty .",
  "same classes; they sample the site and nest the seeds inside the sample, we sample the context and type the sample"),
 ("Q18", "excavation events within a date range",
  "?x a s:S19_Encounter_Event ; crm:P4_has_time_span ?ts . ?ts crm:P82a_begin_of_the_begin ?b ; crm:P82b_end_of_the_end ?en .",
  "?x a s:S19_Encounter_Event ; crm:P4_has_time_span ?ts . ?ts crm:P82a_begin_of_the_begin ?b ; crm:P82b_end_of_the_end ?en .",
  "identical, but the papers give only the year"),
 ("Q19", "excavations with radiocarbon samples",
  "?site s:O3i_was_sampled_by ?m . ?m a s:S3_Measurement_by_Sampling ; crm:P2_has_type ?ty ; s:O5_removed ?x . ?x a s:S13_Sample .",
  "?obs a s:S4_Single_Observation ; crm:P2_has_type ?ty ; s:O8_observed ?x . ?x a s:S13_Sample ; s:O5i_was_removed_by ?st .",
  "they merge taking and measuring into one S3 event; we keep sample taking (S2) and analysis (S4) apart"),
]

graphs = [(p.split("/")[-1].replace(".ttl", ""), Graph().parse(p)) for p in sys.argv[1:]]
print(f"{'question':<7} {'topic':<58} " + " ".join(f"{n[:14]+' theirs':>22}{n[:14]+' ours':>20}" for n, _ in graphs))
totals = {n: [0, 0] for n, _ in graphs}
for qid, topic, theirs, ours, why in Q:
    cells = []
    for name, g in graphs:
        a = int(list(g.query(PFX + "SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE { " + theirs + " }"))[0][0])
        b = int(list(g.query(PFX + "SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE { " + ours + " }"))[0][0])
        totals[name][0] += a > 0
        totals[name][1] += b > 0
        cells.append(f"{a:>22}{b:>20}")
    print(f"{qid:<7} {topic[:58]:<58} " + " ".join(cells))
    print(f"        -> {why}")
print()
for name, (a, b) in totals.items():
    print(f"{name}: {a} of {len(Q)} questions answered by their path as written, {b} of {len(Q)} by our own path")
