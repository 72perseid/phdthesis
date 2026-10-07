#!/usr/bin/env python3
"""Write data/sinekkaya_2024.json.

The record was made by close reading of the paper.  Only Tablo 2 (chipped stone
counts) is read by program, with tools/parse_count_table.py, so that 60 cells
are not typed by hand.

The record says what the paper says.  Fields that the record format did not
have when this paper was read are marked NEW below.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from build_graph import slug  # noqa: E402
from parse_count_table import parse  # noqa: E402

AUTHORS = ["dincer", "sahin", "tugutlu", "icel"]
P = lambda *n: list(n)  # noqa: E731  pages

actors = [
    {"id": "dincer", "class": "E21_Person", "label": "Berkay Dinçer", "orcid": "0000-0001-8240-5973", "member_of": "iu-antropoloji", "pages": P(197)},
    {"id": "sahin", "class": "E21_Person", "label": "Serkan Şahin", "orcid": "0000-0002-5137-805X", "member_of": "kaeu-antropoloji", "pages": P(197)},
    {"id": "tugutlu", "class": "E21_Person", "label": "Eylem Tuğutlu", "member_of": "bursa-muzesi", "pages": P(197)},
    {"id": "icel", "class": "E21_Person", "label": "Zeynep İçel", "member_of": "iu-antropoloji", "pages": P(197)},
    {"id": "iu-antropoloji", "class": "E74_Group", "label": "İstanbul Üniversitesi, Edebiyat Fakültesi, Antropoloji Bölümü", "pages": P(197, 202)},
    {"id": "kaeu-antropoloji", "class": "E74_Group", "label": "Kırşehir Ahi Evran Üniversitesi, Fen-Edebiyat Fakültesi, Antropoloji Bölümü", "pages": P(197, 203)},
    {"id": "bursa-muzesi", "class": "E74_Group", "label": "Bursa Arkeoloji Müzesi Müdürlüğü", "pages": P(197)},
    {"id": "orhaneli-jandarma", "class": "E74_Group", "label": "Orhaneli İlçe Jandarma Komutanlığı", "pages": P(198, 202)},
    {"id": "orhaneli-belediye", "class": "E74_Group", "label": "Orhaneli Belediye Başkanlığı", "pages": P(202)},
    {"id": "orhaneli-kaymakamlik", "class": "E74_Group", "label": "Orhaneli Kaymakamlığı", "pages": P(202)},
    {"id": "beyce-kooperatif", "class": "E74_Group", "label": "Orhaneli/Beyce Kadın Kooperatifi", "pages": P(202)},
    {"id": "hacettepe-arkeoloji", "class": "E74_Group", "label": "Hacettepe Üniversitesi Arkeoloji Bölümü", "pages": P(202)},
    {"id": "mta", "class": "E74_Group", "label": "Maden Tetkik ve Arama Genel Müdürlüğü", "pages": P(202)},
    {"id": "ytu-mimarlik", "class": "E74_Group", "label": "Yıldız Teknik Üniversitesi Mimarlık Fakültesi", "pages": P(203)},
    {"id": "karahan", "class": "E21_Person", "label": "Göknur Karahan", "member_of": "hacettepe-arkeoloji", "pages": P(202)},
    {"id": "sagdic", "class": "E21_Person", "label": "Dilber Sağdıç", "member_of": "mta", "pages": P(202)},
    {"id": "yasar", "class": "E21_Person", "label": "Canan R. Yaşar", "member_of": "kaeu-antropoloji", "pages": P(203)},
    {"id": "kaya", "class": "E21_Person", "label": "Özlem Kaya", "member_of": "ytu-mimarlik", "pages": P(203)},
    {"id": "atesogullari", "class": "E21_Person", "label": "Soner Ateşoğulları"},
    {"id": "kvmgm", "class": "E74_Group", "label": "Kültür Varlıkları ve Müzeler Genel Müdürlüğü"},
]
STUDENTS = [("bekci", "Aleyna Bekçi"), ("arslan-zr", "Z. Rüveyda Arslan"), ("kilictas", "Büşra Kılıçtaş"),
            ("dilmen", "Sude N. Dilmen"), ("takci", "Ezgi Takcı"), ("arslan-yn", "Yaren N. Arslan"),
            ("capar", "Beyza N. Çapar"), ("dogu", "Elif Ç. Doğu"), ("akman", "A. Sena Akman")]
for ident, name in STUDENTS:
    actors.append({"id": ident, "class": "E21_Person", "label": name, "member_of": "iu-antropoloji",
                   "note": "İstanbul Üniversitesi Antropoloji Bölümü öğrencisi veya mezunu", "pages": P(202)})
TEAM = ["karahan"] + [s[0] for s in STUDENTS] + ["sagdic", "yasar", "kaya"]

places = [
    {"id": "bati-anadolu", "label": "Batı Anadolu", "type": "region", "pages": P(197)},
    {"id": "bursa", "label": "Bursa", "type": "province", "within": "bati-anadolu", "pages": P(197)},
    {"id": "orhaneli", "label": "Orhaneli", "type": "district", "within": "bursa", "pages": P(197)},
    {"id": "girencik", "label": "Girencik", "type": "neighbourhood", "within": "orhaneli", "pages": P(197)},
    {"id": "kusumlar", "label": "Kusumlar", "type": "neighbourhood", "within": "orhaneli", "pages": P(197)},
    {"id": "sinekkaya", "label": "Sinekkaya Mağarası (konum)", "type": "cave location", "within": "orhaneli",
     "note": "Girencik ve Kusumlar mahalleleri arasında.", "pages": P(197)},
]

periods = [
    {"id": "palaeolithic", "label": "Paleolitik Çağ", "pages": P(197)},
    {"id": "middle-palaeolithic", "label": "Orta Paleolitik Dönem", "within": "palaeolithic", "pages": P(197, 199)},
    {"id": "upper-palaeolithic", "label": "Üst Paleolitik Dönem", "within": "palaeolithic", "pages": P(197, 199)},
    {"id": "epipalaeolithic", "label": "Epipaleolitik Dönem", "pages": P(199)},
    {"id": "neolithic", "label": "Neolitik Dönem", "pages": P(197, 198)},
    {"id": "pleistocene", "label": "Pleyistosen", "pages": P(198, 202)},
    {"id": "holocene", "label": "Holosen", "pages": P(198)},
    {"id": "republic", "label": "Cumhuriyet Dönemi", "pages": P(201, 202)},
    {"id": "recent", "label": "Yakın dönem (olasılıkla son 50-60 yıl)", "pages": P(198)},
]

features = [
    {"id": "site", "class": "E27_Site", "label": "Sinekkaya Mağarası", "type": "cave", "location": "sinekkaya",
     "figures": ["resim-1"], "pages": P(197)},
    {"id": "area-a", "class": "E25_Human-Made_Feature", "label": "A alanı", "identifier": "A", "type": "excavation area", "part_of": "site", "pages": P(198)},
    {"id": "area-b", "class": "E25_Human-Made_Feature", "label": "B alanı", "identifier": "B", "type": "excavation area", "part_of": "site", "figures": ["resim-2"], "pages": P(198)},
    {"id": "area-c", "class": "E25_Human-Made_Feature", "label": "C alanı", "identifier": "C", "type": "excavation area", "part_of": "site", "figures": ["resim-2"], "pages": P(198)},
    {"id": "hearth-f1-5", "class": "E25_Human-Made_Feature", "label": "F1-5 birimindeki ocak", "type": "hearth", "part_of": "area-a",
     "periods": ["recent"], "dating_certainty": "uncertain",                                                       # NEW dating_certainty
     "note": "Metin yakın dönemde yakılmış ateş ve ocak yerlerinden söz eder; Resim 3 alt yazısı ocağı F1-5 birimine yerleştirir.",
     "figures": ["resim-3"], "pages": P(198, 205)},
]

UNITS = [  # Tablo 1, as printed
    ("f1-1", "F1.1", "area-a", "En üstteki sıvalı gibi sertleşmiş birim.", None),
    ("f1-2", "F1.2", "area-c", "En üstteki sıvalı gibi sertleşmiş birim.", None),
    ("f1-3", "F1.3", "area-b", "En üstteki yanık, küllü alan.", None),
    ("f1-4", "F1.4", "area-a", "F1.1 altında yer alan sıvalı gibi sertleşmiş birim.", None),
    ("f1-5", "F1.5", "area-a", "A alanında sertleşmiş dolgunun altındaki yumuşak dolgu.",
     "Hangi sertleşmiş dolgunun (F1.1 veya F1.4) altında olduğu belirtilmemiştir; bu nedenle ilişki kaydedilmedi."),
    ("f1-6", "F1.6", "area-a", "Mağaranın duvar kenarında nem dolayısıyla sertleşerek konsolide olmuş dolgu.",
     "Kış aylarında buradan su akar. Fırça ile kazılmayan tek birim."),
    ("f1-7", "F1.7", "area-a", "Kanal.", None),
    ("f1-8", "F1.8", "area-a", "A'nın kuzey kenarındaki nispeten sertleşmiş, açık kahverengi renkli taşçık içeren, olasılıkla Holosen.", None),
    ("f1-9", "F1.9", "area-c", "F1-2'nin altındaki 'sıvalı' sertleşmiş dolgunun üst sıvası. 2 kat taban mevcut. İlki kum ve küçük taşçıklı.", None),
]
strata = [
    {"id": "unit-x", "class": "A2_Stratigraphic_Volume_Unit", "label": "X birimi (defineci atık toprağı)", "identifier": "X",
     "type": "looters' spoil", "at_feature": "site",
     "note": "Yumuşak, karışık malzeme içeren dolgu. 2023'te A, B ve C alanlarında kaldırıldı.", "pages": P(197, 198)},
    {"id": "layer-1", "class": "A2_Stratigraphic_Volume_Unit", "label": "1. Tabaka", "identifier": "1", "type": "layer",
     "at_feature": "site", "note": "Mağaranın en üst dolgusu. Küçükbaş hayvan dışkısı, yakın dönem ateş ve ocak yerleri içerir.",
     "pages": P(198, 202)},
]
for ident, code, area, text, note in UNITS:
    u = {"id": ident, "class": "A2_Stratigraphic_Volume_Unit", "label": f"{code}: {text}", "identifier": code,
         "type": "excavation unit (feature)", "at_feature": area,
         "part_of": "layer-1",                                                                                     # NEW part_of on strata
         "figures": ["tablo-1"], "pages": P(199)}
    if note:
        u["note"] = note
    if ident == "f1-8":
        u |= {"periods": ["holocene"], "dating_certainty": "uncertain"}
    if ident == "f1-7":
        u["figures"] += ["resim-4"]
    if ident == "f1-9":
        u["figures"] += ["resim-5"]
    strata.append(u)

relations = [
    {"id": "rel-x-layer1", "from": "unit-x", "to": "layer-1", "type": "overlies", "pages": P(198)},
    {"id": "rel-f11-f14", "from": "f1-1", "to": "f1-4", "type": "overlies", "pages": P(199)},
    {"id": "rel-f12-f19", "from": "f1-2", "to": "f1-9", "type": "overlies", "pages": P(199)},
]

references = [                                                                                                     # NEW list
    {"id": "dincer-2010", "citation": "Dinçer, B. (2010). Bursa ve Çevresi Yüzey Araştırmaları 2008-2009 Tarihöncesi Buluntuları, Arkeoloji ve Sanat, 134, s. 1-16.", "year": "2010", "pages": P(203)},
    {"id": "dincer-2024", "citation": "Dinçer, B., Durakoğlu, Ç., Şahin, S., Çilingiroğlu, Ç., Arcagök, İ., (2024). Sinekkaya Mağarası (Orhaneli-Bursa) Kazısı 2023. Kazı Sonuçları Toplantısı 44 (1), s. 299-312.", "year": "2024",
     "note": "Metinde 'Dinçer vd., 2025' olarak anılır; kaynakçada 2024 tarihlidir.", "pages": P(203)},
    {"id": "sahin-2011", "citation": "Şahin, M., Mert, İ. H., ve Şahin, D. (2011). Bursa ve Çevresi Yüzey Araştırması 2009 – Keles ve Orhaneli, Araştırma Sonuçları Toplantısı, 28 (1), s. 99-114.", "year": "2011", "pages": P(203)},
]

activities = [
    {"id": "survey-2009", "class": "E7_Activity", "type": "surface survey", "label": "Mağaranın tespiti (2009)",
     "timespan": {"begin": "2009", "end": "2009"}, "at_feature": "site",
     "sources": [{"ref": "dincer-2010", "pages": "10"}, {"ref": "sahin-2011", "pages": "105"}],                     # NEW sources
     "pages": P(197)},
    {"id": "looting", "class": "E7_Activity", "type": "illegal excavation", "label": "Yasadışı definecilik kazıları",
     "timespan": {"begin": "2009", "end": "2013"}, "at_feature": "site",
     "produced": ["unit-x"],                                                                                       # NEW produced
     "note": "2009-2013 arasında gerçekleştiği biliniyordu; 2024 kazısı geçmişinin bundan daha uzun olduğunu göstermiştir.",
     "pages": P(197, 202)},
    {"id": "campaign-2023", "class": "A9_Archaeological_Excavation", "type": "excavation campaign", "label": "Sinekkaya Mağarası 2023 kazısı",
     "timespan": {"begin": "2023", "end": "2023"}, "investigated": "site", "took_place_at": ["sinekkaya"],
     "carried_out_by": [{"actor": "bursa-muzesi", "role": "directing institution"}],
     "sources": [{"ref": "dincer-2024"}],
     "note": "İlk kazı sezonu. Hedef defineci tahribatındaki kültür varlıklarının kurtarılmasıydı.", "pages": P(197)},
    {"id": "exc-2023-x", "class": "A1_Excavation_Processing_Unit", "label": "X biriminin kaldırılması (2023)", "part_of": "campaign-2023",
     "at_feature": "area-a", "also_at": ["area-b", "area-c"], "removed": ["unit-x"], "pages": P(197, 198)},
    {"id": "sieving-2023", "class": "E7_Activity", "type": "sieving", "label": "Defineci dolgularının elenmesi (2023)", "part_of": "campaign-2023",
     "used": ["unit-x"], "pages": P(197)},
    {"id": "campaign-2024", "class": "A9_Archaeological_Excavation", "type": "excavation campaign", "label": "Sinekkaya Mağarası 2024 kazısı",
     "timespan": {"begin": "2024", "end": "2024"}, "investigated": "site", "took_place_at": ["sinekkaya"], "continued": ["campaign-2023"],
     "carried_out_by": [{"actor": a, "role": "author"} for a in AUTHORS] + [{"actor": a, "role": "team member"} for a in TEAM],
     "note": "Hedef in situ dolgulara ulaşmaktı; ulaşılamadı. 2024 için kazı başkanı metinde belirtilmemiştir.",
     "figures": ["resim-1", "resim-2"], "pages": P(198, 202)},
    {"id": "doc-3d", "class": "E7_Activity", "type": "photogrammetric documentation", "label": "Fotogrametri ile üç boyutlu belgeleme",
     "part_of": "campaign-2024", "at_feature": "site", "figures": ["resim-1"], "pages": P(198)},
    {"id": "doc-plan", "class": "E7_Activity", "type": "hand drawing", "label": "Elle çizim yöntemiyle plan çizimi",
     "part_of": "campaign-2024", "at_feature": "site", "pages": P(198)},
    {"id": "exc-2024", "class": "A1_Excavation_Processing_Unit", "type": "décapage excavation", "label": "A, B ve C alanlarında 1. tabaka kazısı (2024)",
     "part_of": "campaign-2024", "at_feature": "area-a", "also_at": ["area-b", "area-c"],
     "removed": [u[0] for u in UNITS],
     "excavated": [{"type": "number of buckets", "value": 871, "unit": "bucket"},                                   # NEW excavated
                   {"type": "volume per bucket", "value": 10, "unit": "l"},
                   {"type": "mass", "value": 0.871, "unit": "t"}],
     "note": "Birimler ayrı ayrı kazılmış ve tanımlanmıştır. F1.6 dışındaki birimler yalnızca fırça ile kazılmıştır. "
             "Basılı metinde 871 kova × 10 litre = 0,871 metrik ton olarak verilir; hacim ve kütle birbiriyle tutarlı görünmemektedir.",
     "figures": ["resim-2"], "pages": P(198, 199)},
    {"id": "sieving-2024", "class": "E7_Activity", "type": "dry sieving", "label": "Kazılan toprağın tamamının elenmesi (2024)",
     "part_of": "campaign-2024", "note": "2 mm kuru elek.", "pages": P(198)},
    {"id": "protection", "class": "E7_Activity", "type": "site protection", "label": "Mağaranın korunması",
     "carried_out_by": [{"actor": "orhaneli-jandarma", "role": "security"}], "at_feature": "site",
     "note": "2023 kazısından sonra mağaranın hiç tahrip edilmediği gözlemlenmiştir.", "pages": P(198, 202)},
    {"id": "support", "class": "E7_Activity", "type": "logistic support", "label": "Konaklama ve destek",
     "carried_out_by": [{"actor": "orhaneli-belediye", "role": "accommodation"}, {"actor": "orhaneli-kaymakamlik", "role": "support"},
                        {"actor": "beyce-kooperatif", "role": "support"}],
     "purpose_of": "campaign-2024", "pages": P(202)},
]

records = [                                                                                                        # NEW list
    {"id": "rec-3d-model", "type": "3D model", "label": "Mağaranın fotogrametrik üç boyutlu modeli", "made_by": "doc-3d",
     "depicts": ["site"], "figures": ["resim-1"], "pages": P(198)},
    {"id": "rec-plan", "type": "plan", "label": "Mağaranın planı", "scale": "1/50", "made_by": "doc-plan", "depicts": ["site"], "pages": P(198)},
]

# --- finds -------------------------------------------------------------------
LITHIC_TYPES = {
    "belirsiz": "indeterminate piece", "çekirdek": "core", "dilgi": "blade", "dilgicik": "bladelet", "doğal parça": "natural piece",
    "düzeltili doğal parça": "retouched natural piece", "éclat débordant": "éclat débordant", "éclat siret": "éclat siret",
    "uzun Levallois uç": "elongated Levallois point", "iki yüzeyli/çekirdek": "biface or core", "mikrolit": "microlith",
    "korteksli yonga": "cortical flake", "Levallois dilgi": "Levallois blade", "Levallois uç": "Levallois point",
    "Levallois yonga": "Levallois flake", "litik?": "possible lithic", "manuport": "manuport", "parça": "fragment",
    "pseudo Levallois uç": "pseudo-Levallois point", "vurgaç": "hammerstone", "yarı omurgalı dilgi": "semi-crested blade", "yonga": "flake",
}
ATTRIBUTION = {  # column of Tablo 2 -> periods, certainty
    "belirsiz": ([], None), "doğal": ([], None),
    "Epipaleolitik?": (["epipalaeolithic"], "uncertain"), "Neo-ÜP?": (["neolithic", "upper-palaeolithic"], "one of"),
    "Neolitik?": (["neolithic"], "uncertain"), "Neolitik": (["neolithic"], None), "OP": (["middle-palaeolithic"], None),
    "OP-ÜP?": (["middle-palaeolithic", "upper-palaeolithic"], "one of"), "OP?": (["middle-palaeolithic"], "uncertain"),
    "ÜP": (["upper-palaeolithic"], None), "ÜP-Epi?": (["upper-palaeolithic", "epipalaeolithic"], "one of"),
    "ÜP?": (["upper-palaeolithic"], "uncertain"),
}
COLUMNS = list(ATTRIBUTION)
text = (ROOT / "text/sinekkaya_2024.txt").read_text(encoding="utf-8").split("\f")
page = next(p for p in text if "Tablo 2:" in p)
table, totals, problems = parse(page.split("Toplam", 1)[1].splitlines(), COLUMNS)

finds = [
    {"id": "lithics-2024", "class": "E22_Human-Made_Object", "label": "2024 yontma taş buluntuları (toplam)", "type": "chipped stone assemblage",
     "count": 677, "material": "stone", "found_by": "exc-2024", "at_feature": "site", "from_stratum": "layer-1",
     "note": "Çoğunluğunun dönemi belirlenememiştir. Aletlerin bir kısmı yanmıştır. Tablo 2 kendi içinde tutarsızdır: " + "; ".join(problems) + ".",
     "figures": ["tablo-2", "resim-3", "resim-4", "resim-5"], "pages": P(198, 199, 200, 201)},
]
for row, cells in table.items():
    for col, n in cells.items():
        periods_, certainty = ATTRIBUTION[col]
        natural = col == "doğal" or row in ("doğal parça", "manuport")
        f = {"id": f"lith-{slug(row)}-{slug(col.replace('?', ' q'))}", "class": "E19_Physical_Object" if natural else "E22_Human-Made_Object",
             "label": f"{row} ({col})", "type": LITHIC_TYPES[row], "count": n, "material": "stone",
             "found_by": "exc-2024", "at_feature": "site", "from_stratum": "layer-1",
             "part_of": "lithics-2024",                                                                            # NEW part_of on finds
             "figures": ["tablo-2"], "pages": P(200)}
        if periods_:
            f["periods"] = periods_
            f["dating_by"] = {"by": AUTHORS, "via": "authors' assessment"}
        if certainty:
            f["dating_certainty"] = certainty
        if col == "belirsiz":
            f["note"] = "Dönemi belirlenememiştir."
        if col == "doğal":
            f["note"] = "Tabloda 'doğal' sütununda sayılmıştır."
        finds.append(f)

LAYER = {"found_by": "exc-2024", "at_feature": "site", "from_stratum": "layer-1"}
finds += [
    {"id": "gravettian-point", "class": "E22_Human-Made_Object", "label": "Gravettien uç", "type": "Gravettian point", "count": 1, "material": "stone",
     "periods": ["upper-palaeolithic"], "dating_by": {"by": AUTHORS, "via": "authors' assessment"},
     "found_by": "exc-2024", "at_feature": "site", "from_stratum": "unit-x",
     "note": "Resim 6 alt yazısına göre X biriminden. Tablo 2'de ayrı bir satırı yoktur; hangi satırda sayıldığı belirtilmemiştir.",
     "figures": ["resim-6"], "pages": P(199, 206)},
    {"id": "retouched-blade-x", "class": "E22_Human-Made_Object", "label": "X biriminden düzeltili dilgi", "type": "retouched blade", "material": "stone",
     "found_by": "exc-2024", "at_feature": "site", "from_stratum": "unit-x", "figures": ["resim-6"], "pages": P(206)},
    {"id": "microlith-f1-3", "class": "E22_Human-Made_Object", "label": "F1-3 biriminden geometrik mikrolit (üçgen, düzeltili)", "type": "geometric microlith",
     "count": 1, "material": "stone", "periods": ["epipalaeolithic", "upper-palaeolithic"], "dating_certainty": "one of",
     "dating_by": {"by": AUTHORS, "via": "authors' assessment"}, "found_by": "exc-2024", "at_feature": "area-b", "from_stratum": "f1-3",
     "part_of": "lith-mikrolit-epipaleolitik-q", "note": "Üst Paleolitik'ten daha önceki dönemlere de ait olabilir.", "figures": ["resim-7"], "pages": P(199, 207)},
    {"id": "microlith-f1-4", "class": "E22_Human-Made_Object", "label": "F1-4 biriminden geometrik mikrolit (üçgen, düzeltili)", "type": "geometric microlith",
     "count": 1, "material": "stone", "periods": ["epipalaeolithic", "upper-palaeolithic"], "dating_certainty": "one of",
     "dating_by": {"by": AUTHORS, "via": "authors' assessment"}, "found_by": "exc-2024", "at_feature": "area-a", "from_stratum": "f1-4",
     "part_of": "lith-mikrolit-epipaleolitik-q", "note": "Üst Paleolitik'ten daha önceki dönemlere de ait olabilir.", "figures": ["resim-7"], "pages": P(199, 207)},
    {"id": "levallois-point-f1-9", "class": "E22_Human-Made_Object", "label": "F1-9 biriminden Levallois uç", "type": "Levallois point", "material": "stone",
     "periods": ["middle-palaeolithic"], "dating_by": {"by": AUTHORS, "via": "authors' assessment"},
     "found_by": "exc-2024", "at_feature": "area-c", "from_stratum": "f1-9", "part_of": "lith-levallois-uc-op", "figures": ["resim-5"], "pages": P(199, 206)},
    {"id": "micro-levallois-core-f1-7", "class": "E22_Human-Made_Object", "label": "F1-7 biriminden mikro Levallois çekirdek", "type": "micro Levallois core",
     "material": "stone", "found_by": "exc-2024", "at_feature": "area-a", "from_stratum": "f1-7", "figures": ["resim-4"], "pages": P(205)},
    {"id": "hammerstones", "class": "E22_Human-Made_Object", "label": "Vurgaçlar", "type": "hammerstone", "count": 2,
     "material": "volcanic river pebble", "part_of": "lith-vurgac-belirsiz", **LAYER, "figures": ["resim-3"], "pages": P(201, 205)},
    {"id": "pottery-neolithic", "class": "E22_Human-Made_Object", "label": "Neolitik Dönem seramiği", "type": "pottery sherds", "periods": ["neolithic"],
     **LAYER, "note": "Çok az sayıda; sayı verilmemiştir. Resim 5'e göre F1-9 biriminde de seramik vardır.", "figures": ["resim-5"], "pages": P(198, 199, 206)},
    {"id": "plastics", "class": "E22_Human-Made_Object", "label": "Ambalaj parçaları, sigara ağızlıkları gibi plastik malzeme", "type": "modern debris",
     "material": "plastic", "periods": ["republic"], **LAYER, "note": "Az sayıda.", "pages": P(202)},
    {"id": "dung", "class": "E20_Biological_Object", "label": "Küçükbaş hayvan dışkı kalıntıları", "type": "animal dung", "periods": ["recent"],
     **LAYER, "pages": P(198, 202)},
    {"id": "fauna-2024", "class": "E20_Biological_Object", "label": "2024 hayvan kemik kalıntıları (toplam)", "type": "animal bone",
     "dimensions": [{"type": "volume", "value": 40, "unit": "l", "approx": True}], **LAYER,
     "note": "Kırık parçalar olduğu için sayılmamıştır. Kötü korunmuş ve küçük parçalara ayrılmış. Uzun kemikler kafatası parçalarından fazla; "
             "boynuz parçası yok denecek kadar az; diş sayısı fazla; küçük memeli kalıntısı çok.", "pages": P(198, 201)},
    {"id": "fauna-ice-age", "class": "E20_Biological_Object", "label": "Buzul dönemi faunası", "type": "animal bone", "part_of": "fauna-2024",
     "taxa": ["Panthera spelaea", "Ursus spelaeus", "Crocuta crocuta spelaea"],
     "periods": ["palaeolithic"], "dating_by": {"by": AUTHORS, "via": "extinction range of the species"}, **LAYER,
     "note": "Metne göre Panthera spelaea 450.000-14.000 yıl önce Avrasya'da yayılım göstermiş, Ursus spelaeus yaklaşık 24.000 yıl önce tükenmiş, "
             "Crocuta crocuta spelaea'nın Avrupa'daki en geç örnekleri yaklaşık 31.000 yıl önce yok olmuştur. Ön inceleme.", "pages": P(201, 202)},
    {"id": "cave-bear", "class": "E20_Biological_Object", "label": "Mağara ayısı kalıntıları (dişler, çene parçaları, parmak ve bilek kemikleri)",
     "type": "animal bone", "taxa": ["Ursus spelaeus"], "part_of": "fauna-ice-age", **LAYER,
     "note": "In situ tabakalardan değil, karışık dolgulardan.", "figures": ["resim-8"], "pages": P(202, 207)},
    {"id": "hyena-mandible", "class": "E20_Biological_Object", "label": "Benekli mağara sırtlanı alt çenesi", "type": "mandible",
     "taxa": ["Crocuta crocuta spelaea"], "part_of": "fauna-ice-age", **LAYER, "figures": ["resim-9"], "pages": P(201, 208)},
    {"id": "fauna-neolithic", "class": "E20_Biological_Object", "label": "Neolitik Dönem'e tarihlenebilecek hayvan kalıntıları", "type": "animal bone",
     "taxa": ["Canis lupus", "Vulpes vulpes", "Cervus elaphus", "Dama dama", "Equus caballus", "Bos taurus", "Ovis aries"],
     "periods": ["neolithic"], "dating_certainty": "uncertain", "dating_by": {"by": AUTHORS, "via": "authors' assessment"},
     "part_of": "fauna-2024", **LAYER, "note": "Bu türlerle 2023 çalışmalarında da karşılaşılmıştır.", "pages": P(201, 202)},
    {"id": "fauna-extant-other", "class": "E20_Biological_Object", "label": "Günümüzde de yaşayan diğer türler", "type": "animal bone",
     "taxa": ["Castor fiber", "Felis rufus"], "part_of": "fauna-2024", **LAYER, "note": "Tür adları basıldığı gibi.", "pages": P(201)},
    {"id": "beaver-jaw", "class": "E20_Biological_Object", "label": "Kunduz çenesi", "type": "mandible", "taxa": ["Castor fiber"],
     "part_of": "fauna-extant-other", **LAYER, "note": "Resim 10 alt yazısında 'Castor' olarak geçer.", "figures": ["resim-10"], "pages": P(201, 208)},
    {"id": "fauna-higher-taxa", "class": "E20_Biological_Object", "label": "Tür tayini yapılamayan hayvan kalıntıları", "type": "animal bone",
     "taxa": ["Testudae", "Aves", "Pisces", "Lepus", "Suidae", "Lynx", "Spalax", "Mesocricetus", "Gerbillus", "Vespertlio", "Dinaromys",
              "Martes", "Paradipus", "Mustela", "Microtus"],
     "part_of": "fauna-2024", **LAYER, "note": "Yüksek oranda parçalanmış. Adlar basıldığı gibi.", "pages": P(201)},
]

interpretations = [
    {"id": "int-occupation-span", "about": "site", "assigned": "Orta Paleolitik'ten Üst Paleolitik ve Neolitik'e kadar insan etkinliği",
     "basis": "2023'te elenen defineci dolgularından gelen arkeolojik ve arkeozoolojik malzeme.", "by": AUTHORS, "pages": P(197)},
    {"id": "int-layer1-holocene", "about": "layer-1", "assigned": "Holosen'de depolanmış, içinde Pleyistosen buluntuları olan tabaka",
     "basis": "Genel değerlendirme ('söylenebilir').", "by": AUTHORS, "pages": P(198)},
    {"id": "int-layer1-mixed", "about": "layer-1", "assigned": "karışık dolgu",
     "basis": "Orta ve Üst Paleolitik malzeme, soyu tükenmiş hayvan kalıntıları, Cumhuriyet Dönemi plastikleri, yakın dönem dışkı ve ocak yerleri birlikte bulunmuştur.",
     "by": AUTHORS, "pages": P(198, 199, 202)},
    {"id": "int-short-stay", "about": "site", "assigned": "yıl içinde kısa süreli iskân amaçlı kullanım",
     "basis": "Elenen toprak miktarına oranla buluntu sayısının görece düşük olması.", "by": AUTHORS, "pages": P(201)},
    {"id": "int-teeth", "about": "fauna-2024", "assigned": "diş fazlalığı korunum farkından kaynaklanmış olabilir",
     "basis": "Dişlerin kemik dokusuna kıyasla daha yüksek korunum potansiyeli.", "by": AUTHORS, "pages": P(201)},
    {"id": "int-cave-fauna", "about": "fauna-ice-age", "assigned": "Orta Paleolitik'te mağara büyük mağara faunası tarafından da kullanılmıştır",
     "basis": "Hayvan kalıntılarına ait veriler.", "by": AUTHORS, "pages": P(201)},
    {"id": "int-bear-furs", "about": "cave-bear", "assigned": "kemikler ayı kürkleri içinde mağaraya taşınmış olabilir",
     "basis": "Yalnızca diş, çene, parmak ve bilek kemikleri var; ayılar burada barınmış olsa başka kemikler de bulunurdu. "
              "Yazarlar teyit için daha fazla veri gerektiğini vurgular.", "by": AUTHORS, "pages": P(202)},
    {"id": "int-neolithic-food", "about": "fauna-neolithic", "assigned": "dönemin insan toplulukları bu hayvanlardan gıda temini amacıyla yararlanmıştır",
     "by": AUTHORS, "pages": P(202)},
    {"id": "int-burning", "about": "lithics-2024", "assigned": "yanmanın zamanı belirsiz",
     "basis": "Dolgular karışmış olduğu için Orta Paleolitik bir yonga Cumhuriyet Dönemi'nde yakılmış bir ateşten etkilenmiş olabilir.",
     "by": AUTHORS, "pages": P(201)},
    {"id": "int-potential", "about": "site", "assigned": "Orta ve Üst Paleolitik'e ait kronolojik ve kültürel boşluğu doldurma potansiyeli",
     "basis": "İlk kazının sonuçları; buluntuların iyi korunmuş olması.", "by": AUTHORS, "pages": P(197)},
]

CAPTIONS = [
    ("Resim", 1, "Sinekkaya Mağarası 2024 çalışmalarından bir 3B model örneği.", ["site"], 204),
    ("Resim", 2, "Sinekkaya Mağarası kazı çalışmalarında C (solda) ve B (sağda) alanları.", ["area-c", "area-b"], 204),
    ("Resim", 3, "F1-5 birimindeki ocak (üst solda), tespit edilmiş yontma taş buluntular (alt ortada), volkanik çay taşından vurgaç (sağda).", ["hearth-f1-5", "f1-5", "hammerstones"], 205),
    ("Resim", 4, "F1-7 birimindeki kanal (sağ altta), mikro Levallois çekirdek (sol üstte) ve yontma taşlar (sağ üstte).", ["f1-7", "micro-levallois-core-f1-7"], 205),
    ("Resim", 5, "F1-9 birimindeki sertleşmiş dolgu (alt ortada), Levallois uç (alt sağ), yontma taşlar (üst sol) ve seramikler (üst sağda).", ["f1-9", "levallois-point-f1-9", "pottery-neolithic"], 206),
    ("Resim", 6, "X biriminden düzeltili dilgi (solda), Gravettien uç (sağda).", ["retouched-blade-x", "gravettian-point"], 206),
    ("Resim", 7, "F1-3 (sağda) ve F1-4 birimlerinden iki düzeltili mikrolit (üçgen).", ["microlith-f1-3", "microlith-f1-4"], 207),
    ("Resim", 8, "Mağara ayısına (Ursus spelaeus) ait kalıntılar.", ["cave-bear"], 207),
    ("Resim", 9, "Benekli mağara sırtlanına (Crocuta crocuta spelaea) ait alt çene.", ["hyena-mandible"], 208),
    ("Resim", 10, "Kunduz (Castor) türüne ait çene.", ["beaver-jaw"], 208),
    ("Tablo", 1, "Sinekkaya Mağarası'nda 2024 yılı stratigrafik birimleri özeti.", ["layer-1"] + [u[0] for u in UNITS], 199),
    ("Tablo", 2, "Sinekkaya Mağarası 2024 yontma taş buluntuları.", ["lithics-2024"], 200),
]
figures = [{"id": f"{slug(k)}-{n}", "kind": k, "number": n, "caption": c, "depicts": d, "page": p} for k, n, c, d, p in CAPTIONS]

record = {
    "$comment": "Structured record extracted from: Dinçer, Şahin, Tuğutlu, İçel (2026) 'Sinekkaya Mağarası (Orhaneli, Bursa) Kazısı 2024', "
                "45. Kazı Sonuçları Toplantısı Cilt 1, pp. 197-208. 'pages' are printed page numbers. Made by tools/make_sinekkaya_record.py. "
                "E-mail addresses printed in the paper are left out on purpose.",
    "schema_version": 3,
    "base_uri": "https://example.org/kst45/sinekkaya-2024/",
    "shared_uri": "https://example.org/kst45/",
    "document": {"id": "report", "title": "Sinekkaya Mağarası (Orhaneli, Bursa) Kazısı 2024", "language": "tr", "authors": AUTHORS,
                 "pages": "197-208", "published": "2026", "documents": "campaign-2024",
                 "volume": {"id": "kst45-1", "title": "45. Kazı Sonuçları Toplantısı Bildirileri, Cilt 1", "editor": "atesogullari",
                            "publisher": "kvmgm", "isbn": "978-975-17-6634-2", "place": "Ankara", "published": "2026"},
                 "source_file": "kst_paper_split/13_SINEKKAYA_MAGARASI_ORHANELI_BURSA_KAZISI_2024.pdf"},
    "actors": actors, "places": places, "periods": periods, "features": features, "strata": strata, "relations": relations,
    "references": references, "activities": activities, "records": records, "finds": finds,
    "interpretations": interpretations, "figures": figures,
}
out = ROOT / "data/sinekkaya_2024.json"
out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, {k: len(v) for k, v in record.items() if isinstance(v, list)})
print("Tablo 2:", problems)
