#!/usr/bin/env python3
"""
make_survey_figure.py - one survey unit as a CIDOC CRM graph, hand-written example.

  python3 make_survey_figure.py

Writes survey_example_tr.png and survey_example_en.png. The example is invented
for illustration: a walked unit, its visibility, a collected bag, one diagnostic
sherd, and a dating that is stored as an interpretation with its author and grounds.
Classes are from CIDOC CRM 7.1.3 and CRMsci 3.2 only.
"""
from __future__ import annotations
import subprocess
from pathlib import Path

HERE = Path(__file__).parent

COL = {
    "E7": "#fad7a0", "S19": "#f5b7b1", "E13": "#f5b7b1",
    "E53": "#d5f5e3", "E19": "#aed6f1", "E22": "#aed6f1",
    "E54": "#eeeeee", "E55": "#eeeeee", "E57": "#eeeeee",
    "E4": "#d7bde2", "E52": "#d7bde2", "E21": "#fdebd0", "E74": "#fdebd0", "E31": "#fdebd0",
}

# id: (class, turkish label, english label)
NODES = {
    "survey": ("E7_Activity", "Tokat Erbaa Yüzey Araştırması\n2027 sezonu", "Tokat Erbaa Survey\n2027 season"),
    "team": ("E74_Group", "Ekip A", "Team A"),
    "walk": ("S19_Encounter_Event", "Birim 12'nin yürünmesi\n14 Temmuz 2027", "Walking of unit 12\n14 July 2027"),
    "unit": ("E53_Place", "Birim 12", "Unit 12"),
    "district": ("E53_Place", "Erbaa ilçesi", "Erbaa district"),
    "vis": ("E54_Dimension", "Görünürlük: 60 %", "Visibility: 60 %"),
    "bag": ("E19_Physical_Object", "Torba 12.01\n23 seramik parçası", "Bag 12.01\n23 sherds"),
    "bagtype": ("E55_Type", "sistematik yüzey toplaması", "systematic surface collection"),
    "sherd": ("E22_Human-Made_Object", "Parça 12.01.3", "Sherd 12.01.3"),
    "part": ("E55_Type", "ağız parçası", "rim"),
    "mat": ("E57_Material", "pişmiş toprak", "fired clay"),
    "dating": ("E13_Attribute_Assignment", "Tarihleme\nkesinlik: olası", "Dating\ncertainty: probable"),
    "person": ("E21_Person", "S. Ünlüsoy", "S. Ünlüsoy"),
    "grounds": ("E31_Document", "biçim benzerliği:\nHayes 1972, form 3", "form parallel:\nHayes 1972, form 3"),
    "period": ("E4_Period", "Geç Roma Dönemi", "Late Roman period"),
    "span": ("E52_Time-Span", "MS 300 – 450", "AD 300 – 450"),
}

EDGES = [
    ("survey", "walk", "P9_consists_of"),
    ("walk", "team", "P14_carried_out_by"),
    ("walk", "unit", "O21_encountered_at"),
    ("unit", "district", "P89_falls_within"),
    ("walk", "vis", "O16_observed_value"),
    ("walk", "bag", "O19_encountered_object"),
    ("bag", "bagtype", "P2_has_type"),
    ("sherd", "bag", "P46i_forms_part_of"),
    ("sherd", "part", "P2_has_type"),
    ("sherd", "mat", "P45_consists_of"),
    ("dating", "sherd", "P140_assigned_attribute_to"),
    ("dating", "period", "P141_assigned"),
    ("dating", "person", "P14_carried_out_by"),
    ("dating", "grounds", "P17_was_motivated_by"),
    ("period", "span", "P4_has_time-span"),
]

LEGEND = {
    "tr": "Kutular varlık, oklar ilişkidir. Pembe: olaylar ve yorumlar. Mavi: nesneler. Yeşil: yerler. Mor: dönem ve zaman. Gri: tür, malzeme, ölçüm. Bej: kişi, ekip, kaynak.",
    "en": "Boxes are entities, arrows are relations. Pink: events and interpretations. Blue: objects. Green: places. Purple: period and time. Grey: type, material, measurement. Beige: person, team, source.",
}


def build(lang: str) -> None:
    idx = 1 if lang == "tr" else 2
    lines = [
        "digraph survey {",
        '  rankdir=TB; dpi=200; nodesep=0.3; ranksep=0.55; labelloc="b"; fontname="DejaVu Sans"; fontsize=9;',
        f'  label="{LEGEND[lang]}";',
        '  node [shape=box, style="filled,rounded", fontname="DejaVu Sans", fontsize=10, margin="0.12,0.06"];',
        '  edge [fontname="DejaVu Sans", fontsize=8, color="#555555"];',
    ]
    for nid, (cls, *labels) in NODES.items():
        text = labels[idx - 1].replace('"', "'") + "\n" + cls
        colour = COL[cls.split("_", 1)[0]]
        lines.append(f'  {nid} [label="{text}", fillcolor="{colour}"];')
    for s, o, p in EDGES:
        lines.append(f'  {s} -> {o} [label="{p}"];')
    lines.append("  { rank=same; unit; vis; bag; }")
    lines.append("  { rank=same; person; grounds; period; }")
    lines.append("}")
    dot = HERE / f"survey_example_{lang}.dot"
    dot.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["dot", "-Tpng", str(dot), "-o", str(HERE / f"survey_example_{lang}.png")], check=True)
    print("written:", dot.with_suffix(".png").name)


if __name__ == "__main__":
    build("tr")
    build("en")
