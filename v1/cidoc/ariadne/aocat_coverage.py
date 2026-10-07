#!/usr/bin/env python3
"""
aocat_coverage.py - Can a report record fill the ARIADNE catalogue (AO-Cat v1.2)?

AO-Cat describes a data resource for discovery (What / Where / When / Who).
For every AO-Cat property of AO_Data_Resource and its spatial and temporal
regions, this script says whether our record holds the value, could derive it,
or lacks it.  Obligations are taken from AO-Cat v1.2, Appendix 2
(doi:10.5281/zenodo.7818375).

  python aocat_coverage.py ../data/yumuktepe_2024.json
"""
import json
import sys
from pathlib import Path

rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
doc = rec["document"]
places = rec.get("places", [])
periods = rec.get("periods", [])
types = sorted({x.get("type") for k in ("features", "finds") for x in rec.get(k, []) if x.get("type")})
dated = [p for p in periods if p.get("begin") or p.get("end")]

HAVE, DERIVE, MISSING = "have", "derivable", "MISSING"
rows = [
    # property, obligation, status, what we have / what is needed
    ("has_title", "mandatory", HAVE, doc["title"][:60]),
    ("has_description", "optional", DERIVE, "no abstract in the record; could be generated from the campaign note"),
    ("has_type", "mandatory", DERIVE, "'excavation report' is recorded; must be one AO_Concept"),
    ("has_original_id", "mandatory", HAVE, f"{rec['base_uri']}document/{doc['id']}"),
    ("has_identifier", "optional", HAVE if doc.get("volume", {}).get("isbn") else MISSING, "ISBN of the volume; the paper has no DOI"),
    ("has_language", "mandatory", HAVE, doc.get("language")),
    ("has_creator", "mandatory", HAVE, f"{len(doc['authors'])} authors"),
    ("has_publisher", "mandatory", HAVE if doc.get("volume", {}).get("publisher") else MISSING, doc.get("volume", {}).get("publisher")),
    ("has_contributor", "mandatory", DERIVE, "in ARIADNE this is the body supplying the record; not in the paper"),
    ("has_owner", "mandatory", DERIVE, "rights holder; KST states copyright passes to KVMGM, not recorded by us"),
    ("has_responsible", "mandatory", DERIVE, "scientifically responsible person; director if the paper names one"),
    ("was_issued / was_modified", "mandatory", DERIVE, "dates of the catalogue record, set at aggregation time"),
    ("was_created_on", "mandatory", HAVE if doc.get("published") else MISSING, doc.get("published")),
    ("has_access_rights", "mandatory", MISSING, "licence / access statement is not recorded"),
    ("has_landing_page", "optional", MISSING, "no URL of the published paper recorded"),
    ("has_ARIADNE_subject", "mandatory", DERIVE, "one of the ARIADNE categories, e.g. 'Fieldwork report'"),
    ("has_native_subject", "mandatory", HAVE, f"{len(types)} local type terms (coin, oven, pithos ...)"),
    ("has_derived_subject (Getty AAT)", "mandatory", MISSING, "no term is mapped to AAT; all types are local labels"),
    ("has_spatial_coverage", "mandatory", HAVE, f"{len(places)} named places"),
    ("  has_place_name", "mandatory", HAVE, places[0]["label"] if places else None),
    ("  has_country_code", "mandatory", MISSING, "country never recorded (papers assume Türkiye)"),
    ("  has_latitude / has_longitude (WGS84)", "needed for map search", MISSING, "no coordinates anywhere in the record"),
    ("has_temporal_coverage", "optional but drives 'When' search", HAVE, f"{len(periods)} period labels"),
    ("  has_native_period", "mandatory", HAVE, ", ".join(p["label"] for p in periods[:3]) + " ..."),
    ("  has_period (PeriodO)", "needed for cross-collection search", MISSING, "no period is linked to a PeriodO definition"),
    ("  from / until (xsd:gYear)", "optional", HAVE if dated else MISSING, f"{len(dated)} of {len(periods)} periods carry years"),
]
w = max(len(r[0]) for r in rows)
print(f"AO-Cat coverage for: {doc['title']}\n")
print(f"{'AO-Cat property':<{w}}  {'obligation':<36} {'status':<10} note")
print("-" * (w + 100))
for prop, obl, status, note in rows:
    print(f"{prop:<{w}}  {obl:<36} {status:<10} {note}")
mand = [r for r in rows if r[1] == "mandatory"]
print(f"\nmandatory fields: {sum(r[2]==HAVE for r in mand)} held, {sum(r[2]==DERIVE for r in mand)} derivable, "
      f"{sum(r[2]==MISSING for r in mand)} missing, of {len(mand)}")
print("not mandatory but required for the portal's map and period search: coordinates, PeriodO links")
