# -*- coding: utf-8 -*-
import json, re, collections, sys

BASE = "/media/tugce/ProgramsVS/tez/v2/blind/test3/"
OUT = BASE + "readerA/statements.json"
GROUPS = "DOC STRUCT PEOPLE ADMIN WORK PLACE BUILT FIND MEASURE DATE INTERP LAB FIGURE DESCR HISTORY".split()

rows = []
P = [115]


def pg(n):
    P[0] = n


def S(group, subject, says, value, quote, hedge="", neg=False, who="", form="prose"):
    rows.append(dict(n=len(rows) + 1, page=P[0], group=group, form=form, subject=subject,
                     says=says, value=value, hedge=hedge, negative=neg, who=who, quote=quote))


def L(group, subject, says, value, quote, hedge="", neg=False, who=""):
    S(group, subject, says, value, quote, hedge, neg, who, form="list")


KAZI = "İznik Hisardere Nekropolü 2024 yılı kazı çalışmaları"

# ---------------------------------------------------------------- page 115
pg(115)
S("STRUCT", "sayfa üst başlığı", "page header reads", "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1",
  "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1")
S("DOC", "bildiri", "has title", "İZNİK HİSARDERE NEKROPOLÜ 2024 YILI KAZI ÇALIŞMALARI",
  "İZNİK HİSARDERE NEKROPOLÜ 2024 YILI KAZI ÇALIŞMALARI")
for a in ["Aygün EKİN MERİÇ", "Ali Kazım ÖZ", "Tolga KOPARAL", "Gülşen KUTBAY", "Ruken Zeynep KÖSE"]:
    L("DOC", "bildiri", "has author", a, a)
S("ADMIN", KAZI, "was permitted by", "Kültür ve Turizm Bakanlığı", "Kültür ve Turizm Bakanlığının izni ve maddi desteği ile")
S("ADMIN", KAZI, "was financially supported by", "Kültür ve Turizm Bakanlığı", "Kültür ve Turizm Bakanlığının izni ve maddi desteği ile")
S("ADMIN", KAZI, "was carried out under the presidency of", "İznik Müzesi Müdürlüğü", "İznik Müzesi Müdürlüğü başkanlığında")
S("PEOPLE", "Aygün Ekin Meriç", "role in the work", "Bilimsel Koordinatör", "Prof. Dr. Aygün Ekin Meriç’in Bilimsel Koordinatörlüğünde")
S("PEOPLE", "Aygün Ekin Meriç", "title", "Prof. Dr.", "Prof. Dr. Aygün Ekin Meriç’in")
S("PEOPLE", "Aygün Ekin Meriç", "affiliation", "Dokuz Eylül Üniversitesi", "Dokuz Eylül Üniversitesinden Prof. Dr. Aygün Ekin Meriç’in")
S("WORK", KAZI, "was carried out by", "Bilimsel Koordinatörlüğünde oluşturulan bir ekip", "oluşturulan bir ekip tarafından gerçekleştirilmiştir")
S("WORK", KAZI, "took place between", "01.08.2024-27.12.2024", "01.08.2024-27.12.2024 tarihleri arasında")
S("WORK", KAZI, "manner of continuation", "aralıklı olarak", "aralıklı olarak 01.08.2024-27.12.2024")
q = "bir arkeolog, bir antropolog, dört işçi ve sekiz gönüllü öğrenci tarafından sürdürülmüştür"
L("PEOPLE", "arkeolog", "count in the team", "bir", q)
L("PEOPLE", "antropolog", "count in the team", "bir", q)
L("ADMIN", "işçi", "count in the team", "dört", q)
L("PEOPLE", "gönüllü öğrenci", "count in the team", "sekiz", q)
S("WORK", "çalışmalar", "number of work areas", "beş alan", "olmak üzere beş alanda gerçekleşmiştir")
for v, qq in [("Kazı Çalışmaları", "Çalışmalar; Kazı Çalışmaları"),
              ("Seramik ve Küçük Buluntu Değerlendirme", "Seramik ve Küçük Buluntu Değerlendirme"),
              ("Antropoloji Çalışmaları", "Antropoloji Çalışmaları"),
              ("Mimari Belgeleme ve Çizim", "Mimari Belgeleme ve Çizim"),
              ("Restorasyon ve Konservasyon", "Restorasyon ve Konservasyon olmak üzere")]:
    L("WORK", "çalışmalar", "had work area", v, qq)
S("STRUCT", "başlık", "heading reads", "KAZI ÇALIŞMALARI", "KAZI ÇALIŞMALARI")
S("WORK", "alan", "was scanned with", "yeraltı görüntüleme sistemi", "yeraltı görüntüleme sistemi yardımıyla taranan alanın")
S("WORK", "yeraltı görüntüleme sistemi taraması", "took place in", "2020 yılı temmuz ayı", "2020 yılı temmuz ayında gerçekleştirilen yeraltı görüntüleme sistemi")
S("WORK", "çalışma planı", "was based on", "jeoradar verileri", "jeoradar verileri esas alınarak çalışma planı belirlenmiştir")
S("WORK", "öncelikli kazılacak alanlar", "were determined from", "jeoradar tarama verileri", "Jeoradar tarama verileriyle birlikte")
S("WORK", "öncelikli kazılacak alanlar", "were determined from", "önceki yıllarda gerçekleştirilen kazı çalışmaları",
  "önceki yıllarda gerçekleştirilen kazı çalışmaları bir arada değerlendirilerek, öncelikli kazılacak alanlar belirlenmiştir")
q = "E-15 ve E-16 plankarelerinde gerçekleştirilmiştir"
S("WORK", "01.08.2024-30.08.2024 çalışmaları", "took place between", "01.08.2024-30.08.2024", "01.08.2024-30.08.2024 tarihleri arasında")
S("ADMIN", "01.08.2024-30.08.2024 çalışmaları", "was funded by", "Kültür ve Turizm Bakanlığından sağlanan ödenek",
  "Kültür ve Turizm Bakanlığından sağlanan ödenek ile gerçekleştirilen çalışmalar")
S("WORK", "01.08.2024-30.08.2024 çalışmaları", "took place in square", "E-15", q)
S("WORK", "01.08.2024-30.08.2024 çalışmaları", "took place in square", "E-16", q)
S("WORK", "03.10.2024-29.11.2024 çalışmaları", "took place between", "03.10.2024-29.11.2024", "03.10.2024-29.11.2024 tarihleri arasında")
S("ADMIN", "03.10.2024-29.11.2024 çalışmaları", "was part of project", "Geleceğe Miras Projesi", "Geleceğe Miras Projesi kapsamında")
S("ADMIN", "03.10.2024-29.11.2024 çalışmaları", "was funded by", "Kültür ve Turizm Bakanlığından sağlanan ödenek yardımı",
  "Kültür ve Turizm Bakanlığından sağlanan ödenek yardımı ile")
q = "J-17, J-18, J-K/18, K-16, K-17, K-18, K-L/15-16, L-17 ve L-18 plankarelerinde"
for v in ["J-17", "J-18", "J-K/18", "K-16", "K-17", "K-18", "K-L/15-16", "L-17", "L-18"]:
    L("WORK", "03.10.2024-29.11.2024 çalışmaları", "took place in square", v, q)
S("FIGURE", "plankareler / kazı alanı", "is shown in figure", "Çizim: 1", "gerçekleştirilmiştir (Çizim: 1)")
# footnote
fn = [
    ("Aygün Ekin Meriç", None, "Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü",
     "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE", "0000-0002-1343-847X",
     "Prof. Dr. Aygün EKİN MERIÇ; Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü",
     "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE, E-posta: aygun", "ORCID: 0000-0002-1343-847X"),
    ("Ali Kazım Öz", "Prof. Dr.", "Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü",
     "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE", "0000-0002-3005-323X",
     "Prof. Dr. Ali Kazım ÖZ; Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü",
     "Arkeoloji Bölümü, Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE, E-posta: ali", "ORCID: 0000-0002-3005-323X"),
    ("Tolga Koparal", "Arkeolog", "İznik Müzesi Müdürlüğü", "16860 İznik, Bursa, TÜRKIYE", None,
     "Arkeolog Tolga KOPARAL; İznik Müzesi Müdürlüğü", "İznik Müzesi Müdürlüğü, 16860 İznik, Bursa, TÜRKIYE", None),
    ("Gülşen Kutbay", "Arkeolog Dr.", "Hisardere Nekropolü Kazıevi", "16860 İznik, Bursa, TÜRKIYE", None,
     "Arkeolog Dr. Gülşen KUTBAY; Hisardere Nekropolü Kazıevi", "KUTBAY; Hisardere Nekropolü Kazıevi, 16860 İznik, Bursa, TÜRKIYE", None),
    ("Ruken Zeynep Köse", "Antropolog", "Hisardere Nekropolü Kazıevi", "16860 İznik, Bursa, TÜRKIYE", None,
     "Antropolog Ruken Zeynep KÖSE; Hisardere Nekropolü Kazıevi", "KÖSE; Hisardere Nekropolü Kazıevi, 16860 İznik, Bursa, TÜRKIYE", None),
]
for name, title, aff, addr, orcid, q1, q2, q3 in fn:
    if title:
        L("PEOPLE", name, "title", title, q1)
    L("PEOPLE", name, "affiliation", aff, q1)
    L("PEOPLE", name, "address of affiliation", addr, q2)
    if orcid:
        L("PEOPLE", name, "identifier (ORCID)", orcid, q3)

# ---------------------------------------------------------------- page 116
pg(116)
S("STRUCT", "sayfa üst başlığı", "page header reads", "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ", "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ")
S("STRUCT", "başlık", "heading reads", "E-15 Plankaresi", "E-15 Plankaresi")
S("BUILT", "bazilika", "was built over", "Nekropol alanı", "Nekropol alanı üzerine inşa edilmiş bazilikanın")
S("WORK", "E-15 plankaresi kazı çalışmaları", "was planned because of", "jeoradar taramaları sonucu", "Alanda gerçekleştirilen jeoradar taramaları sonucunda")
S("WORK", "E-15 plankaresi kazı çalışmaları", "had the aim", "bazilikanın batı sınırını ortaya çıkarmak",
  "bazilikanın batı sınırını ortaya çıkarmak amacıyla E-15 plankaresinde")
S("WORK", "E-15 açması", "trench limits measure", "600x600 cm", "600x600 cm ölçülerinde açma sınırları belirlenmiş")
S("PLACE", "E-15 açması", "work started at elevation", "+96,82 m", "çalışmalar +96,82 m kotunda başlatılmıştır")
q = "sert, kuru ve sıkışmış bir yapıya sahip toprak tabakasında"
S("BUILT", "toprak tabakası (E-15)", "lies in", "alanın kuzey kesiti", "Alanın kuzey kesitinde")
L("BUILT", "toprak tabakası (E-15)", "has character", "sert", q)
L("BUILT", "toprak tabakası (E-15)", "has character", "kuru", q)
L("BUILT", "toprak tabakası (E-15)", "has character", "sıkışmış", q)
q = "tessera ve mozaik parçalarının öbekler halinde bulunduğu tespit edilmiştir"
S("FIND", "tessera (E-15)", "kind", "tessera", q)
S("FIND", "tessera (E-15)", "was found in", "kuzey kesitteki toprak tabakası", "toprak tabakasında, tessera ve mozaik parçalarının")
S("FIND", "tessera (E-15)", "position in place", "öbekler halinde", q)
S("FIND", "mozaik parçaları (E-15)", "kind", "mozaik parçaları", q)
S("FIND", "mozaik parçaları (E-15)", "was found in", "kuzey kesitteki toprak tabakası", "toprak tabakasında, tessera ve mozaik parçalarının")
S("FIND", "mozaik parçaları (E-15)", "position in place", "öbekler halinde", q)
S("WORK", "tesseralar (E-15)", "was examined for", "alanla organik bir bağının olup olmadığı",
  "ele geçirilen tesseraların alanla organik bir bağının olup olmadığı titizlikle incelenmiştir")
q = "96,44 m kotunda tahrip olmuş bir statumen tabakası ve mozaik harcı gözlemlenmiştir"
S("BUILT", "statumen tabakası (E-15)", "kind", "statumen tabakası", q)
S("PLACE", "statumen tabakası (E-15)", "elevation", "96,44 m", q)
S("BUILT", "statumen tabakası (E-15)", "condition", "tahrip olmuş", q)
S("BUILT", "mozaik harcı (E-15)", "kind", "mozaik harcı", q)
S("PLACE", "mozaik harcı (E-15)", "elevation", "96,44 m", q)
S("INTERP", "alan (E-15)", "is interpreted as covered with", "mozaik taban döşemesi",
  "alanın mozaik taban döşemesiyle kaplı olduğuna işaret ettiğinden", hedge="işaret ettiğinden")
S("WORK", "statumen tabakası ve mozaik harcı kalıntıları (E-15)", "decision", "korunmasına karar verilmiştir",
  "kalıntıların korunmasına karar verilmiştir")
S("DESCR", "statumen tabakası ve mozaik harcı kalıntıları (E-15)", "is judged", "önemli", "bu önemli kalıntıların")
q = "+96,33 m kotunda, 67x120 cm ölçülerinde iki sıra taş örgülü bir duvar yapısı tespit edilmiştir"
S("WORK", "E-15 kazı çalışmaları", "advanced towards", "kuzey yönü", "Kazı çalışmaları kuzey yönünde ilerletildiği esnada")
S("BUILT", "duvar yapısı (E-15)", "kind", "duvar yapısı", q)
S("PLACE", "duvar yapısı (E-15)", "elevation", "+96,33 m", q)
S("MEASURE", "duvar yapısı (E-15)", "measures", "67x120 cm", q)
S("BUILT", "duvar yapısı (E-15)", "is built as", "iki sıra taş örgülü", q)
S("BUILT", "duvar (E-15)", "orientation", "doğu-batı doğrultulu", "doğu-batı doğrultulu duvarın güneyinde")
q = "dibe yakın bölümü korunmuş bir pithos kalıntısı ortaya çıkarılmıştır"
S("FIND", "pithos kalıntısı (E-15)", "kind", "pithos kalıntısı", q)
S("FIND", "pithos kalıntısı (E-15)", "was found in", "doğu-batı doğrultulu duvarın güneyinde yer alan bir alan",
  "doğu-batı doğrultulu duvarın güneyinde yer alan bir alanda")
S("FIND", "pithos kalıntısı (E-15)", "condition", "dibe yakın bölümü korunmuş", q)
S("FIND", "pithos kalıntısı (E-15)", "contains", "harç kalıntıları", "içinde harç kalıntıları bulunan")
S("DESCR", "pithosun harç kalıntıları (E-15)", "is judged to have potential to inform on", "yapının kullanım amacı ve dönemin gömü pratikleri",
  "yapının kullanım amacı ve dönemin gömü pratiklerine ilişkin bilgiler sağlama potansiyeline sahiptir", hedge="potansiyeline sahiptir")
S("BUILT", "ÇM 1 (E-15)", "kind", "Çatkı Mezar", "bir Çatkı Mezar (ÇM 1) tespit edilmiştir")
S("BUILT", "ÇM 1 (E-15)", "position", "açmanın kuzey kesitinden 40 cm içeride", "açmanın kuzey kesitinden 40 cm içeride")
S("PLACE", "ÇM 1 (E-15)", "elevation", "+96,00 m.", "+96,00 m. kotunda doğu-batı doğrultusunda uzanan")
S("BUILT", "ÇM 1 (E-15)", "orientation", "doğu-batı doğrultusunda", "+96,00 m. kotunda doğu-batı doğrultusunda uzanan")
S("MEASURE", "ÇM 1 (E-15)", "measures (length)", "182 cm", "uzunluğu 182 cm")
S("MEASURE", "ÇM 1 (E-15)", "measures (width)", "50 cm", "genişliği ise 50 cm olan bir Çatkı Mezar")
S("BUILT", "ÇM 1 (E-15)", "extends", "bir kısmı doğu kesitin altına doğru", "mezarın bir kısmının doğu kesitin altına doğru uzandığı")
S("BUILT", "ÇM 1 (E-15) mezar kapakları", "are supported with", "harç ve taşlar", "mezar kapaklarının harç ve taşlarla desteklendiği")
S("WORK", "ÇM 1 (E-15)", "work done", "belgeleme işlemleri tamamlandı", "Mezarın belgeleme işlemlerinin tamamlanmasının ardından")
S("WORK", "ÇM 1 (E-15)", "work done", "batı yönündeki iki kapak açıldı", "batı yönündeki iki kapağın açılmasıyla")
q = "iskelete ait kemik döküntüleri toplanarak kayıt altına alınmıştır"
S("FIND", "kemik döküntüleri (E-15 ÇM 1)", "kind", "iskelete ait kemik döküntüleri", q)
S("FIND", "kemik döküntüleri (E-15 ÇM 1)", "was found in", "ÇM 1 mezar içi", "mezar içinde neredeyse tamamen yok olmuş olan iskelete ait")
S("FIND", "iskelet (E-15 ÇM 1)", "condition", "neredeyse tamamen yok olmuş", "neredeyse tamamen yok olmuş olan iskelete")
S("WORK", "kemik döküntüleri (E-15 ÇM 1)", "work done", "toplanarak kayıt altına alınmıştır", q)
S("WORK", "E-15 kazı çalışmaları", "continued towards", "güney yönü", "Güney yönünde sürdürülen kazı çalışmaları sırasında")
S("BUILT", "TPM 1 (E-15)", "kind", "terrakota plaka kapaklı mezar yapısı", "terrakota plaka kapaklı bir mezar yapısına (TPM 1)")
S("PLACE", "TPM 1 (E-15) kapakları ve tuğla sırası", "elevation", "+95,98 m", "+95,98 m kotunda terrakota plaka kapaklı")
S("BUILT", "TPM 1 (E-15)", "has part", "mezarın duvarına ait tuğla sırası", "mezarın duvarına ait tuğla sırasına ulaşılmıştır")
S("BUILT", "TPM 1 (E-15)", "orientation", "doğu-batı doğrultusunda", "Doğu-batı doğrultusunda uzanan mezarın boyutları")
S("MEASURE", "TPM 1 (E-15)", "measures", "71x213 cm", "mezarın boyutları 71x213 cm olarak ölçülmüştür")
q = "her biri 8 cm kalınlığında ve 71x71 cm boyutlarında üç adet pişmiş toprak plaka ile örtülmüş"
S("BUILT", "TPM 1 (E-15)", "is covered with", "pişmiş toprak plaka", q)
S("BUILT", "TPM 1 (E-15) pişmiş toprak plakalar", "count", "üç adet", q)
S("MEASURE", "TPM 1 (E-15) pişmiş toprak plakalar", "measures (thickness)", "8 cm", q)
S("MEASURE", "TPM 1 (E-15) pişmiş toprak plakalar", "measures", "71x71 cm", q)
S("BUILT", "TPM 1 (E-15)", "is surrounded by", "tuğlalardan oluşan bir sıra", "tuğlalardan oluşan bir sıra ile çevrelenmiştir")
S("MEASURE", "TPM 1 (E-15) tuğlalar", "measures (length)", "32 cm", "32 cm uzunluğundaki tuğlalardan")
S("MEASURE", "TPM 1 (E-15) tuğla sırası", "measures (measurable total length)", "238 cm",
  "Tuğla sırasının ölçülebilen toplam uzunluğu 238 cm olarak kaydedilmiştir")
S("BUILT", "TPM 1 (E-15)", "number of covers fit for opening", "üç kapak", "açılmaya uygun olan üç kapağından")
S("WORK", "TPM 1 (E-15)", "work done", "doğu yönündeki iki kapak kaldırıldı", "doğu yönündeki iki kapak kaldırılarak mezar içi çalışmalara başlanmıştır")
S("MEASURE", "TPM 1 (E-15) mezar içi", "measures (length)", "185 cm", "uzunluğu 185 cm")
S("MEASURE", "TPM 1 (E-15) mezar içi", "measures (width)", "38 cm", "genişliği ise 38 cm olan mezar içerisinde")
q = "mezar içerisinde bir bireye ait iskelet kalıntısı tespit edilmiş"
S("FIND", "iskelet kalıntısı (E-15 TPM 1)", "kind", "iskelet kalıntısı", q)
S("FIND", "iskelet kalıntısı (E-15 TPM 1)", "was found in", "TPM 1 mezar içi", q)
S("FIND", "iskelet kalıntısı (E-15 TPM 1)", "count of individuals", "bir birey", q)
S("WORK", "TPM 1 (E-15)", "work done", "mezarın içi temizlenerek çalışmalar sonlandırılmıştır", "mezarın içi temizlenerek çalışmalar sonlandırılmıştır")
S("BUILT", "TPM 1 (E-15) mezar iç duvarları", "are coated with", "tuğla tozu içeren pembemsi bir sıva",
  "Mezar iç duvarlarının, tuğla tozu içeren pembemsi bir sıva ile kaplı olduğu")
S("BUILT", "TPM 1 (E-15) zemini", "is paved with", "düzensiz biçimde alana uydurulmuş tuğlalar",
  "zeminin ise düzensiz biçimde alana uydurulmuş tuğlalarla döşendiği")
S("FIGURE", "TPM 1 (E-15)", "is shown in figure", "Resim: 1", "döşendiği belirlenmiştir (Resim: 1)")
S("LAB", "iskelet (E-15 TPM 1)", "sex is", "kadın", "iskeletin muhtemelen bir kadına ait olabileceği yönünde ilk bulgular elde edilmiştir",
  hedge="muhtemelen ... olabileceği yönünde ilk bulgular")
S("BUILT", "beş çatkı mezar (E-15)", "position", "Çatkı Mezar 1’in (ÇM 1) güney paralelinde", "Çatkı Mezar 1’in (ÇM 1) güney paralelinde")
S("BUILT", "beş çatkı mezar (E-15)", "was found during work in", "doğu kesit", "Doğu kesitte yürütülen kazı çalışmaları sırasında")

# ---------------------------------------------------------------- page 117
pg(117)
q = "yerleştirilmiş beş adet çatkı mezar daha açığa çıkarılmıştır"
S("BUILT", "beş çatkı mezar (E-15)", "kind", "çatkı mezar", q)
S("BUILT", "beş çatkı mezar (E-15)", "count", "beş adet", q)
S("BUILT", "beş çatkı mezar (E-15)", "orientation", "doğu-batı doğrultusunda", "ğu-batı doğrultusunda yerleştirilmiş beş adet çatkı mezar")
S("WORK", "E-15 mezarları", "were evaluated by", "korunma durumları",
  "mezarların korunma durumlarına göre değerlendirilmesi yapılmıştır")
q = "Korunma durumları oldukça kötü olan ÇM 2, ÇM 3 ve ÇM 5’in kapalı konumda muhafaza edilmesine"
for m in ["ÇM 2", "ÇM 3", "ÇM 5"]:
    L("BUILT", m + " (E-15)", "condition", "korunma durumu oldukça kötü", q)
    L("WORK", m + " (E-15)", "decision", "kapalı konumda muhafaza edilmesi", q)
S("BUILT", "ÇM 4 (E-15)", "condition", "nispeten iyi durumda", "nispeten iyi durumda olan ÇM 4’ün ise açılarak incelenmesine", hedge="nispeten")
S("WORK", "ÇM 4 (E-15)", "decision", "açılarak incelenmesi", "nispeten iyi durumda olan ÇM 4’ün ise açılarak incelenmesine")
S("INTERP", "ÇM 4 (E-15) mezar kapakları", "compared with other simple çatkı graves are", "daha kalın cidarlı ve özenli bir yapıya sahip",
  "diğer basit formlu çatkı mezarlara kıyasla daha kalın cidarlı ve özenli bir yapıya sahip olduğu")
S("BUILT", "ÇM 4 (E-15) kapaklarının iç yüzeyleri", "bear", "basit kazıma motifler", "basit kazıma motiflerin işlendiği tespit edilmiştir")
S("MEASURE", "ÇM 4 (E-15)", "measures (length)", "187 cm", "Uzunluğu 187 cm")
S("MEASURE", "ÇM 4 (E-15)", "measures (width)", "45 cm", "genişliği ise 45 cm olan mezarın")
S("WORK", "ÇM 4 (E-15)", "work done", "temizlik ve belgeleme çalışmaları tamamlanmış", "temizlik ve belgeleme çalışmaları tamamlanmış")
S("FIND", "iskelet (E-15 ÇM 4)", "kind", "iskelet", "iskelet laboratuvar ortamında detaylı analiz için toplanmış")
S("WORK", "iskelet (E-15 ÇM 4)", "work done", "laboratuvar ortamında detaylı analiz için toplanmış", "iskelet laboratuvar ortamında detaylı analiz için toplanmış")
S("WORK", "ÇM 4 (E-15)", "work done", "mezar içi temizlenerek çalışmalar sonlandırılmıştır", "mezar içi temizlenerek çalışmalar sonlandırılmıştır")
S("BUILT", "bazilikanın batı sınırını oluşturan duvar sırası", "was exposed in E-15 (extent)", "bir bölümü",
  "bazilikanın batı sınırını oluşturan duvar sırasının bir bölümü")
S("BUILT", "odaları birbirinden ayıran duvarlar", "was exposed in E-15 (extent)", "bazı kısımları",
  "odaları birbirinden ayıran duvarların bazı kısımları açığa çıkarılmıştır")
q = "beşik çatkı tipi, ikisi pişmiş toprak plaka kapaklı olmak üzere toplam yedi mezar tespit edilmiştir"
S("BUILT", "E-15 mezarları", "count", "toplam yedi mezar", q)
S("BUILT", "E-15 mezarları", "type", "beşik çatkı tipi", q)
S("BUILT", "E-15 mezarları", "count with pişmiş toprak plaka cover", "ikisi", q)
S("FIGURE", "E-15 mezarları", "is shown in figure", "Resim: 2", "edilmiştir (Resim: 2)")
q = "az sayıda seramik parçası"
S("FIND", "seramik parçası (E-15)", "kind", "seramik parçası", q)
S("FIND", "seramik parçası (E-15)", "count", "az sayıda", q)
S("FIND", "seramik parçası (E-15)", "was found in", "E-15 plankaresi", q)
q = "üç adet bronz sikke de bulunmuştur"
S("FIND", "bronz sikke (E-15)", "kind", "sikke", q)
S("FIND", "bronz sikke (E-15)", "count", "üç adet", q)
S("FIND", "bronz sikke (E-15)", "is made of", "bronz", q)
S("FIND", "bronz sikke (E-15)", "was found in", "E-15 plankaresi", q)
S("DESCR", "E-15 buluntuları", "is judged", "alanın mimari düzenini, kullanım amacını ve tarihi bağlamını anlamak açısından önemli veriler sunmaktadır",
  "kullanım amacını ve tarihi bağlamını anlamak açısından önemli veriler sunmaktadır")
S("STRUCT", "başlık", "heading reads", "E-16 Plankaresi", "E-16 Plankaresi")
S("WORK", "E-16 açması", "trench limits measure", "3,50x5,00 m", "E-16 plankaresinde 3,50x5,00 m ölçülerinde belirlenen açma sınırlarında")
S("PLACE", "E-16 açması", "work started at elevation", "+96,82 m", "+96,82 m kotunda kazı çalışmalarına başlanmıştır")
q = "+96,15 m kotunda doğu-batı doğrultulu, basit formlu iki çatkı mezar (ÇM 1 ve ÇM 2) açığa çıkarılmıştır"
for m in ["ÇM 1", "ÇM 2"]:
    S("BUILT", m + " (E-16)", "kind", "basit formlu çatkı mezar", q)
    S("PLACE", m + " (E-16)", "elevation", "+96,15 m", q)
    S("BUILT", m + " (E-16)", "orientation", "doğu-batı doğrultulu", q)
S("BUILT", "ÇM 1 (E-16) mezar kapakları", "bear", "düzensiz kazıma motifler", "mezar kapakları üzerinde düzensiz kazıma motiflerin bulunduğu")
S("BUILT", "ÇM 1 (E-16)", "condition", "korunma durumu kötü", "Mezarın korunma durumunun kötü olması")
S("BUILT", "ÇM 1 (E-16)", "condition", "kapaklardaki çökme sonucu içeriye fazlaca toprak dolmuş",
  "kapaklardaki çökme sonucu içeriye fazlaca toprak dolmuş olması nedeniyle")
S("FIND", "iskelet kalıntısı (E-16 ÇM 1)", "was found in situ", "rastlanamamıştır", "in situ halde iskelet kalıntısına rastlanamamıştır", neg=True)
S("STRUCT", "başlık", "heading reads", "K-17 Plankaresi", "K-17 Plankaresi")
S("ADMIN", "K-17 plankaresi kazı çalışmaları", "was part of project", "Kültür ve Turizm Bakanlığı, Geleceğe Miras Projesi",
  "Kültür ve Turizm Bakanlığı, Geleceğe Miras Projesi kapsamında")
S("PLACE", "K-17 plankaresi", "is located in", "nekropol alanının güneyi", "nekropol alanının güneyinde yer alan K-17 plankaresinde")
q = "Narteks bölümüne ait güney duvarının devamına +97,63 m seviyesinde ulaşılmıştır"
S("BUILT", "bazilikanın Narteks bölümüne ait güney duvarının devamı (K-17)", "kind", "duvar (Narteks güney duvarının devamı)", q)
S("BUILT", "Narteks", "is part of", "bazilika", "bazilikanın Narteks bölümüne ait")
S("PLACE", "Narteks güney duvarının devamı (K-17)", "elevation", "+97,63 m", q)
S("BUILT", "Narteks güney duvarının devamı (K-17)", "orientation", "doğu-batı doğrultulu", "doğrultulu olan bu duvarın genişliği 1,46 m")
S("MEASURE", "Narteks güney duvarının devamı (K-17)", "measures (width)", "1,46 m", "doğrultulu olan bu duvarın genişliği 1,46 m")
S("MEASURE", "buna dik duvarlar (K-17)", "measures (dimension not named)", "[unclear] 72 cm", "buna dik duvarlar ise 72 cm olarak ölçülmüştür")
S("BUILT", "dik duvarlar (K-17)", "position", "doğu-batı doğrultulu duvara dik", "buna dik duvarlar ise 72 cm olarak ölçülmüştür")
S("BUILT", "Sanduka (K-17)", "kind", "Sanduka tipinde bir mezar", "Sanduka tipinde bir mezara +97,22 m seviyesinde rastlanmıştır")
S("PLACE", "Sanduka (K-17)", "elevation", "+97,22 m", "Sanduka tipinde bir mezara +97,22 m seviyesinde rastlanmıştır")
S("BUILT", "Sanduka (K-17)", "position", "doğu-batı doğrultulu duvara paralel", "doğu-batı doğrultulu duvara paralel biçimde yerleştirilmiş")
S("BUILT", "Sanduka (K-17)", "condition", "modern atıklarla tamamen dolmuş", "Modern atıklarla tamamen dolmuş olan mezar")
S("HISTORY", "Sanduka (K-17)", "was looted by", "kaçak kazıcılar", "kaçak kazıcılar tarafından talan edilmiştir")
q = "iskelet kalıntısına ya da buluntu niteliği taşıyan bir materyale rastlanmamıştır"
S("FIND", "iskelet kalıntısı (K-17 Sanduka)", "was found in grave", "rastlanmamıştır", q, neg=True)
S("FIND", "buluntu niteliği taşıyan materyal (K-17 Sanduka)", "was found in grave", "rastlanmamıştır", q, neg=True)
L("MEASURE", "Sanduka (K-17)", "measures (length)", "220 cm", "Uzunluğu 220 cm")
L("MEASURE", "Sanduka (K-17)", "measures (width)", "88 cm", "genişliği 88 cm")
L("MEASURE", "Sanduka (K-17)", "measures (depth)", "40 cm", "derinliği 40 cm olan Sanduka")
q = "oldukça düzgün yontulmuş dört adet monolit taştan oluşmaktadır"
S("BUILT", "Sanduka (K-17)", "is made of", "monolit taş", q)
S("BUILT", "Sanduka (K-17) monolit taşlar", "count", "dört adet", q)
S("BUILT", "Sanduka (K-17) monolit taşlar", "workmanship", "oldukça düzgün yontulmuş", q)

# ---------------------------------------------------------------- page 118
pg(118)
S("STRUCT", "başlık", "heading reads", "K-16 Plankaresi", "K-16 Plankaresi")
S("BUILT", "Hipoje 1 (K-16)", "kind", "yeraltı mezar odası", "bir yeraltı mezar odası olan Hipoje 1’in")
S("PLACE", "Hipoje 1 (K-16) tonozlu üst yapısı ve plaka kapağı", "elevation", "+97,10 m", "K-16 plankaresinde +97,10 m kotunda")
S("BUILT", "Hipoje 1 (K-16)", "orientation", "doğu-batı doğrultusunda", "doğu-batı doğrultusunda yönelmiş bir yeraltı")
S("BUILT", "Hipoje 1 (K-16)", "has part", "tonozlu üst yapı", "Hipoje 1’in tonozlu üst yapısı")
S("BUILT", "Hipoje 1 (K-16)", "entrance is given by", "terrakotta içbükey bir plaka kapak",
  "bu yapıya giriş sağlayan terrakotta içbükey bir plaka kapak tespit edilmiştir")
S("BUILT", "ÇM 1 (K-16)", "kind", "çatkı mezar", "olan bir çatkı mezara (ÇM 1) ulaşılmıştır")
S("PLACE", "ÇM 1 (K-16)", "elevation", "+96,92 m", "+96,92 m kotunda, uzunluğu 174 cm")
S("MEASURE", "ÇM 1 (K-16)", "measures (length)", "174 cm", "+96,92 m kotunda, uzunluğu 174 cm")
S("MEASURE", "ÇM 1 (K-16)", "measures (width)", "52 cm", "genişliği 52 cm olan bir çatkı mezara")
S("FIGURE", "ÇM 1 (K-16)", "is shown in figure", "Resim: 3", "ulaşılmıştır (Resim: 3)")
S("BUILT", "ÇM 1 (K-16) pişmiş toprak plakalar", "consist of", "dört parça", "dört parçadan oluşan pişmiş toprak plakaların")
q = "bir bireye ait iskelet kalıntılarına rastlanmıştır"
S("FIND", "iskelet kalıntıları (K-16 ÇM 1)", "kind", "iskelet kalıntıları", q)
S("FIND", "iskelet kalıntıları (K-16 ÇM 1)", "count of individuals", "bir birey", q)
S("FIND", "iskelet kalıntıları (K-16 ÇM 1)", "was found in", "ÇM 1", "pişmiş toprak plakaların üzerinde yer alan bir bireye")
S("FIND", "iskelet kalıntıları (K-16 ÇM 1)", "position in place", "pişmiş toprak plakaların üzerinde", "pişmiş toprak plakaların üzerinde yer alan bir bireye")
S("WORK", "iskelet (K-16 ÇM 1)", "work done", "laboratuvar ortamında incelenmek üzere toplanmıştır",
  "ortamında incelenmek üzere toplanmıştır")
S("BUILT", "Hipoje 1 (K-16) özgün giriş kapısı", "is located in", "doğu lunette bölümü", "mezarın özgün giriş kapısının doğu lunette bölümünde yer aldığı")
S("BUILT", "Hipoje 1 (K-16) özgün giriş kapısı", "was closed with", "tuğla duvar örgüsü", "kendi döneminde tuğla duvar örgüsüyle kapatıldığı")
S("DATE", "Hipoje 1 (K-16) giriş kapısının kapatılması", "took place in", "kendi döneminde", "kendi döneminde tuğla duvar örgüsüyle kapatıldığı")
S("HISTORY", "Hipoje 1 (K-16) giriş kapısının üst kısmı", "was torn down by", "kaçak kazıcılar", "kaçak kazıcılar tarafından yıkıldığı belirlenmiştir")
L("MEASURE", "Hipoje 1 (K-16)", "measures (inner length)", "192 cm", "İç uzunluğu 192 cm")
L("MEASURE", "Hipoje 1 (K-16)", "measures (width)", "81 cm", "İç uzunluğu 192 cm, genişliği 81 cm")
L("MEASURE", "Hipoje 1 (K-16)", "measures (height)", "156 cm", "ve yüksekliği 156 cm olan mezarın")
q = "mezarın tüm bölümlerinin beyaz renkte, incelikle uygulanmış, bezemesiz bir sıva ile kaplandığı"
S("BUILT", "Hipoje 1 (K-16)", "is coated with", "sıva (tüm bölümleri)", q)
S("BUILT", "Hipoje 1 (K-16) sıvası", "colour", "beyaz", q)
S("BUILT", "Hipoje 1 (K-16) sıvası", "workmanship", "incelikle uygulanmış", q)
S("BUILT", "Hipoje 1 (K-16) sıvası", "has decoration", "bezemesiz", q, neg=True)
S("BUILT", "Hipoje 1 (K-16)", "has part", "havalandırma bacası (tavan kısmında)", "çapında bir havalandırma bacasının bulunduğu tespit edilmiştir")
S("MEASURE", "Hipoje 1 (K-16) havalandırma bacası", "measures (diameter)", "7 cm", "mezarın tavan kısmında 7 cm")
S("BUILT", "Hipoje 1 (K-16) alanı", "is separated by", "sonradan tuğlayla örülmüş bir kapı", "Sonradan tuğlayla örülmüş bir kapı ile ayrılan alanda")
S("MEASURE", "bazilika duvarı ile mezar (Hipoje 1, K-16) arasındaki boşluk", "measures", "42 cm", "bazilika duvarı ile mezar arasında 42")
q = "bu boşlukta iskelet kalıntılarının bulunduğu"
S("FIND", "iskelet kalıntıları (K-16 Hipoje 1 boşluğu)", "kind", "iskelet kalıntıları", q)
S("FIND", "iskelet kalıntıları (K-16 Hipoje 1 boşluğu)", "was found in", "bazilika duvarı ile mezar arasındaki boşluk", q)
S("FIGURE", "Hipoje 1 (K-16)", "is shown in figure", "Resim: 4", "tir (Resim: 4)")
S("WORK", "Hipoje 2 (K-16)", "was found", "önceden", "K-16 plankaresinden önceden bulunan Hipoje 2’ye")
S("WORK", "Hipoje 2 (K-16)", "was entered by", "pişmiş toprak kapağın çıkarılması", "giriş, pişmiş toprak kapağın çıkarılmasıyla sağlanmıştır")
q = "Kapağın iç yüzünde, kırmızımsı kahverengi tonlarda geometrik motifler gözlemlenmiştir"
S("BUILT", "Hipoje 2 (K-16) kapağının iç yüzü", "bears", "geometrik motifler", q)
S("BUILT", "Hipoje 2 (K-16) kapağındaki geometrik motifler", "colour", "kırmızımsı kahverengi tonlarda", q)
L("MEASURE", "Hipoje 2 (K-16)", "measures (inner length)", "253 cm", "İç uzunluğu 253 cm")
L("MEASURE", "Hipoje 2 (K-16)", "measures (width)", "100 cm", "İç uzunluğu 253 cm, genişliği 100 cm")
L("MEASURE", "Hipoje 2 (K-16)", "measures (height)", "173 cm", "yüksekliği 173 cm olan Hipoje")
q = "almaşık düzende örülmüş beşik tonoz formunda inşa edilmiştir"
S("BUILT", "Hipoje 2 (K-16)", "masonry", "almaşık düzende örülmüş", q)
S("BUILT", "Hipoje 2 (K-16)", "form", "beşik tonoz formunda", q)
S("DESCR", "Hipoje 2 (K-16)", "workmanship is judged", "oldukça özenli bir şekilde", "oldukça özenli bir şekilde, almaşık düzende örülmüş")
S("FIGURE", "Hipoje 2 (K-16)", "is shown in figure", "Resim: 5", "inşa edilmiştir (Resim: 5)")
S("BUILT", "Hipoje 2 (K-16) tabanı", "is paved with", "tuğla plakalar", "Mezarın tabanının tuğla plakalarla döşendiği")
S("BUILT", "Hipoje 2 (K-16) duvarları", "has plaster", "sıvasız", "yapılan duvarların sıvasız olduğu", neg=True)
S("BUILT", "Hipoje 2 (K-16)", "has part", "iki adet küçük niş", "iki adet küçük nişin varlığı tespit edilmiştir")
S("BUILT", "kemerli kapı (K-16 Hipoje 2)", "kind", "kemerli bir kapı", "içi tuğla ile örülmüş kemerli bir kapı tespit edilmiştir")
S("BUILT", "kemerli kapı (K-16 Hipoje 2)", "is located in", "Hipojenin kuzey duvarı", "Hipojenin kuzey duvarında, zeminden 39 cm yukarıda")
S("MEASURE", "kemerli kapı (K-16 Hipoje 2)", "measures (height above floor)", "39 cm", "Hipojenin kuzey duvarında, zeminden 39 cm yukarıda")
S("MEASURE", "kemerli kapı (K-16 Hipoje 2)", "measures (height)", "76 cm", "yüksekliği 76 cm ve genişliği 90")
S("MEASURE", "kemerli kapı (K-16 Hipoje 2)", "measures (width)", "90 cm", "yüksekliği 76 cm ve genişliği 90")
S("BUILT", "kemerli kapı (K-16 Hipoje 2)", "is filled with", "tuğla (içi tuğla ile örülmüş)", "içi tuğla ile örülmüş kemerli bir kapı tespit edilmiştir")
S("INTERP", "kemerli kapı alanı (K-16 Hipoje 2)", "certain evidence of function", "kesin bir bulgu olmamakla birlikte",
  "Bu alanın işlevine dair kesin bir bulgu olmamakla birlikte", neg=True)
S("INTERP", "kemerli kapı alanı (K-16 Hipoje 2)", "is interpreted as",
  "diğer Hipojelerle ulaşmak amacıyla yapılmış ve işlevini yitirerek iptal edilmiş bir geçit",
  "yitirerek iptal edilmiş bir geçit olabileceği düşünülmektedir", hedge="olabileceği düşünülmektedir")
q = "in situ halde birden fazla bireye ait iskelet kalıntılarıyla birlikte"
S("FIND", "iskelet kalıntıları (K-16 Hipoje 2)", "kind", "iskelet kalıntıları", q, hedge="İlk incelemelere göre")
S("FIND", "iskelet kalıntıları (K-16 Hipoje 2)", "count of individuals", "birden fazla birey", q, hedge="İlk incelemelere göre")
S("FIND", "iskelet kalıntıları (K-16 Hipoje 2)", "position in place", "in situ halde", q)
S("FIND", "iskelet kalıntıları (K-16 Hipoje 2)", "was found in", "Hipoje 2 mezar içi", "İlk incelemelere göre, mezar")
q = "bir adet testi formunda kap tespit edilmiştir"
S("FIND", "testi formunda kap (K-16 Hipoje 2)", "kind", "testi formunda kap", q)
S("FIND", "testi formunda kap (K-16 Hipoje 2)", "count", "bir adet", q)
S("FIND", "testi formunda kap (K-16 Hipoje 2)", "was found in", "Hipoje 2 mezar içi", q)
q = "Dağınık halde ele geçirilen cam boncuklar"
S("FIND", "cam boncuklar (K-16 Hipoje 2)", "kind", "boncuk", q)
S("FIND", "cam boncuklar (K-16 Hipoje 2)", "is made of", "cam", q)
S("FIND", "cam boncuklar (K-16 Hipoje 2)", "position in place", "dağınık halde", q)
S("FIND", "cam boncuklar (K-16 Hipoje 2)", "was found in", "Hipoje 2 mezar içi", "küpe de mezar içindeki diğer buluntular arasındadır")
q = "bir çift altın küpe de mezar içindeki diğer buluntular arasındadır"
S("FIND", "altın küpe (K-16 Hipoje 2)", "kind", "küpe", q)
S("FIND", "altın küpe (K-16 Hipoje 2)", "count", "bir çift", q)
S("FIND", "altın küpe (K-16 Hipoje 2)", "is made of", "altın", q)
S("FIND", "altın küpe (K-16 Hipoje 2)", "was found in", "Hipoje 2 mezar içi", q)
S("WORK", "Hipoje 2 (K-16) iskeletleri ve buluntuları", "work done",
  "laboratuvar ortamında detaylı incelemeler yapılmak üzere ayrı kasalara yerleştirilerek muhafaza edilmiştir",
  "yapılmak üzere ayrı kasalara yerleştirilerek muhafaza edilmiştir")
S("WORK", "Hipoje 2 (K-16)", "work done", "belgeleme işlemleri tamamlandı", "Belgeleme işlemleri tamamlandıktan")
S("INTERP", "Hipoje 3 (K-16)", "was at first interpreted as", "Hipojeler arası geçiş sağlayan bir koridor",
  "Başlangıçta Hipojeler arası geçiş sağlayan bir koridor olduğu düşünülen Hipoje 3’ün", hedge="Başlangıçta ... düşünülen")
S("INTERP", "Hipoje 3 (K-16)", "is interpreted as", "bebek ve çocuklar için inşa edilmiş Hipoje yapısı",
  "aslında bebek ve çocuklar için inşa edilmiş oldukça dar ve küçük bir Hipoje yapısı olduğu")
S("BUILT", "Hipoje 3 (K-16)", "has character", "oldukça dar ve küçük", "oldukça dar ve küçük bir Hipoje yapısı olduğu")
q = "dört bebeğe ait iskelet kalıntıları tespit edilmiştir"
S("FIND", "iskelet kalıntıları (K-16 Hipoje 3)", "kind", "bebeğe ait iskelet kalıntıları", q)
S("FIND", "iskelet kalıntıları (K-16 Hipoje 3)", "count of individuals", "dört bebek", q)
S("FIND", "iskelet kalıntıları (K-16 Hipoje 3)", "was found in", "Hipoje 3", q)
S("LAB", "iskelet kalıntıları (K-16 Hipoje 3)", "was examined by", "Antropolog (detaylı antropolojik incelemeler)",
  "Antropolog tarafından gerçekleştirilen detaylı antropolojik incelemeler")
L("MEASURE", "Hipoje 3 (K-16)", "measures (inner length)", "258 cm", "İç uzunluğu 258 cm")
L("MEASURE", "Hipoje 3 (K-16)", "measures (width)", "70 cm", "70 cm ve yüksekliği 180 cm")
L("MEASURE", "Hipoje 3 (K-16)", "measures (height)", "180 cm", "70 cm ve yüksekliği 180 cm")
q = "Hipoje duvarlarında herhangi bir sıva ya da bezeme bulunmamakla birlikte"
S("BUILT", "Hipoje 3 (K-16) duvarları", "has plaster", "bulunmamakla birlikte", q, neg=True)
S("BUILT", "Hipoje 3 (K-16) duvarları", "has decoration", "bulunmamakla birlikte", q, neg=True)
S("BUILT", "Hipoje 3 (K-16) doğu duvarı", "masonry", "tamamen tuğlayla örülmüş", "doğu duvarı tamamen tuğlayla örülmüşken")
S("BUILT", "Hipoje 3 (K-16) batı duvarı", "masonry", "almaşık düzende", "batı duvarının almaşık")

# ---------------------------------------------------------------- page 119
pg(119)
q = "Roma Dönemi nekropol alanında farklı yaş gruplarına yönelik Hipoje yapılarının varlığını ve gömü geleneklerindeki çeşitliliği"
S("DATE", "nekropol alanı", "is dated to period", "Roma Dönemi", "Roma Dönemi nekropol alanında")
S("INTERP", "Hipoje 3 incelemesi", "is interpreted as showing", "farklı yaş gruplarına yönelik Hipoje yapılarının varlığı", q)
S("INTERP", "Hipoje 3 incelemesi", "is interpreted as showing", "gömü geleneklerindeki çeşitlilik", q)
S("STRUCT", "başlık", "heading reads", "J-17 Plankaresi", "J-17 Plankaresi")
q = "+97,31 m seviyesinde tuğla zemin döşemesine rastlanmıştır"
S("BUILT", "tuğla zemin döşemesi (J-17)", "kind", "tuğla zemin döşemesi", q)
S("PLACE", "tuğla zemin döşemesi (J-17)", "elevation", "+97,31 m", q)
S("PLACE", "tuğla zemin döşemesi (J-17)", "position", "yüzeye oldukça yakın", "Yüzeye oldukça yakın olan bu zemin döşemesi")
S("BUILT", "tuğla zemin döşemesi (J-17)", "is made of", "pişmiş toprak plakalar", "40x40 cm ölçülerinde pişmiş toprak plakalardan oluşmaktadır")
S("MEASURE", "tuğla zemin döşemesi (J-17) pişmiş toprak plakaları", "measures", "40x40 cm", "40x40 cm ölçülerinde pişmiş toprak plakalardan oluşmaktadır")
S("BUILT", "tuğla zemin döşemesi (J-17)", "condition", "kırıklar ve çökmeler", "Zeminde kırıklar ve çökmeler gözlenmekle birlikte")
q = "toprağı içinden yoğun miktarda irili ufaklı demir çiviler ele geçmiştir"
S("FIND", "demir çiviler (J-17)", "kind", "çivi", q)
S("FIND", "demir çiviler (J-17)", "is made of", "demir", q)
S("FIND", "demir çiviler (J-17)", "count", "yoğun miktarda", q)
S("FIND", "demir çiviler (J-17)", "size", "irili ufaklı", q)
S("FIND", "demir çiviler (J-17)", "was found in", "kül toprağı", q)
S("MEASURE", "tuğla zemin döşemesi (J-17) kazılan alan içindeki sınırları", "measures (north-south)", "4,90 m", "kuzey-güney yönünde 4,90 m")
S("MEASURE", "tuğla zemin döşemesi (J-17) kazılan alan içindeki sınırları", "measures (east-west)", "3,04 m", "doğu-batı yönünde ise 3,04 m olarak ölçülmüştür")
S("BUILT", "payeler (J-17)", "kind", "taş ve harçla örülmüş payeler", "örülmüş payeler tespit edilmiştir")
S("BUILT", "payeler (J-17)", "position", "tuğla döşemenin batısında", "Tuğla döşemenin batısında birbirinden")
S("MEASURE", "payeler (J-17)", "measures (distance between them)", "174 cm", "174 cm aralıklı 83x70 cm ve 59x75 cm ölçülerinde")
S("MEASURE", "paye (J-17), birinci", "measures", "83x70 cm", "174 cm aralıklı 83x70 cm ve 59x75 cm ölçülerinde")
S("MEASURE", "paye (J-17), ikinci", "measures", "59x75 cm", "174 cm aralıklı 83x70 cm ve 59x75 cm ölçülerinde")
S("BUILT", "payeler (J-17)", "is made of", "taş ve harç", "sütun kaidesi olabilecek taş ve harçla")
S("INTERP", "payeler (J-17)", "is interpreted as", "sütun kaidesi", "sütun kaidesi olabilecek taş ve harçla", hedge="olabilecek")
S("INTERP", "tuğla döşeme (J-17)", "is interpreted as", "Bazilika’nın dışında yer alan atriuma (avlu) ait döşeme",
  "Bu alan muhtemelen Bazilika’nın dışında yer alan atriuma ait döşeme ve Portiko olmalıdır", hedge="muhtemelen ... olmalıdır")
S("INTERP", "payeler (J-17)", "is interpreted as belonging to", "Portiko",
  "Bu alan muhtemelen Bazilika’nın dışında yer alan atriuma ait döşeme ve Portiko olmalıdır", hedge="muhtemelen ... olmalıdır")
S("BUILT", "atrium", "position", "Bazilika’nın dışında", "Bazilika’nın dışında yer alan atriuma")
S("BUILT", "Çatkı Mezar 1 (J-17)", "kind", "Çatkı Mezar", "J-17 plankaresinde Çatkı Mezar 1’in kuzey yönündeki")
S("BUILT", "Çatkı Mezar 1 (J-17)", "condition", "kuzey yönündeki ilk kapağı açılabilir", "Çatkı Mezar 1’in kuzey yönündeki ilk kapağının açılabilir olduğu")
S("BUILT", "Çatkı Mezar 2 (J-17)", "kind", "Çatkı Mezar", "Çatkı Mezar 2’nin ise kapaklarının")
S("BUILT", "Çatkı Mezar 2 (J-17) kapakları", "lies below", "zemin döşemesi (büyük çoğunluğu)",
  "Çatkı Mezar 2’nin ise kapaklarının büyük çoğunluğunun zemin döşemesinin altında olması sebebiyle")
S("WORK", "Çatkı Mezar 2 (J-17)", "decision", "[unclear] belgelenerek olduğu haliyle korunması (kararın ÇM 1'i de kapsayıp kapsamadığı belirsiz)",
  "belgelenerek olduğu haliyle korunmasına karar verilmiştir")
S("FIGURE", "tuğla döşeme ve payeler (J-17)", "is shown in figure", "Resim: 6", "düşünülmektedir (Resim: 6)")
S("STRUCT", "başlık", "heading reads", "L-18 Plankaresi", "L-18 Plankaresi")
S("WORK", "L-18 plankaresi çalışmaları", "advanced towards", "plankarenin güney yönü", "Plankarenin güney yönünde ilerleyen çalışmalar sırasında")
q = "64x64 cm ölçülerindeki terrakota içbükey plaka kapağın tamamı açığa çıkarılmıştır"
S("BUILT", "Hipoje 1 (L-18) plaka kapağı", "kind", "terrakota içbükey plaka kapak", q)
S("MEASURE", "Hipoje 1 (L-18) plaka kapağı", "measures", "64x64 cm", q)
S("WORK", "Hipoje 1 (L-18) plaka kapağı", "was exposed (extent)", "tamamı", q)
L("MEASURE", "Hipoje 1 (L-18)", "measures (inner length)", "424 cm", "uzunluğu 424 cm")
L("MEASURE", "Hipoje 1 (L-18)", "measures (width)", "230 cm", "genişliği 230 cm")
L("MEASURE", "Hipoje 1 (L-18)", "measures (height)", "180 cm", "yüksekliği 180 cm olan mezarın tonoz bölümünün")
S("BUILT", "Hipoje 1 (L-18) tonoz bölümü", "is made of", "tuğla", "mezarın tonoz bölümünün tuğladan")
S("BUILT", "Hipoje 1 (L-18) duvarları", "is made of", "moloz taş", "duvarlarının ise moloz taş ile inşa edildiği")
S("BUILT", "Hipoje 1 (L-18)", "is coated with", "beyaz renkli bir sıva", "beyaz renkli bir sıva ile kaplandığı")
S("BUILT", "Hipoje 1 (L-18) orijinal girişi", "count of entrance points", "iki farklı nokta", "Mezarın orijinal girişinin iki farklı noktadan sağlandığı anlaşılmıştır")
S("BUILT", "Hipoje 1 (L-18) ilk girişi", "is located in", "mezar tonozunun kuzeydoğu köşesi", "mezar tonozunun kuzeydoğu köşesine yerleştirilmiş terrakota içbükey bir plaka kapak")
S("BUILT", "Hipoje 1 (L-18) ilk girişi", "is closed with", "terrakota içbükey bir plaka kapak", "mezar tonozunun kuzeydoğu köşesine yerleştirilmiş terrakota içbükey bir plaka kapak")
q = "ikinci girişin güney lunette bölümünde yer alan bir kapı"
S("INTERP", "Hipoje 1 (L-18) ikinci girişi", "is interpreted as", "güney lunette bölümünde yer alan bir kapı açıklığı", q, hedge="olduğu düşünülmektedir")
S("MEASURE", "Hipoje 1 (L-18) kapı açıklığı", "measures", "80x48 cm", "açıklığı (80x48 cm) olduğu düşünülmektedir")
S("BUILT", "kline (L-18 Hipoje 1)", "kind", "kline", "Hipojenin güney kısmında bir kline")
S("BUILT", "kline (L-18 Hipoje 1)", "is located in", "Hipojenin güney kısmı", "Hipojenin güney kısmında bir kline")
S("HISTORY", "kline (L-18 Hipoje 1)", "was destroyed by", "kaçak kazılar (tamamen yok edildi)", "ancak kaçak kazılar sonucu tamamen yok edildiğini ortaya koymuştur")
S("DOC", "cümle: Hipojenin güney kısmında bir kline ... ortaya koymuştur", "subject of the sentence", "[unclear] neyin ortaya koyduğu yazılmamış",
  "ancak kaçak kazılar sonucu tamamen yok edildiğini ortaya koymuştur")
S("WORK", "kline (L-18 Hipoje 1) ölçüleri", "were taken from", "mevcut izler", "izlere dayanarak yapılan ölçümlere göre")
L("MEASURE", "kline (L-18 Hipoje 1)", "measures (height)", "yaklaşık 70 cm", "kline yaklaşık 70 cm yüksekliğinde", hedge="yaklaşık")
L("MEASURE", "kline (L-18 Hipoje 1)", "measures (north-south)", "1,05 m", "yönünde 1,05 m, doğu-batı yönünde ise 2,30 m genişliğindedir")
L("MEASURE", "kline (L-18 Hipoje 1)", "measures (east-west)", "2,30 m", "yönünde 1,05 m, doğu-batı yönünde ise 2,30 m genişliğindedir")
S("PLACE", "Hipoje 2 (L-18)", "elevation", "97,87 metre", "97,87 metre seviyesinde")
S("BUILT", "Hipoje 2 (L-18)", "kind", "Hipoje", "tahrip edilmiş olan Hipoje 2’de mezar içi")
S("HISTORY", "Hipoje 2 (L-18)", "was damaged by", "kaçak kazıcılar", "tespit edilen ve kaçak kazıcılar tarafından tahrip edilmiş olan Hipoje 2’de")
S("WORK", "Hipoje 2 (L-18) mezar içi çalışmaları", "started after", "plankare seviye çalışmalarının tamamlanması",
  "Plankare seviye çalışmalarının tamamlanmasının ardından")
q = "açılan 30x50 cm ölçülerindeki bir açıklıktan mezar içine giriş sağlanmıştır"
S("BUILT", "açıklık (L-18 Hipoje 2)", "is located in", "Hipojenin kuzey kısmı, tepe kısmı", "Hipojenin kuzey kısmında, tepe kısmında kaçak kazıcılar")
S("HISTORY", "açıklık (L-18 Hipoje 2)", "was opened by", "kaçak kazıcılar", "Hipojenin kuzey kısmında, tepe kısmında kaçak kazıcılar")
S("MEASURE", "açıklık (L-18 Hipoje 2)", "measures", "30x50 cm", q)
S("WORK", "Hipoje 2 (L-18)", "was entered through", "kaçak kazıcıların açtığı açıklık", q)
S("BUILT", "Hipoje 2 (L-18) tonoz bölümü", "is made of", "tuğla", "mezarın tonoz bölümünün tuğla, duvarların ise")
S("BUILT", "Hipoje 2 (L-18) duvarları", "is made of", "taş", "taş ile örüldüğü ve duvarların inşasında kullanılan harç ile sıvandığı")
S("BUILT", "Hipoje 2 (L-18) duvarları", "is plastered with", "duvarların inşasında kullanılan harç", "taş ile örüldüğü ve duvarların inşasında kullanılan harç ile sıvandığı")
S("BUILT", "kline (L-18 Hipoje 2)", "kind", "kline", "kuzey cephesinde bir")
S("BUILT", "kline (L-18 Hipoje 2)", "is located in", "kuzey cephesi", "kuzey cephesinde bir")
S("HISTORY", "kline (L-18 Hipoje 2)", "was destroyed by", "kaçak kazıcılar (tamamen yok edildi)", "ancak kaçak kazıcılar tarafından tamamen yok edildiği")
L("MEASURE", "kline (L-18 Hipoje 2)", "measures (height)", "64 cm", "klinenin 64 cm yüksekliğinde, doğu-batı yönünde 2,30 m ve", hedge="değerlendirilmiştir")
L("MEASURE", "kline (L-18 Hipoje 2)", "measures (east-west)", "2,30 m", "klinenin 64 cm yüksekliğinde, doğu-batı yönünde 2,30 m ve", hedge="değerlendirilmiştir")

# ---------------------------------------------------------------- page 120
pg(120)
L("MEASURE", "kline (L-18 Hipoje 2)", "measures (north-south)", "1,05 m", "kuzey-güney yönünde 1,05 m ölçülerinde olduğu değerlendirilmiştir", hedge="değerlendirilmiştir")
L("MEASURE", "Hipoje 2 (L-18)", "measures (inner length)", "326 cm", "İç uzunluğu 326 cm")
L("MEASURE", "Hipoje 2 (L-18)", "measures (width)", "228 cm", "genişliği 228 cm ve yüksekliği 178 cm")
L("MEASURE", "Hipoje 2 (L-18)", "measures (height)", "178 cm", "genişliği 228 cm ve yüksekliği 178 cm")
S("BUILT", "Hipoje 2 (L-18) orijinal giriş bölümü", "has part", "merdivenler", "mezarın orijinal giriş bölümünde merdivenlerin bulunduğu")
S("HISTORY", "Hipoje 2 (L-18) merdiven basamakları", "were removed by", "kaçak kazıcılar (büyük çoğunluğu)",
  "merdiven basamaklarının büyük çoğunluğunun kaçak kazıcılar tarafından söküldüğü")
S("STRUCT", "başlık", "heading reads", "MİMARİ BELGELEME VE KORUMA PROJELERİ", "MİMARİ BELGELEME VE KORUMA PROJELERİ")
S("WORK", "mimari belgeleme çalışmaları", "had the aim", "Nekropol alanının arkeolojik ve mimari özelliklerini detaylı bir şekilde incelemek ve belgelemek",
  "arkeolojik ve mimari özelliklerini detaylı bir şekilde incelemek ve belgelemek amacıyla yürütülmüştür")
q = "Neval Sarıtekin ile Doruk Bayrak tarafından gerçekleştirilmiştir"
S("PEOPLE", "Neval Sarıtekin", "role in the work", "alanın mimari belgelerinin hazırlanması", q)
S("PEOPLE", "Doruk Bayrak", "role in the work", "alanın mimari belgelerinin hazırlanması", q)
q = "üç boyutlu vaziyet görüntüleri, plan ve kesit rölöve çizimleriyle kapsamlı bir şekilde belgelenmiştir"
L("WORK", "Nekropol", "was documented with", "üç boyutlu vaziyet görüntüleri", q)
L("WORK", "Nekropol", "was documented with", "plan rölöve çizimleri", q)
L("WORK", "Nekropol", "was documented with", "kesit rölöve çizimleri", q)
S("FIGURE", "mimari belgeleme", "is shown in figure", "Çizim: 2", "belgelenmiştir (Çizim: 2)")
S("STRUCT", "başlık", "heading reads", "Geçici Çatı Örtüsü", "Geçici Çatı Örtüsü")
S("DESCR", "arkeolojik kazı alanlarında yapılan çalışmalar", "general statement", "uygun koruma önlemlerini zorunlu kılar",
  "uygun koruma önlemlerini zorunlu kılar")
S("DESCR", "geçici çatı örtülerinin kullanılması", "is judged", "önemlidir (çevresel faktörlerin kazı alanına zarar vermesini önlemek amacıyla)",
  "geçici çatı örtülerinin kullanılması önemlidir")
q = "çevresel faktörlerin (güneş, yağmur, rüzgar vb.)"
for v in ["güneş", "yağmur", "rüzgar"]:
    L("DESCR", "çevresel faktörler", "includes", v, q)
S("WORK", "mevcut çatı örtüleri", "is made of", "branda", "mevcut branda ile yapılmış çatı örtülerinin")
S("ADMIN", "mevcut branda ile yapılmış çatı örtüleri", "was judged sufficient", "yeterli olmadığı belirlenmiş",
  "çatı örtülerinin yeterli olmadığı belirlenmiş", neg=True, who="Kültür ve Turizm Bakanlığından gelen uzmanlar")
S("ADMIN", "Kültür ve Turizm Bakanlığından gelen uzmanlar", "role in the work", "çatı örtülerini incelediler",
  "Kültür ve Turizm Bakanlığından gelen uzmanların incelemeleri sonucunda")
S("WORK", "çatı örtüleri", "decision", "yerine geçici ancak daha dayanıklı bir sistemin inşa edilmesi",
  "daha dayanıklı bir sistemin inşa edilmesine karar verilmiştir")
q = "çelik iskelet ve trapez çatı örtüsü kullanılarak oluşturulmuş"
S("WORK", "yeni yapılan çatılar", "is made of", "çelik iskelet", q)
S("WORK", "yeni yapılan çatılar", "is made of", "trapez çatı örtüsü", q)
S("DESCR", "yeni yapılan çatılar", "is judged", "geçici fakat sağlam bir yapı", "geçici fakat sağlam bir yapı olması sağlanmıştır")
q = "kazı alanının zeminine müdahale etmeyen ve taşınabilir beton ayaklar ile desteklenmiştir"
S("WORK", "yeni yapılan çatılar", "is supported by", "taşınabilir beton ayaklar", q)
S("WORK", "beton ayaklar", "intervene in the ground of the excavation area", "müdahale etmeyen", q, neg=True)
S("FIGURE", "geçici çatı", "is shown in figure", "Resim: 7", "desteklenmiştir (Resim: 7)")
S("DESCR", "çatıların tasarımı", "took into account", "dayanıklılık, işlevsellik ve pratiklik",
  "sadece dayanıklılık değil, aynı zamanda işlevsellik ve pratiklik de göz önünde bulundurulmuştur")
S("WORK", "çatılar", "provide", "yeterli ışık ve hava sirkülasyonu", "yeterli ışık ve hava sirkülasyonu sağlanarak")
S("DESCR", "kullanılan malzemeler", "is judged", "çevresel etkilere karşı dirençli; bakım maliyetlerini azaltmakta, uzun süreli kullanıma olanak tanımakta",
  "çevresel etkilere karşı dirençli olması ise hem bakım maliyetlerini azaltmakta")
S("DESCR", "bu tür uygulamalar", "is judged", "kültürel mirasın zarar görmeden geleceğe aktarılmasına katkı sağlamaktadır",
  "kültürel mirasın zarar görmeden geleceğe aktarılmasına katkı sağlamaktadır")
S("DESCR", "geçici çatı sistemlerinin tasarımı", "is judged", "alanın özgünlüğünü koruyacak hassasiyetin gösterilmesi büyük önem taşımaktadır",
  "koruyacak hassasiyetin gösterilmesi büyük önem taşımaktadır")
S("STRUCT", "başlık", "heading reads", "SERAMİK VE KÜÇÜK BULUNTU DEĞERLENDİRME ÇALIŞMALARI", "SERAMİK VE KÜÇÜK BULUNTU DEĞERLENDİRME ÇALIŞMALARI")
q = "Gizem Sevinç Memiş ve Beyza Davdav tarafından gerçekleştirilmiştir"
S("PEOPLE", "Gizem Sevinç Memiş", "role in the work", "seramik ve küçük buluntu çalışmaları", q)
S("PEOPLE", "Beyza Davdav", "role in the work", "seramik ve küçük buluntu çalışmaları", q)
S("FIND", "2024 yılı seramikleri", "count", "1.970 adet", "ele geçen seramik sayısı 1.970 adettir")
q = "E-15, E-16, J-15, J-17, J-18, J-K-18, K-16, K-17, K-18, K-L-15-16, L-17 Kuzey Batı Kesit ve L-18 açmasında"
for v in ["E-15", "E-16", "J-15", "J-17", "J-18", "J-K-18", "K-16", "K-17", "K-18", "K-L-15-16", "L-17 Kuzey Batı Kesit", "L-18"]:
    L("FIND", "2024 yılı seramikleri", "was found in trench", v, q)
S("FIND", "analizi yapılıp alınan seramik", "count", "559 adet", "Analizi yapılıp alınan seramik sayısı 559 adet")
S("FIND", "atılan seramik", "count", "1.411 adettir", "atılan seramik sayısı 1.411 adettir")

# ---------------------------------------------------------------- page 121
pg(121)
L("DATE", "2024 yılında ele geçen seramikler", "share dated to Roma Dönemi", "%68 (çoğunluğu)", "çoğunluğu Roma Dönemi’ne (%68) tarihlenmiş")
L("DATE", "2024 yılında ele geçen seramikler", "share dated to Helenistik Dönem", "%31", "Helenistik Dönem (%31)")
L("DATE", "2024 yılında ele geçen seramikler", "share dated to Bizans Dönemi", "%1 (çok az sayıda)", "çok az sayıda Bizans Dönemi (%1) seramikleri gelmektedir")
S("FIGURE", "2024 yılı seramikleri", "is shown in figure", "Çizim: 3", "seramikleri gelmektedir (Çizim: 3)")

# ceramics per trench: (page, trench, bags, bagquote, period, pct, densquote, extra shares, kinds)
# kinds: (name, period, date, quote)
R = "Roma Dönemi"
H = "Helenistik Dönem"
B = "Bizans Dönemi"
cer = [
    (121, "E-15", "17 poşet", "E-15 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 17 poşet seramik",
     R, "%77", "E-15 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%77)", [],
     [("Mermer Seramikleri", "", "", "Mermer Seramikleri ve pişirme kapları da bulunmaktadır"),
      ("pişirme kapları", "", "", "Mermer Seramikleri ve pişirme kapları da bulunmaktadır"),
      ("tam firnisli tabaklar", H, "", "Helenistik Dönem’e ait tam firnisli tabaklar"),
      ("kırmızı hamurlu tabaklar", B, "", "Bizans Dönemi’ne ait kırmızı hamurlu tabaklar bulunmaktadır")]),
    (121, "E-16", "11 poşet", "E-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 11 poşet seramik",
     R, "%61", "E-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%61)", [],
     [("tabaklar", R, "", "Roma Dönemi’ne ait tabaklar bulunmaktadır")]),
    (121, "J-15", "1 poşet", "J-15 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 1 poşet seramiğin",
     H, "%50", "toplam 1 poşet seramiğin genel yoğunluğu Helenistik Dönem’e aittir (%50)", [],
     [("Tam Firnisli tabaklar", "", "", "Tam Firnisli tabaklar bulunmaktadır")]),
    (121, "J-17", "8 poşet", "J-17 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 8 poşet seramik",
     R, "%85", "J-17 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%85)", [],
     [("pişirme kapları", "", "", "pişirme kapları ve yerel tip kandiller (MS 4.-6. yy.) bulunmaktadır"),
      ("yerel tip kandiller", "", "MS 4.-6. yy.", "pişirme kapları ve yerel tip kandiller (MS 4.-6. yy.) bulunmaktadır")]),
    (121, "J-18", "5 poşet", "J-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 5 poşet seramik",
     R, "%58", "J-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%58)", [],
     [("günlük kullanım kapları", R, "", "Roma Dönemi’ne ait günlük kullanım kapları bulunmaktadır")]),
    (121, "J-K-18", "5 poşet", "J-K-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 5 poşet seramik",
     R, "%62", "genel yoğunluğu Roma Dönemi’ne aittir (%62)", [],
     [("amphoralar", R, "", "Roma Dönemi’ne ait amphoralar ve mermer seramikleri (MS 3.-4. yy.) bulunmaktadır"),
      ("mermer seramikleri", R, "MS 3.-4. yy.", "Roma Dönemi’ne ait amphoralar ve mermer seramikleri (MS 3.-4. yy.) bulunmaktadır")]),
    (121, "K-16", "10 poşet", "K-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 10 poşet seramik",
     R, "%61", "K-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%61)",
     [(H, "%39", "Helenistik Dönem’e (%39) ait Megara kaseleri")],
     [("günlük kullanım kapları", R, "", "Roma Dönemi’ne ait günlük kullanım kapları bulunmaktadır"),
      ("Megara kaseleri", H, "", "Helenistik Dönem’e (%39) ait Megara kaseleri, gri siyah ve tam firnisli tabaklar"),
      ("gri siyah tabaklar", H, "", "Helenistik Dönem’e (%39) ait Megara kaseleri, gri siyah ve tam firnisli tabaklar"),
      ("tam firnisli tabaklar", H, "", "Helenistik Dönem’e (%39) ait Megara kaseleri, gri siyah ve tam firnisli tabaklar")]),
    (121, "K-17", "8 poşet", "K-17 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 8 poşet seramik",
     R, "%77", "K-17 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%77)", [],
     [("Filistin Amphorası", R, "MS 5.-6. yy.", "Filistin Amphorası (MS 5.-6. yy.)"),
      ("Yerel Tip Kandiller", R, "MS 3.-4. yy.", "Yerel Tip Kandiller (MS 3.-4. yy.)"),
      ("Günlük Kullanım Kapları", R, "", "Yerel Tip Kandiller (MS 3.-4. yy.) ve Günlük Kullanım Kapları bulunmaktadır")]),
    (121, "K-18", "6 poşet", "K-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 6 poşet seramik",
     R, "%67", "K-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%67)",
     [(H, "%33", "(%33) ait basit ve tam firnisli tabaklar da bulunmaktadır")],
     [("yerel tip kandiller", R, "MS 4.-6. yy.", "yerel tip kandiller (MS 4.-6. yy.) ve Günlük Kullanım kapları bulunmaktadır"),
      ("Günlük Kullanım kapları", R, "", "yerel tip kandiller (MS 4.-6. yy.) ve Günlük Kullanım kapları bulunmaktadır"),
      ("basit firnisli tabaklar", H, "", "(%33) ait basit ve tam firnisli tabaklar da bulunmaktadır"),
      ("tam firnisli tabaklar", H, "", "(%33) ait basit ve tam firnisli tabaklar da bulunmaktadır")]),
    (121, "K-L-15-16", "4 poşet", "K-L-15-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 4 poşet seramik",
     R, "%74", "K-L-15-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%74)", [],
     [("Yerel Tip Kandiller", R, "MS 4.-6. yy.", "Yerel Tip Kandiller (MS 4.-6. yy.) ve Günlük Kullanım Kapları bulunmaktadır"),
      ("Günlük Kullanım Kapları", R, "", "Yerel Tip Kandiller (MS 4.-6. yy.) ve Günlük Kullanım Kapları bulunmaktadır")]),
    (122, "L-17 Kuzey Batı Kesit", "2 poşet", "açmasında yapılan kazı çalışmalarında analizi yapılan toplam 2 poşet seramik vardır",
     R, "%74", "Seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%74)", [],
     [("pişirme kapları", R, "", "Roma Dönemi’ne ait pişirme kapları, kandil kulbu ve mermer seramikleri bulunmaktadır"),
      ("kandil kulbu", R, "", "Roma Dönemi’ne ait pişirme kapları, kandil kulbu ve mermer seramikleri bulunmaktadır"),
      ("mermer seramikleri", R, "", "Roma Dönemi’ne ait pişirme kapları, kandil kulbu ve mermer seramikleri bulunmaktadır")]),
    (122, "L-18", "6 poşet", "L-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 6 poşet seramik vardır",
     R, "%63", "L-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%63)",
     [(H, "%35", "Helenistik Dönem’e (%35) ait Megara kaseleri")],
     [("pişirme kapları", R, "", "Roma Dönemi’ne ait pişirme kapları ve tabaklar"),
      ("tabaklar", R, "", "Roma Dönemi’ne ait pişirme kapları ve tabaklar"),
      ("Megara kaseleri", H, "", "Helenistik Dönem’e (%35) ait Megara kaseleri ve basit firnisli tabaklar bulunmaktadır"),
      ("basit firnisli tabaklar", H, "", "Helenistik Dönem’e (%35) ait Megara kaseleri ve basit firnisli tabaklar bulunmaktadır")]),
]
first122 = True
for page, tr, bags, bq, per, pct, dq, extra, kinds in cer:
    pg(page)
    if page == 122 and first122:
        first122 = False
    L("FIND", tr + " açması analizi yapılan seramik", "count (bags)", bags, bq)
    L("DATE", tr + " açması seramikleri", "general density belongs to period", per, dq)
    L("DATE", tr + " açması seramikleri", "share of " + per, pct, dq)
    for ep, epct, eq in extra:
        L("DATE", tr + " açması seramikleri", "share of " + ep, epct, eq)
    for name, kp, kd, kq in kinds:
        subj = name + " (" + tr + " açması)"
        L("FIND", subj, "kind", name, kq)
        L("FIND", subj, "was found in", tr + " açması", kq)
        if kp:
            L("DATE", subj, "is dated to period", kp, kq)
        if kd:
            L("DATE", subj, "is dated to", kd, kq)

# ---------------------------------------------------------------- page 122
pg(122)
S("STRUCT", "başlık", "heading reads", "RESTORASYON VE KONSERVASYON ÇALIŞMALARI", "RESTORASYON VE KONSERVASYON ÇALIŞMALARI")
S("PEOPLE", "Tuğçe Güçlü", "role in the work", "konservasyon çalışmaları", "Arkeolog/Restoratör Tuğçe Güçlü tarafından gerçekleştirilmiştir")
S("PEOPLE", "Tuğçe Güçlü", "title", "Arkeolog/Restoratör", "Arkeolog/Restoratör Tuğçe Güçlü tarafından gerçekleştirilmiştir")
q = "1 adet pişmiş toprak testi, 1 adet metal obje, bir çift altın küpe ve 6 adet bronz sikke konservasyon amacıyla teslim alınmıştır"
q = "1 adet pişmiş toprak testi, 1 adet metal obje, bir çift altın küpe ve 6 adet bronz sikke konservasyon amacıyla teslim alınmıştır"[:200]
L("LAB", "pişmiş toprak testi", "count received for conservation", "1 adet", q)
L("FIND", "pişmiş toprak testi", "is made of", "pişmiş toprak", q)
L("LAB", "metal obje", "count received for conservation", "1 adet", q)
L("FIND", "metal obje", "kind", "metal obje", q)
L("FIND", "metal obje", "is made of", "metal", q)
L("LAB", "altın küpe", "count received for conservation", "bir çift", q)
L("LAB", "bronz sikke", "count received for conservation", "6 adet", q)
S("LAB", "eserler", "conservation step", "öncelikle kayıt altına alınmış", "Eserler, öncelikle kayıt altına alınmış")
q = "yüzeydeki korozyonun yumuşatılması amacıyla %50 oranında saf su ve alkol karışımı kullanılmıştır"
S("LAB", "metal eserlerin temizliği", "substance used", "%50 oranında saf su ve alkol karışımı", q)
S("LAB", "metal eserlerin temizliği", "aim of the substance", "yüzeydeki korozyonun yumuşatılması", q)
S("LAB", "metal eserler", "conservation step", "mikroskop altında mekanik temizlik", "eserlerin mikroskop altında mekanik temizliği gerçekleştirilmiştir")
q = "bisturi, bambu çubuk, çeşitli fırçalar ve dişçi motoru gibi profesyonel ekipmanlar kullanılmıştır"
for v in ["bisturi", "bambu çubuk", "çeşitli fırçalar", "dişçi motoru"]:
    L("LAB", "metal eserlerin mekanik temizliği", "tool used", v, q)
q = "oranında Paraloid B72 çözeltisi uygulanmıştır"
S("LAB", "metal eser ve sikkeler", "substance applied", "%3 oranında Paraloid B72 çözeltisi", "koruma ve stabilizasyon amacıyla %3")
S("LAB", "Paraloid B72 çözeltisi uygulaması", "aim", "koruma ve stabilizasyon", "koruma ve stabilizasyon amacıyla %3")
S("LAB", "eserler", "conservation step", "uygun koşullarda muhafaza edilmek üzere kaldırılmıştır", "edilmek üzere kaldırılmıştır (Resim: 8)")
S("FIGURE", "konservasyonu yapılan eserler", "is shown in figure", "Resim: 8", "edilmek üzere kaldırılmıştır (Resim: 8)")
q = "yüzeydeki kalker tabakasının yumuşaması için %50 oranında saf su ve alkol karışımı"
S("FIND", "pişmiş toprak testi", "condition", "yüzeyde kalker tabakası", q)
S("LAB", "pişmiş toprak testinin temizliği", "substance used", "%50 oranında saf su ve alkol karışımı", q)
S("LAB", "pişmiş toprak testi", "conservation step", "paketleme yöntemiyle karışım içinde bekletilmiş", "eser, paketleme yöntemiyle karışım içinde bekletilmiş")
S("LAB", "pişmiş toprak testi", "conservation step", "yumuşayan kalker tabakası mekanik yöntemlerle temizlenmiştir",
  "yumuşayan kalker tabakası çeşitli bisturi uçları kullanılarak mekanik yöntemlerle")
S("LAB", "pişmiş toprak testinin temizliği", "tool used", "çeşitli bisturi uçları", "yumuşayan kalker tabakası çeşitli bisturi uçları kullanılarak mekanik yöntemlerle")
S("LAB", "pişmiş toprak testi", "conservation step", "uygun şekilde muhafaza edilmek üzere teslim edilmiştir", "uygun şekilde muhafaza edilmek üzere")
S("FIGURE", "pişmiş toprak testi", "is shown in figure", "Resim: 9", "edilmiştir (Resim: 9)")
S("STRUCT", "başlık", "heading reads", "ANTROPOLOJİ ÇALIŞMALARI", "ANTROPOLOJİ ÇALIŞMALARI")
S("PEOPLE", "Ruken Zeynep Köse", "role in the work", "antropoloji çalışmaları", "Antropolog Ruken Zeynep Köse tarafından gerçekleştirilmiştir")
q = "Önceki yıllarda ortaya çıkarılan Hipoje 2022-1 ve Hipoje 2023-1’e ait iskelet kalıntıları detaylı bir şekilde belgelenmiştir"
for h in ["Hipoje 2022-1", "Hipoje 2023-1"]:
    S("WORK", h, "was exposed in", "önceki yıllarda", "Önceki yıllarda ortaya çıkarılan Hipoje 2022-1 ve Hipoje")
    S("LAB", h + " iskelet kalıntıları", "work done", "detaylı bir şekilde belgelenmiştir", "ait iskelet kalıntıları detaylı bir şekilde belgelenmiştir")
q = "cinsiyet, yaş tayini ve hastalıklarla ilgili detaylı incelemeler yapılmıştır"
for v in ["cinsiyet", "yaş tayini", "hastalıklar"]:
    L("LAB", "2024 yılında bulunan Hipojeler, Sanduka Mezar ve Çatkı Mezarlar içinden çıkan iskeletler", "was examined for", v, q)
S("LAB", "cinsiyet belirleme", "bones examined first", "cranium ve pelvis kemikleri", "ilk olarak cranium ve pelvis kemikleri incelenmiştir")
crit = [("craniumda bulunan mastoid çıkıntıların yapısı", "craniumda bulunan mastoid çıkıntıların yapısı"),
        ("kaş kemerleri ve glabellanın belirginliği", "kaş kemerleri ve"),
        ("orbitaların şekli", "orbitaların şekli"),
        ("mandibula kemiklerinin özellikleri", "mandibula kemiklerinin özellikleri"),
        ("uzun kemiklerdeki kas tutunma izleri", "kas tutunma izleri dikkate alınmıştır")]
for v, qq in crit:
    L("LAB", "cinsiyet belirleme", "criterion used", v, qq)
S("LAB", "yaş tayini", "method", "yaş grupları için farklı teknik ve yöntem", "yaş grupları için")
L("LAB", "bebek ve çocukların yaş tayini", "criterion used", "diş sürme süreci", "diş sürme süreci ve sağlam olan uzun kemiklerden ölçüm alınarak belirlenmiştir")
L("LAB", "bebek ve çocukların yaş tayini", "criterion used", "sağlam olan uzun kemiklerden ölçüm", "diş sürme süreci ve sağlam olan uzun kemiklerden ölçüm alınarak belirlenmiştir")

# ---------------------------------------------------------------- page 123
pg(123)
L("LAB", "genç erişkinlerin yaş tayini", "criterion used", "epifiz kaynaşması", "epifiz kaynaşması, diş köklerinin kapanma dereceleri dikkate alınmıştır")
L("LAB", "genç erişkinlerin yaş tayini", "criterion used", "diş köklerinin kapanma dereceleri", "epifiz kaynaşması, diş köklerinin kapanma dereceleri dikkate alınmıştır")
for v, qq in [("cranium sütural kapanma dereceleri", "cranium sütural kapanma dereceleri"),
              ("symphysial yaşlandırma", "symphysial yaşlandırma"),
              ("dental aşınma derecesi", "derecesi ve clavicula kemiğinin uçlarına bakılarak yapılmıştır"),
              ("clavicula kemiğinin uçları", "derecesi ve clavicula kemiğinin uçlarına bakılarak yapılmıştır")]:
    L("LAB", "erişkin bireylerin yaş tayini", "criterion used", v, qq)
q = "farklı mezar tipleri, gömü türleri, mezar içindeki"
for v, qq in [("farklı mezar tipleri", q), ("gömü türleri", q), ("mezar içindeki yatış pozisyonları", "ve ritüeller gözlemlenmiştir"),
              ("ritüeller", "ve ritüeller gözlemlenmiştir")]:
    L("LAB", "antropolojik sonuç", "observed", v, qq)
S("DESCR", "antropolojik bulgular", "is judged", "dönemin sosyo-kültürel yapısı ve inanç sistemleri hakkında önemli bilgiler sunmaktadır",
  "inanç sistemleri hakkında önemli bilgiler sunmaktadır")
S("FIND", "bazı mezarların içerisinde yer alan iskeletler", "condition", "fazlasıyla zarar görmüş (çevresel, fiziksel ve toprak yapısı ile alakalı olarak)",
  "iskeletler çevresel, fiziksel ve toprak yapısı ile alakalı olarak fazlasıyla zarar görmüştür")
S("HISTORY", "Hisardere alanı", "was used earlier for", "tarım", "Hisardere alanının önceki zamanlarda tarım amaçlı kullanılması")
S("INTERP", "iskeletlerin zarar görmesi", "most important cause is", "Hisardere alanının önceki zamanlarda tarım amaçlı kullanılması",
  "tarım amaçlı kullanılması bu durumun en önemli sebebidir")
q = "Schormol nodülü, osteoartrit gibi hastalıklar"
S("LAB", "kemikler (özellikle vertebralar)", "disease observed", "Schormol nodülü", q)
S("LAB", "kemikler (özellikle vertebralar)", "disease observed", "osteoartrit", q)
S("INTERP", "Schormol nodülü, osteoartrit gibi hastalıklar", "is interpreted as showing", "bireylerin ağır ve fiziksel işlerde çalıştığı",
  "bireylerin ağır ve fiziksel işlerde çalıştığını göstermektedir")
S("LAB", "dişler", "observed", "aşınmalar ve kırıklar", "dişlerdeki aşınmalar ve kırıklar")
S("INTERP", "dişlerdeki aşınmalar ve kırıklar", "is interpreted as showing", "dişlerin günlük yaşamda bir alet ya da “üçüncü el” gibi kullanıldığı",
  "da “üçüncü el” gibi kullanıldığını ortaya koymakta")
S("DESCR", "dişlerin alet gibi kullanılması", "is judged to inform on", "bireylerin sosyo-ekonomik koşulları",
  "bireylerin sosyo-ekonomik koşulları hakkında bilgi sağlamaktadır")
S("LAB", "dişler", "observed", "hipoplaziler", "Dişlerde gözlemlenen hipoplaziler")
S("INTERP", "dişlerde gözlemlenen hipoplaziler", "is interpreted as showing", "çocukluk döneminde besin yetersizliğinin ve stres düzeyinin yüksek olduğu",
  "döneminde besin yetersizliğinin ve stres düzeyinin yüksek olduğunun göstergesidir")
q = "metabolik ve enfeksiyonel hastalıkların varlığı da gözlemlenmiştir"
S("LAB", "iskeletler", "disease observed", "metabolik hastalıklar", q)
S("LAB", "iskeletler", "disease observed", "enfeksiyonel hastalıklar", q)
S("LAB", "metabolik hastalıklar", "observed especially in", "çocuklar", "Özellikle çocuklarda izlenen metabolik hastalıkların nedeni")
q = "izlenen metabolik hastalıkların nedeni, beslenme yetersizliği, anne sütü bakımından"
S("INTERP", "çocuklarda izlenen metabolik hastalıklar", "give a clue about", "beslenme yetersizliği", q, hedge="ipucu sağlamaktadır")
S("INTERP", "çocuklarda izlenen metabolik hastalıklar", "give a clue about", "anne sütü bakımından eksiklik", q, hedge="ipucu sağlamaktadır")
S("INTERP", "çocuklarda izlenen metabolik hastalıklar", "give a clue about", "hijyen koşulları", "hijyen koşulları hakkında ipucu sağlamaktadır", hedge="ipucu sağlamaktadır")
S("DESCR", "antropoloji sonuçları", "is judged to inform on", "popülasyonun sosyo-kültürel durumu, beslenme pratikleri ve yaşam tarzları",
  "beslenme pratikleri ve yaşam tarzları hakkında bilgi sağlamıştır")
S("STRUCT", "başlık", "heading reads", "SONUÇ", "SONUÇ")
S("DESCR", KAZI, "is judged", "bölgenin Roma Dönemi’ne ait mimari yapısı ve gömü pratikleriyle ilgili dikkate değer veriler sunmuştur",
  "mimari yapısı ve gömü pratikleriyle ilgili dikkate değer veriler sunmuştur")
S("DESCR", "kazı çalışmaları", "is judged", "titizlikle yürütülmüştür", "ışığında titizlikle yürütülmüştür")
S("ADMIN", "E-15 ve E-16 plankarelerindeki çalışmalar", "was part of project", "Geleceğe Miras Projesi",
  "Geleceğe Miras Projesi kapsamındaki çalışmalar E-15 ve E-16, J-17, J-18, J-K/18, K-16, K-17, K-18, K-L/15-16, L-17 ve L-18 plankarelerinde")
q = "7 adet Hipoje, 10 adet Çatkı Mezar, 1 adet Taş Sanduka Mezar ve 2 adet Tuğla Plaka Mezar ortaya çıkarılmıştır"
L("BUILT", "Hipoje (2024 kazıları)", "count", "7 adet", q)
L("BUILT", "Çatkı Mezar (2024 kazıları)", "count", "10 adet", q)
L("BUILT", "Taş Sanduka Mezar (2024 kazıları)", "count", "1 adet", q)
L("BUILT", "Tuğla Plaka Mezar (2024 kazıları)", "count", "2 adet", q)
S("FIND", "envanterlik eser", "count", "7 tanesi", "Ele geçen buluntulardan 7 tanesi envanterlik eser")
S("FIND", "etütlük eser", "count", "6 tanesi", "6 tanesi ise etütlük eser olarak ayrılmıştır")
S("INTERP", "Nekropol alanı", "is interpreted as",
  "yalnızca bir mezarlık değil, aynı zamanda sosyal ve dini bağlamlarla bütünleşmiş bir yapıya sahip",
  "Nekropol alanının yalnızca bir mezarlık değil, aynı zamanda")
q = "nekropolde mozaik taban döşemeleri, duvar kalıntıları ve farklı gömü türlerini temsil eden mezar yapıları gibi pek çok önemli bulguya da ulaşılmıştır"
q1 = "nekropolde mozaik taban döşemeleri, duvar kalıntıları ve farklı gömü türlerini temsil"
for v in ["mozaik taban döşemeleri", "duvar kalıntıları", "farklı gömü türlerini temsil eden mezar yapıları"]:
    L("BUILT", "nekropol", "yielded", v, q1 if v != "farklı gömü türlerini temsil eden mezar yapıları" else "eden mezar yapıları gibi pek çok önemli bulguya da ulaşılmıştır")
S("INTERP", "Bazilika ile Nekropol alanındaki mezarlar arasındaki mekânsal ilişki", "is noticeable especially in", "Hipoje mezarlar",
  "Hipoje mezarlarda dikkati çekmektedir")
S("FIND", "mezar hediyeleri (Hipojeler)", "was found in", "Hipojeler (iskelet kalıntıları ile beraber)",
  "iskelet kalıntıları ve beraberlerinde çeşitli mezar hediyeleri ele geçirilmiştir")
S("FIND", "mezar hediyeleri (Hipojeler)", "kind", "çeşitli mezar hediyeleri",
  "iskelet kalıntıları ve beraberlerinde çeşitli mezar hediyeleri ele geçirilmiştir")
S("INTERP", "Hipoje mezarlar", "is interpreted as", "yalnızca bireysel definler için değil, aile ya da topluluk mezarları olarak kullanıldı",
  "mezarların yalnızca bireysel definler için değil, aile ya da topluluk mezarları olarak")
S("INTERP", "bölge (Nekropol alanı)", "use in Roma Dönemi", "gömü alanı", "bölgenin Roma Dönemi’nde gömü alanı olarak kullanılırken")
S("INTERP", "bölge (Nekropol alanı)", "in Erken Bizans Dönemi had", "dini yapılarla bütünleşmiş bir düzenleme",
  "Erken Bizans Dönemi’nde dini yapılarla bütünleşmiş bir")

# ---------------------------------------------------------------- page 124
pg(124)
S("INTERP", "Bazilika", "is interpreted as", "Mezarlık Kilisesi (ölülerle yaşayanlar arasında manevi bir köprü görevi gören)",
  "gören Mezarlık Kilisesi olabileceğini göstermektedir", hedge="olabileceğini göstermektedir")
S("INTERP", "Bazilika", "is interpreted as", "ibadet mekânı", "Bazilika’nın yalnızca bir ibadet mekânı değil")
S("DESCR", "Hisardere Nekropolü Kazıları", "is judged",
  "Roma Dönemi Nekropol alanlarının mekânsal düzeni, dini ve toplumsal bağlamları açısından dönemin dinamik yapısını gözler önüne sermektedir",
  "açısından dönemin dinamik yapısını gözler önüne sermektedir")
S("DESCR", "çalışmalar sırasında elde edilen bulgular", "is judged", "Roma Dönemi ölü gömme ritüelleri ve mimari planlama konusunda yeni sorular ortaya çıkarır",
  "gömme ritüelleri ve mimari planlama konusunda yeni sorular ortaya çıkarırken")
S("DESCR", "alan", "is judged to need", "korunması ve daha ileri teknolojiyle incelenmesi",
  "korunması ve daha ileri teknolojiyle incelenmesi gerekliliğini de vurgulamaktadır")

# ---------------------------------------------------------------- captions
pg(125)
S("STRUCT", "başlık", "heading reads", "EKLER", "EKLER")
S("FIGURE", "Çizim 1", "caption reads", "İznik Hisardere Nekropolü Kazı Alanı.", "Çizim 1: İznik Hisardere Nekropolü Kazı Alanı.")
S("FIGURE", "Çizim 2", "caption reads", "Kesit üzerinde mezarlar arasındaki ilişki.", "Çizim 2: Kesit üzerinde mezarlar arasındaki ilişki.")
pg(126)
S("FIGURE", "Çizim 3", "caption reads", "2024 yılı seramik buluntu örnekleri.", "Çizim 3: 2024 yılı seramik buluntu örnekleri.")
caps = [(127, "Resim 1", "Terrakota Plaka Kapaklı Mezar-1."),
        (127, "Resim 2", "E-15 Plankaresi’nde ortaya çıkarılan mezarlar."),
        (128, "Resim 3", "K-16 Plankaresi’nde ortaya çıkarılan Çatkı Mezar-1."),
        (128, "Resim 4", "K-16 Plankaresi’nde ortaya çıkarılan Hipoje-2."),
        (129, "Resim 5", "K-16 Plankaresi’nde ortaya çıkarılan Hipoje-1."),
        (129, "Resim 6", "J-17 Plankaresi Tuğla Zemin Döşemesi."),
        (130, "Resim 7", "Nekropol alanına yapılan Geçici Koruma Çatısı."),
        (130, "Resim 8", "Konservasyonu yapılan altın küpeler."),
        (131, "Resim 9", "K16 Plankaresi Hipoje-2 içinden çıkarılan pişmiş toprak testi."),
        (131, "Resim 10", "Kemikler üzerinde gözlemlenen hastalıklar.")]
for p_, s_, c_ in caps:
    pg(p_)
    L("FIGURE", s_, "caption reads", c_, s_ + ": " + c_)

for i, r in enumerate(rows):
    r["n"] = i + 1
json.dump(rows, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ check
data = json.load(open(OUT, encoding="utf-8"))
txt = open(BASE + "paper.txt", encoding="utf-8").read()
pages = txt.split("\f")


def norm(s):
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s).strip()


pn = {115 + i: norm(p) for i, p in enumerate(pages)}
full = norm(txt)
KEYS = ["n", "page", "group", "form", "subject", "says", "value", "hedge", "negative", "who", "quote"]
bad = 0
for r in data:
    if sorted(r.keys()) != sorted(KEYS):
        print("KEYS", r["n"]); bad += 1
    if r["group"] not in GROUPS:
        print("GROUP", r["n"]); bad += 1
    if r["form"] not in ("list", "prose"):
        print("FORM", r["n"]); bad += 1
    qn = norm(r["quote"])
    if len(r["quote"]) > 200:
        print("LONG", r["n"], len(r["quote"])); bad += 1
    if qn not in pn.get(r["page"], ""):
        where = [k for k, v in pn.items() if qn in v]
        print("QUOTE", r["n"], r["page"], where, repr(r["quote"])); bad += 1
    if "@" in json.dumps(r, ensure_ascii=False):
        print("EMAIL", r["n"]); bad += 1
print("pages in file:", len(pages), "bad:", bad, "total:", len(data))
c = collections.Counter
print("group", dict(c(r["group"] for r in data)))
print("form", dict(c(r["form"] for r in data)))
print("page", dict(sorted(c(r["page"] for r in data).items())))
print("hedged", sum(1 for r in data if r["hedge"]), "negative", sum(1 for r in data if r["negative"]))
print("unclear", [(r["n"], r["page"], r["subject"]) for r in data if "[unclear]" in r["value"]])
