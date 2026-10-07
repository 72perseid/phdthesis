# -*- coding: utf-8 -*-
import json, re, collections

BASE = "/media/tugce/ProgramsVS/tez/v2/blind/test3/"
rows = []


def S(p, g, f, subj, says, val, q, h="", neg=False, who=""):
    rows.append(dict(page=p, group=g, form=f, subject=subj, says=says, value=val,
                     hedge=h, negative=neg, who=who, quote=q))


L, P = "list", "prose"
K = "İznik Hisardere Nekropolü 2024 yılı kazı çalışmaları"

# ---------------------------------------------------------------- page 115
p = 115
S(p, "STRUCT", P, "sayfa üst başlığı", "page header reads", "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1",
  "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1")
S(p, "DOC", P, "bildiri", "has title", "İZNİK HİSARDERE NEKROPOLÜ 2024 YILI KAZI ÇALIŞMALARI",
  "İZNİK HİSARDERE NEKROPOLÜ 2024 YILI KAZI ÇALIŞMALARI")
for a in ["Aygün EKİN MERİÇ", "Ali Kazım ÖZ", "Tolga KOPARAL", "Gülşen KUTBAY", "Ruken Zeynep KÖSE"]:
    S(p, "DOC", L, "bildiri", "has author", a, a)
q = "Kültür ve Turizm Bakanlığının izni ve maddi desteği ile"
S(p, "ADMIN", P, K, "was permitted by", "Kültür ve Turizm Bakanlığı", q)
S(p, "ADMIN", P, K, "was financially supported by", "Kültür ve Turizm Bakanlığı", q)
S(p, "PEOPLE", P, "İznik Müzesi Müdürlüğü", "role in the work", "başkanlık", "İznik Müzesi Müdürlüğü başkanlığında")
q = "Dokuz Eylül Üniversitesinden Prof. Dr. Aygün Ekin Meriç’in Bilimsel Koordinatörlüğünde"
S(p, "PEOPLE", P, "Aygün Ekin Meriç", "role in the work", "Bilimsel Koordinatör", q)
S(p, "PEOPLE", P, "Aygün Ekin Meriç", "has title", "Prof. Dr.", q)
S(p, "PEOPLE", P, "Aygün Ekin Meriç", "is affiliated with", "Dokuz Eylül Üniversitesi", q)
S(p, "WORK", P, K, "was carried out by", "oluşturulan bir ekip", "oluşturulan bir ekip tarafından gerçekleştirilmiştir")
q = "aralıklı olarak 01.08.2024-27.12.2024 tarihleri arasında"
S(p, "WORK", P, K, "took place between", "01.08.2024-27.12.2024", q)
S(p, "WORK", P, K, "continuity", "aralıklı olarak", q)
S(p, "PEOPLE", L, "arkeolog", "count in team", "bir", "bir arkeolog, bir antropolog, dört işçi ve sekiz gönüllü öğrenci")
S(p, "PEOPLE", L, "antropolog", "count in team", "bir", "bir antropolog")
S(p, "ADMIN", L, "işçi", "count in team", "dört", "dört işçi")
S(p, "PEOPLE", L, "gönüllü öğrenci", "count in team", "sekiz", "sekiz gönüllü öğrenci")
S(p, "WORK", P, "çalışmalar", "number of work areas", "beş alan", "olmak üzere beş alanda gerçekleşmiştir")
for a, q in [("Kazı Çalışmaları", "Çalışmalar; Kazı Çalışmaları"),
             ("Seramik ve Küçük Buluntu Değerlendirme", "Seramik ve Küçük Buluntu Değerlendirme"),
             ("Antropoloji Çalışmaları", "Antropoloji Çalışmaları"),
             ("Mimari Belgeleme ve Çizim", "Mimari Belgeleme ve Çizim"),
             ("Restorasyon ve Konservasyon", "Restorasyon ve Konservasyon olmak üzere")]:
    S(p, "WORK", L, "çalışmalar", "has work area", a, q)
S(p, "STRUCT", P, "başlık", "heading reads", "KAZI ÇALIŞMALARI", "KAZI ÇALIŞMALARI")
q = "2020 yılı temmuz ayında gerçekleştirilen yeraltı görüntüleme sistemi yardımıyla taranan alanın jeoradar verileri"
S(p, "WORK", P, "alanın taranması", "took place in", "2020 yılı temmuz ayı", q)
S(p, "WORK", P, "alanın taranması", "was done with tool", "yeraltı görüntüleme sistemi", q)
S(p, "WORK", P, "alanın taranması", "produced", "jeoradar verileri", q)
S(p, "WORK", P, "çalışma planı", "was based on", "jeoradar verileri", "jeoradar verileri esas alınarak çalışma planı belirlenmiştir")
q = "Jeoradar tarama verileriyle birlikte, önceki yıllarda gerçekleştirilen kazı çalışmaları bir arada değerlendirilerek, öncelikli kazılacak alanlar belirlenmiştir"
S(p, "WORK", P, "öncelikli kazılacak alanlar", "were determined from", "jeoradar tarama verileri", q)
S(p, "WORK", P, "öncelikli kazılacak alanlar", "were determined from", "önceki yıllarda gerçekleştirilen kazı çalışmaları", q)
W1 = "01.08.2024-30.08.2024 tarihli çalışmalar"
S(p, "WORK", P, W1, "took place between", "01.08.2024-30.08.2024", "01.08.2024-30.08.2024 tarihleri arasında")
S(p, "ADMIN", P, W1, "was funded by", "Kültür ve Turizm Bakanlığından sağlanan ödenek",
  "Kültür ve Turizm Bakanlığından sağlanan ödenek ile gerçekleştirilen çalışmalar")
S(p, "WORK", P, W1, "took place in square", "E-15", "E-15 ve E-16 plankarelerinde gerçekleştirilmiştir")
S(p, "WORK", P, W1, "took place in square", "E-16", "E-15 ve E-16 plankarelerinde gerçekleştirilmiştir")
W2 = "03.10.2024-29.11.2024 tarihli çalışmalar"
S(p, "WORK", P, W2, "took place between", "03.10.2024-29.11.2024", "03.10.2024-29.11.2024 tarihleri arasında")
S(p, "ADMIN", P, W2, "was part of project", "Geleceğe Miras Projesi", "Geleceğe Miras Projesi kapsamında")
S(p, "ADMIN", P, W2, "was funded by", "Kültür ve Turizm Bakanlığından sağlanan ödenek yardımı",
  "Kültür ve Turizm Bakanlığından sağlanan ödenek yardımı ile")
q = "J-17, J-18, J-K/18, K-16, K-17, K-18, K-L/15-16, L-17 ve L-18 plankarelerinde"
for a in ["J-17", "J-18", "J-K/18", "K-16", "K-17", "K-18", "K-L/15-16", "L-17", "L-18"]:
    S(p, "WORK", L, W2, "took place in square", a, q)
S(p, "FIGURE", P, W2 + " (plankareler)", "is shown in figure", "Çizim: 1", "gerçekleştirilmiştir (Çizim: 1)")
# footnote
q = "Prof. Dr. Aygün EKİN MERIÇ; Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü"
S(p, "PEOPLE", L, "Aygün EKİN MERIÇ", "unit of affiliation", "Edebiyat Fakültesi, Arkeoloji Bölümü", q)
S(p, "PEOPLE", L, "Aygün EKİN MERIÇ", "has address", "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE",
  "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE")
S(p, "PEOPLE", L, "Aygün EKİN MERIÇ", "has identifier (ORCID)", "0000-0002-1343-847X", "ORCID: 0000-0002-1343-847X")
q = "Prof. Dr. Ali Kazım ÖZ; Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü, Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE"
S(p, "PEOPLE", L, "Ali Kazım ÖZ", "has title", "Prof. Dr.", q)
S(p, "PEOPLE", L, "Ali Kazım ÖZ", "is affiliated with", "Dokuz Eylül Üniversitesi, Edebiyat Fakültesi, Arkeoloji Bölümü", q)
S(p, "PEOPLE", L, "Ali Kazım ÖZ", "has address", "Tınaztepe Kampüsü, 35390 Buca, İzmir, TÜRKIYE", q)
S(p, "PEOPLE", L, "Ali Kazım ÖZ", "has identifier (ORCID)", "0000-0002-3005-323X", "ORCID: 0000-0002-3005-323X")
q = "Arkeolog Tolga KOPARAL; İznik Müzesi Müdürlüğü, 16860 İznik, Bursa, TÜRKIYE"
S(p, "PEOPLE", L, "Tolga KOPARAL", "has title", "Arkeolog", q)
S(p, "PEOPLE", L, "Tolga KOPARAL", "is affiliated with", "İznik Müzesi Müdürlüğü", q)
S(p, "PEOPLE", L, "Tolga KOPARAL", "has address", "16860 İznik, Bursa, TÜRKIYE", q)
q = "Arkeolog Dr. Gülşen KUTBAY; Hisardere Nekropolü Kazıevi, 16860 İznik, Bursa, TÜRKIYE"
S(p, "PEOPLE", L, "Gülşen KUTBAY", "has title", "Arkeolog Dr.", q)
S(p, "PEOPLE", L, "Gülşen KUTBAY", "is affiliated with", "Hisardere Nekropolü Kazıevi", q)
S(p, "PEOPLE", L, "Gülşen KUTBAY", "has address", "16860 İznik, Bursa, TÜRKIYE", q)
q = "Antropolog Ruken Zeynep KÖSE; Hisardere Nekropolü Kazıevi, 16860 İznik, Bursa, TÜRKIYE"
S(p, "PEOPLE", L, "Ruken Zeynep KÖSE", "has title", "Antropolog", q)
S(p, "PEOPLE", L, "Ruken Zeynep KÖSE", "is affiliated with", "Hisardere Nekropolü Kazıevi", q)
S(p, "PEOPLE", L, "Ruken Zeynep KÖSE", "has address", "16860 İznik, Bursa, TÜRKIYE", q)

# ---------------------------------------------------------------- page 116
p = 116
S(p, "STRUCT", P, "sayfa üst başlığı", "page header reads", "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ",
  "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ")
S(p, "STRUCT", P, "başlık", "heading reads", "E-15 Plankaresi", "E-15 Plankaresi")
q = "Alanda gerçekleştirilen jeoradar taramaları sonucunda"
S(p, "WORK", P, "E-15 plankaresi kazı çalışmaları", "was planned as a result of", "jeoradar taramaları", q)
q = "bazilikanın batı sınırını ortaya çıkarmak amacıyla E-15 plankaresinde kazı çalışmalarının yürütülmesi planlanmıştır"
S(p, "WORK", P, "E-15 plankaresi kazı çalışmaları", "has purpose", "bazilikanın batı sınırını ortaya çıkarmak", q)
S(p, "BUILT", P, "bazilika", "is built over", "Nekropol alanı", "Nekropol alanı üzerine inşa edilmiş bazilikanın")
S(p, "MEASURE", P, "E-15 açması", "measures", "600x600 cm", "600x600 cm ölçülerinde açma sınırları belirlenmiş")
S(p, "PLACE", P, "E-15 açması", "work started at elevation", "+96,82 m", "çalışmalar +96,82 m kotunda başlatılmıştır")
q = "Alanın kuzey kesitinde, sert, kuru ve sıkışmış bir yapıya sahip toprak tabakasında"
S(p, "BUILT", P, "toprak tabakası (E-15)", "is located in", "alanın kuzey kesiti", q)
S(p, "BUILT", P, "toprak tabakası (E-15)", "has character", "sert, kuru ve sıkışmış", q)
q2 = "tessera ve mozaik parçalarının öbekler halinde bulunduğu tespit edilmiştir"
for a in ["tessera", "mozaik parçaları"]:
    S(p, "FIND", P, a + " (E-15)", "is of kind", a, q2)
    S(p, "FIND", P, a + " (E-15)", "was found in", "alanın kuzey kesiti, toprak tabakası", q)
    S(p, "FIND", P, a + " (E-15)", "position in place of finding", "öbekler halinde", q2)
S(p, "WORK", P, "tesseralar (E-15)", "was examined", "alanla organik bir bağının olup olmadığı",
  "ele geçirilen tesseraların alanla organik bir bağının olup olmadığı titizlikle incelenmiştir")
q = "96,44 m kotunda tahrip olmuş bir statumen tabakası ve mozaik harcı gözlemlenmiştir"
S(p, "BUILT", P, "statumen tabakası (E-15)", "is of kind", "statumen tabakası", q)
S(p, "BUILT", P, "statumen tabakası (E-15)", "elevation", "96,44 m", q)
S(p, "BUILT", P, "statumen tabakası (E-15)", "condition", "tahrip olmuş", q)
S(p, "BUILT", P, "mozaik harcı (E-15)", "is of kind", "mozaik harcı", q)
S(p, "BUILT", P, "mozaik harcı (E-15)", "elevation", "96,44 m", q)
S(p, "INTERP", P, "alan (E-15)", "is interpreted as", "mozaik taban döşemesiyle kaplı",
  "Söz konusu bulgular, alanın mozaik taban döşemesiyle kaplı olduğuna işaret ettiğinden", h="işaret ettiğinden")
q = "bu önemli kalıntıların korunmasına karar verilmiştir"
S(p, "DESCR", P, "kalıntılar (statumen tabakası ve mozaik harcı)", "is judged as", "önemli", q)
S(p, "WORK", P, "kalıntılar (statumen tabakası ve mozaik harcı)", "decision", "korunmasına karar verilmiştir", q)
q = "+96,33 m kotunda, 67x120 cm ölçülerinde iki sıra taş örgülü bir duvar yapısı tespit edilmiştir"
D = "duvar yapısı (E-15)"
S(p, "WORK", P, D, "was found while", "kazı çalışmaları kuzey yönünde ilerletildiği esnada",
  "Kazı çalışmaları kuzey yönünde ilerletildiği esnada")
S(p, "BUILT", P, D, "is of kind", "iki sıra taş örgülü duvar yapısı", q)
S(p, "BUILT", P, D, "elevation", "+96,33 m", q)
S(p, "MEASURE", P, D, "measures", "67x120 cm", q)
S(p, "BUILT", P, D, "orientation", "doğu-batı doğrultulu", "doğu-batı doğrultulu duvarın güneyinde")
q = "içinde harç kalıntıları bulunan ve dibe yakın bölümü korunmuş bir pithos kalıntısı ortaya çıkarılmıştır"
S(p, "FIND", P, "pithos (E-15)", "is of kind", "pithos kalıntısı", q)
S(p, "FIND", P, "pithos (E-15)", "was found in", "doğu-batı doğrultulu duvarın güneyinde yer alan bir alan",
  "doğu-batı doğrultulu duvarın güneyinde yer alan bir alanda")
S(p, "FIND", P, "pithos (E-15)", "condition", "dibe yakın bölümü korunmuş", q)
S(p, "FIND", P, "pithos (E-15)", "contains", "harç kalıntıları", q)
S(p, "DESCR", P, "pithosun harç kalıntıları", "could inform about", "yapının kullanım amacı ve dönemin gömü pratikleri",
  "yapının kullanım amacı ve dönemin gömü pratiklerine ilişkin bilgiler sağlama potansiyeline sahiptir",
  h="potansiyeline sahiptir")
G = "ÇM 1 (E-15)"
q = "açmanın kuzey kesitinden 40 cm içeride, +96,00 m. kotunda doğu-batı doğrultusunda uzanan"
q2 = "uzunluğu 182 cm, genişliği ise 50 cm olan bir Çatkı Mezar (ÇM 1) tespit edilmiştir"
S(p, "BUILT", P, G, "is of kind", "Çatkı Mezar", q2)
S(p, "BUILT", P, G, "is located at", "açmanın kuzey kesitinden 40 cm içeride", q)
S(p, "BUILT", P, G, "elevation", "+96,00 m.", q)
S(p, "BUILT", P, G, "orientation", "doğu-batı doğrultusunda", q)
S(p, "MEASURE", P, G, "measures (length)", "182 cm", q2)
S(p, "MEASURE", P, G, "measures (width)", "50 cm", q2)
S(p, "BUILT", P, G, "extends under", "doğu kesit (mezarın bir kısmı)", "mezarın bir kısmının doğu kesitin altına doğru uzandığı")
S(p, "BUILT", P, G, "covers are supported with", "harç ve taşlar", "mezar kapaklarının harç ve taşlarla desteklendiği belirlenmiştir")
S(p, "WORK", P, G, "was documented", "belgeleme işlemleri tamamlandı", "Mezarın belgeleme işlemlerinin tamamlanmasının ardından")
S(p, "WORK", P, G, "was opened by", "batı yönündeki iki kapağın açılması", "batı yönündeki iki kapağın açılmasıyla")
q = "mezar içinde neredeyse tamamen yok olmuş olan iskelete ait kemik döküntüleri toplanarak kayıt altına alınmıştır"
S(p, "FIND", P, "kemik döküntüleri (ÇM 1, E-15)", "is of kind", "iskelete ait kemik döküntüleri", q)
S(p, "FIND", P, "kemik döküntüleri (ÇM 1, E-15)", "was found in", "ÇM 1 mezar içi", q)
S(p, "FIND", P, "kemik döküntüleri (ÇM 1, E-15)", "condition", "neredeyse tamamen yok olmuş", q)
S(p, "WORK", P, "kemik döküntüleri (ÇM 1, E-15)", "was treated", "toplanarak kayıt altına alınmıştır", q)
G = "TPM 1 (E-15)"
q = "+95,98 m kotunda terrakota plaka kapaklı bir mezar yapısına (TPM 1) ait kapaklara ve mezarın duvarına ait tuğla sırasına ulaşılmıştır"
S(p, "WORK", P, G, "was found during", "güney yönünde sürdürülen kazı çalışmaları", "Güney yönünde sürdürülen kazı çalışmaları sırasında")
S(p, "BUILT", P, G, "is of kind", "terrakota plaka kapaklı mezar yapısı", q)
S(p, "BUILT", P, G, "elevation", "+95,98 m", q)
q = "Doğu-batı doğrultusunda uzanan mezarın boyutları 71x213 cm olarak ölçülmüştür"
S(p, "BUILT", P, G, "orientation", "Doğu-batı doğrultusunda", q)
S(p, "MEASURE", P, G, "measures", "71x213 cm", q)
q = "her biri 8 cm kalınlığında ve 71x71 cm boyutlarında üç adet pişmiş toprak plaka ile örtülmüş"
S(p, "BUILT", P, G, "is covered with", "pişmiş toprak plaka", q)
S(p, "BUILT", P, G + " plakaları", "count", "üç adet", q)
S(p, "MEASURE", P, G + " plakaları", "measures (thickness)", "8 cm", q)
S(p, "MEASURE", P, G + " plakaları", "measures", "71x71 cm", q)
q = "çevresi ise 32 cm uzunluğundaki tuğlalardan oluşan bir sıra ile çevrelenmiştir"
S(p, "BUILT", P, G, "is surrounded by", "tuğlalardan oluşan bir sıra", q)
S(p, "MEASURE", P, G + " tuğlaları", "measures (length)", "32 cm", q)
S(p, "MEASURE", P, G + " tuğla sırası", "measures (measurable total length)", "238 cm",
  "Tuğla sırasının ölçülebilen toplam uzunluğu 238 cm olarak kaydedilmiştir")
q = "açılmaya uygun olan üç kapağından, doğu yönündeki iki kapak kaldırılarak mezar içi çalışmalara başlanmıştır"
S(p, "BUILT", P, G, "covers fit for opening", "üç kapak", q)
S(p, "WORK", P, G, "was opened by", "doğu yönündeki iki kapak kaldırılarak", q)
q = "uzunluğu 185 cm ve genişliği ise 38 cm olan mezar içerisinde bir bireye ait iskelet kalıntısı tespit edilmiş"
S(p, "MEASURE", P, G + " mezar içi", "measures (length)", "185 cm", q)
S(p, "MEASURE", P, G + " mezar içi", "measures (width)", "38 cm", q)
S(p, "FIND", P, "iskelet kalıntısı (TPM 1)", "is of kind", "iskelet kalıntısı", q)
S(p, "FIND", P, "iskelet kalıntısı (TPM 1)", "was found in", "TPM 1 mezar içi", q)
S(p, "FIND", P, "iskelet kalıntısı (TPM 1)", "count of individuals", "bir birey", q)
S(p, "WORK", P, G, "was treated", "mezarın içi temizlenerek çalışmalar sonlandırılmıştır", "mezarın içi temizlenerek çalışmalar sonlandırılmıştır")
S(p, "BUILT", P, G + " iç duvarları", "is coated with", "tuğla tozu içeren pembemsi bir sıva",
  "Mezar iç duvarlarının, tuğla tozu içeren pembemsi bir sıva ile kaplı olduğu")
S(p, "BUILT", P, G + " zemini", "is paved with", "düzensiz biçimde alana uydurulmuş tuğlalar",
  "zeminin ise düzensiz biçimde alana uydurulmuş tuğlalarla döşendiği belirlenmiştir")
S(p, "FIGURE", P, G, "is shown in figure", "Resim: 1", "tuğlalarla döşendiği belirlenmiştir (Resim: 1)")
q = "Mezar içerisindeki antropolojik inceleme sırasında, iskeletin muhtemelen bir kadına ait olabileceği yönünde ilk bulgular elde edilmiştir"
S(p, "WORK", P, "iskelet kalıntısı (TPM 1)", "was examined by method", "mezar içerisindeki antropolojik inceleme", q)
S(p, "INTERP", P, "iskelet kalıntısı (TPM 1)", "sex is interpreted as", "kadın", q,
  h="muhtemelen ... olabileceği yönünde ilk bulgular")
G5 = "beş adet çatkı mezar (E-15)"
S(p, "WORK", P, G5, "was found during", "doğu kesitte yürütülen kazı çalışmaları", "Doğu kesitte yürütülen kazı çalışmaları")
S(p, "BUILT", P, G5, "is located at", "Çatkı Mezar 1’in (ÇM 1) güney paraleli", "Çatkı Mezar 1’in (ÇM 1) güney paralelinde")

# ---------------------------------------------------------------- page 117
p = 117
q = "batı doğrultusunda yerleştirilmiş beş adet çatkı mezar daha açığa çıkarılmıştır"
S(p, "BUILT", P, G5, "orientation", "doğu-batı doğrultusunda", q)
S(p, "BUILT", P, G5, "count", "beş adet", q)
S(p, "BUILT", P, G5, "is of kind", "çatkı mezar", q)
S(p, "WORK", P, "E-15 mezarları", "were assessed by", "korunma durumları",
  "alanda açığa çıkarılan mezarların korunma durumlarına göre değerlendirilmesi yapılmıştır")
q = "Korunma durumları oldukça kötü olan ÇM 2, ÇM 3 ve ÇM 5’in kapalı konumda muhafaza edilmesine"
for a in ["ÇM 2", "ÇM 3", "ÇM 5"]:
    S(p, "BUILT", L, a + " (E-15)", "condition", "oldukça kötü", q)
    S(p, "WORK", L, a + " (E-15)", "decision", "kapalı konumda muhafaza edilmesi", q)
G = "ÇM 4 (E-15)"
q = "nispeten iyi durumda olan ÇM 4’ün ise açılarak incelenmesine karar verilmiştir"
S(p, "BUILT", P, G, "condition", "nispeten iyi", q)
S(p, "WORK", P, G, "decision", "açılarak incelenmesi", q)
S(p, "INTERP", P, G + " mezar kapakları", "compared with other basit formlu çatkı mezarlar",
  "daha kalın cidarlı ve özenli bir yapıya sahip",
  "mezar kapaklarının diğer basit formlu çatkı mezarlara kıyasla daha kalın cidarlı ve özenli bir yapıya sahip olduğu")
S(p, "BUILT", P, G + " mezar kapakları", "inner surfaces bear", "basit kazıma motifler",
  "kapakların iç yüzeylerinde ise basit kazıma motiflerin işlendiği tespit edilmiştir")
q = "Uzunluğu 187 cm ve genişliği ise 45 cm olan mezarın temizlik ve belgeleme çalışmaları tamamlanmış"
S(p, "MEASURE", P, G, "measures (length)", "187 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "45 cm", q)
S(p, "WORK", P, G, "was treated", "temizlik ve belgeleme çalışmaları tamamlanmış", q)
q = "iskelet laboratuvar ortamında detaylı analiz için toplanmış"
S(p, "FIND", P, "iskelet (ÇM 4, E-15)", "is of kind", "iskelet", q)
S(p, "FIND", P, "iskelet (ÇM 4, E-15)", "was found in", "ÇM 4", q)
S(p, "WORK", P, "iskelet (ÇM 4, E-15)", "was collected for", "laboratuvar ortamında detaylı analiz", q)
S(p, "WORK", P, G, "was treated", "mezar içi temizlenerek çalışmalar sonlandırılmıştır", "mezar içi temizlenerek çalışmalar sonlandırılmıştır")
q = "bazilikanın batı sınırını oluşturan duvar sırasının bir bölümü ile odaları birbirinden ayıran duvarların bazı kısımları açığa çıkarılmıştır"
S(p, "BUILT", P, "bazilikanın batı sınırını oluşturan duvar sırası", "was exposed in E-15 (extent)", "bir bölümü", q)
S(p, "BUILT", P, "odaları birbirinden ayıran duvarlar", "was exposed in E-15 (extent)", "bazı kısımları", q)
q = "beşik çatkı tipi, ikisi pişmiş toprak plaka kapaklı olmak üzere toplam yedi mezar tespit edilmiştir"
S(p, "BUILT", P, "E-15 mezarları", "count (total)", "yedi mezar", q)
S(p, "BUILT", P, "E-15 mezarları", "is of type", "beşik çatkı tipi", q)
S(p, "BUILT", P, "E-15 mezarları", "count with pişmiş toprak plaka kapak", "ikisi", q)
S(p, "FIGURE", P, "E-15 mezarları", "is shown in figure", "Resim: 2", "tespit edilmiştir (Resim: 2)")
q = "az sayıda seramik parçası, tessera ve mozaik kalıntılarının yanı sıra üç adet bronz sikke de bulunmuştur"
S(p, "FIND", P, "seramik parçası (E-15)", "is of kind", "seramik parçası", q)
S(p, "FIND", P, "seramik parçası (E-15)", "was found in", "E-15 plankaresi", q)
S(p, "FIND", P, "seramik parçası (E-15)", "count", "az sayıda", q)
S(p, "FIND", P, "sikke (E-15)", "is of kind", "sikke", q)
S(p, "FIND", P, "sikke (E-15)", "was found in", "E-15 plankaresi", q)
S(p, "FIND", P, "sikke (E-15)", "count", "üç adet", q)
S(p, "FIND", P, "sikke (E-15)", "is made of", "bronz", q)
S(p, "DESCR", P, "E-15 buluntuları", "is judged as", "önemli veriler sunmaktadır",
  "alanın mimari düzenini, kullanım amacını ve tarihi bağlamını anlamak açısından önemli veriler sunmaktadır")
S(p, "STRUCT", P, "başlık", "heading reads", "E-16 Plankaresi", "E-16 Plankaresi")
q = "E-16 plankaresinde 3,50x5,00 m ölçülerinde belirlenen açma sınırlarında, +96,82 m kotunda kazı çalışmalarına başlanmıştır"
S(p, "MEASURE", P, "E-16 açması", "measures", "3,50x5,00 m", q)
S(p, "PLACE", P, "E-16 açması", "work started at elevation", "+96,82 m", q)
q = "+96,15 m kotunda doğu-batı doğrultulu, basit formlu iki çatkı mezar (ÇM 1 ve ÇM 2) açığa çıkarılmıştır"
S(p, "BUILT", P, "çatkı mezarlar (E-16)", "count", "iki", q)
for a in ["ÇM 1 (E-16)", "ÇM 2 (E-16)"]:
    S(p, "BUILT", P, a, "is of kind", "basit formlu çatkı mezar", q)
    S(p, "BUILT", P, a, "elevation", "+96,15 m", q)
    S(p, "BUILT", P, a, "orientation", "doğu-batı doğrultulu", q)
G = "ÇM 1 (E-16)"
S(p, "BUILT", P, G + " mezar kapakları", "bear", "düzensiz kazıma motifler",
  "ÇM 1’in mezar kapakları üzerinde düzensiz kazıma motiflerin bulunduğu gözlemlenmiştir")
q = "Mezarın korunma durumunun kötü olması ve kapaklardaki çökme sonucu içeriye fazlaca toprak dolmuş olması nedeniyle"
S(p, "BUILT", P, G, "condition", "korunma durumu kötü", q)
S(p, "BUILT", P, G, "condition of covers", "kapaklardaki çökme", q)
S(p, "BUILT", P, G, "is filled with", "fazlaca toprak", q)
S(p, "FIND", P, "iskelet kalıntısı (ÇM 1, E-16)", "was found in situ", "rastlanamamıştır",
  "in situ halde iskelet kalıntısına rastlanamamıştır", neg=True)
S(p, "STRUCT", P, "başlık", "heading reads", "K-17 Plankaresi", "K-17 Plankaresi")
q = "nekropol alanının güneyinde yer alan K-17 plankaresinde kazı çalışmalarına başlanmıştır"
S(p, "PLACE", P, "K-17 plankaresi", "is located in", "nekropol alanının güneyi", q)
S(p, "WORK", P, "K-17 plankaresi", "excavation was started", "kazı çalışmalarına başlanmıştır", q)
G = "bazilikanın Narteks bölümüne ait güney duvarının devamı (K-17)"
q = "bazilikanın Narteks bölümüne ait güney duvarının devamına +97,63 m seviyesinde ulaşılmıştır"
S(p, "BUILT", P, G, "belongs to", "bazilikanın Narteks bölümü", q)
S(p, "BUILT", P, G, "elevation", "+97,63 m", q)
q = "doğrultulu olan bu duvarın genişliği 1,46 m, buna dik duvarlar ise 72 cm olarak ölçülmüştür"
S(p, "BUILT", P, G, "orientation", "Doğu-batı doğrultulu", q)
S(p, "MEASURE", P, G, "measures (width)", "1,46 m", q)
S(p, "BUILT", P, "dik duvarlar (K-17)", "position relative to güney duvarı", "buna dik", q)
S(p, "MEASURE", P, "dik duvarlar (K-17)", "unclear: measures (dimension not named)", "72 cm", q)
G = "Sanduka (K-17)"
q = "doğu-batı doğrultulu duvara paralel biçimde yerleştirilmiş, Sanduka tipinde bir mezara +97,22 m seviyesinde rastlanmıştır"
S(p, "BUILT", P, G, "is of kind", "Sanduka tipinde mezar", q)
S(p, "BUILT", P, G, "is located at", "doğu-batı doğrultulu duvara paralel", q)
S(p, "BUILT", P, G, "elevation", "+97,22 m", q)
q = "Modern atıklarla tamamen dolmuş olan mezar, kaçak kazıcılar tarafından talan edilmiştir"
S(p, "BUILT", P, G, "is filled with", "modern atıklar (tamamen)", q)
S(p, "BUILT", P, G, "was looted by", "kaçak kazıcılar", q)
q = "Mezar içinden herhangi bir iskelet kalıntısına ya da buluntu niteliği taşıyan bir materyale rastlanmamıştır"
S(p, "FIND", P, "iskelet kalıntısı (Sanduka, K-17)", "was found in", "rastlanmamıştır", q, neg=True)
S(p, "FIND", P, "buluntu niteliği taşıyan materyal (Sanduka, K-17)", "was found in", "rastlanmamıştır", q, neg=True)
q = "220 cm, genişliği 88 cm ve derinliği 40 cm olan Sanduka, oldukça düzgün yontulmuş dört adet monolit taştan oluşmaktadır"
S(p, "MEASURE", P, G, "measures (length)", "220 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "88 cm", q)
S(p, "MEASURE", P, G, "measures (depth)", "40 cm", q)
S(p, "BUILT", P, G, "consists of", "dört adet monolit taş", q)
S(p, "BUILT", P, G + " taşları", "workmanship", "oldukça düzgün yontulmuş", q)

# ---------------------------------------------------------------- page 118
p = 118
S(p, "STRUCT", P, "başlık", "heading reads", "K-16 Plankaresi", "K-16 Plankaresi")
G = "Hipoje 1 (K-16)"
q = "K-16 plankaresinde +97,10 m kotunda, doğu-batı doğrultusunda yönelmiş bir yeraltı mezar odası olan Hipoje 1’in tonozlu üst yapısı"
S(p, "BUILT", P, G, "is located in", "K-16 plankaresi", q)
S(p, "BUILT", P, G, "is of kind", "yeraltı mezar odası", q)
S(p, "BUILT", P, G, "elevation", "+97,10 m", q)
S(p, "BUILT", P, G, "orientation", "doğu-batı doğrultusunda", q)
S(p, "BUILT", P, G, "has part", "tonozlu üst yapı", q)
S(p, "BUILT", P, G, "entrance is given by", "terrakotta içbükey bir plaka kapak",
  "bu yapıya giriş sağlayan terrakotta içbükey bir plaka kapak tespit edilmiştir")
G = "ÇM 1 (K-16)"
q = "+96,92 m kotunda, uzunluğu 174 cm ve genişliği 52 cm olan bir çatkı mezara (ÇM 1) ulaşılmıştır (Resim: 3)"
S(p, "BUILT", P, G, "is of kind", "çatkı mezar", q)
S(p, "BUILT", P, G, "elevation", "+96,92 m", q)
S(p, "MEASURE", P, G, "measures (length)", "174 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "52 cm", q)
S(p, "FIGURE", P, G, "is shown in figure", "Resim: 3", q)
q = "dört parçadan oluşan pişmiş toprak plakaların üzerinde yer alan bir bireye ait iskelet kalıntılarına rastlanmıştır"
S(p, "FIND", P, "iskelet kalıntıları (ÇM 1, K-16)", "is of kind", "iskelet kalıntıları", q)
S(p, "FIND", P, "iskelet kalıntıları (ÇM 1, K-16)", "was found in", "ÇM 1 (K-16)", q)
S(p, "FIND", P, "iskelet kalıntıları (ÇM 1, K-16)", "position in place of finding", "pişmiş toprak plakaların üzerinde", q)
S(p, "FIND", P, "iskelet kalıntıları (ÇM 1, K-16)", "count of individuals", "bir birey", q)
S(p, "BUILT", P, G + " pişmiş toprak plakaları", "consists of", "dört parça", q)
S(p, "WORK", P, "iskelet kalıntıları (ÇM 1, K-16)", "was collected for", "laboratuvar ortamında incelenmek",
  "Mezar içi çalışmalar tamamlandıktan sonra iskelet, laboratuvar ortamında incelenmek üzere toplanmıştır")
G = "Hipoje 1 (K-16)"
S(p, "BUILT", P, G + " özgün giriş kapısı", "is located in", "doğu lunette bölümü",
  "mezarın özgün giriş kapısının doğu lunette bölümünde yer aldığı")
S(p, "BUILT", P, G + " özgün giriş kapısı", "was closed with", "tuğla duvar örgüsü (kendi döneminde)",
  "kendi döneminde tuğla duvar örgüsüyle kapatıldığı")
S(p, "BUILT", P, G + " özgün giriş kapısı", "upper part was demolished by", "kaçak kazıcılar",
  "kaçak kazıcılar tarafından yıkıldığı belirlenmiştir")
q = "İç uzunluğu 192 cm, genişliği 81 cm ve yüksekliği 156 cm olan mezarın tüm bölümlerinin beyaz renkte, incelikle uygulanmış, bezemesiz bir sıva ile kaplandığı gözlemlenmiştir"
S(p, "MEASURE", P, G, "measures (inner length)", "192 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "81 cm", q)
S(p, "MEASURE", P, G, "measures (height)", "156 cm", q)
S(p, "BUILT", P, G, "all parts are coated with", "beyaz renkte, incelikle uygulanmış sıva", q)
S(p, "BUILT", P, G + " sıvası", "has decoration", "bezemesiz", q, neg=True)
q = "mezarın tavan kısmında 7 cm çapında bir havalandırma bacasının bulunduğu tespit edilmiştir"
S(p, "BUILT", P, G, "has part", "havalandırma bacası (tavan kısmında)", q)
S(p, "MEASURE", P, G + " havalandırma bacası", "measures (diameter)", "7 cm", q)
S(p, "BUILT", P, G, "area is separated by", "sonradan tuğlayla örülmüş bir kapı", "Sonradan tuğlayla örülmüş bir kapı ile ayrılan alanda")
q = "bazilika duvarı ile mezar arasında 42 cm’lik bir boşluğun olduğu ve bu boşlukta iskelet kalıntılarının bulunduğu"
S(p, "MEASURE", P, "boşluk (bazilika duvarı ile Hipoje 1 arasında)", "measures", "42 cm", q)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 1 boşluğu, K-16)", "is of kind", "iskelet kalıntıları", q)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 1 boşluğu, K-16)", "was found in", "bazilika duvarı ile mezar arasındaki boşluk", q)
S(p, "FIGURE", P, G, "is shown in figure", "Resim: 4", "tir (Resim: 4)")
G = "Hipoje 2 (K-16)"
q = "K-16 plankaresinden önceden bulunan Hipoje 2’ye giriş, pişmiş toprak kapağın çıkarılmasıyla sağlanmıştır"
S(p, "BUILT", P, G, "is located in", "K-16 plankaresi", q)
S(p, "WORK", P, G, "unclear: was found (time not given)", "önceden", q)
S(p, "WORK", P, G, "was entered by", "pişmiş toprak kapağın çıkarılması", q)
S(p, "BUILT", P, G + " kapağı", "is made of", "pişmiş toprak", q)
S(p, "BUILT", P, G + " kapağı", "inner face bears", "kırmızımsı kahverengi tonlarda geometrik motifler",
  "Kapağın iç yüzünde, kırmızımsı kahverengi tonlarda geometrik motifler gözlemlenmiştir")
q = "İç uzunluğu 253 cm, genişliği 100 cm ve yüksekliği 173 cm olan Hipoje"
S(p, "MEASURE", P, G, "measures (inner length)", "253 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "100 cm", q)
S(p, "MEASURE", P, G, "measures (height)", "173 cm", q)
q = "oldukça özenli bir şekilde, almaşık düzende örülmüş beşik tonoz formunda inşa edilmiştir (Resim: 5)"
S(p, "DESCR", P, G, "workmanship is judged as", "oldukça özenli", q)
S(p, "BUILT", P, G, "masonry", "almaşık düzende örülmüş", q)
S(p, "BUILT", P, G, "has form", "beşik tonoz", q)
S(p, "FIGURE", P, G, "is shown in figure", "Resim: 5", q)
q = "Mezarın tabanının tuğla plakalarla döşendiği, almaşık teknikle yapılan duvarların sıvasız olduğu ve iki adet küçük nişin varlığı tespit edilmiştir"
S(p, "BUILT", P, G + " tabanı", "is paved with", "tuğla plakalar", q)
S(p, "BUILT", P, G + " duvarları", "has plaster", "sıvasız", q, neg=True)
S(p, "BUILT", P, G + " nişleri", "count", "iki adet küçük niş", q)
D = G + " kuzey duvarındaki kemerli kapı"
q = "zeminden 39 cm yukarıda, yüksekliği 76 cm ve genişliği 90 cm olan, içi tuğla ile örülmüş kemerli bir kapı tespit edilmiştir"
S(p, "BUILT", P, D, "is located in", "Hipojenin kuzey duvarı", "Hipojenin kuzey duvarında")
S(p, "BUILT", P, D, "is of kind", "içi tuğla ile örülmüş kemerli kapı", q)
S(p, "MEASURE", P, D, "height above floor", "39 cm", q)
S(p, "MEASURE", P, D, "measures (height)", "76 cm", q)
S(p, "MEASURE", P, D, "measures (width)", "90 cm", q)
S(p, "INTERP", P, D, "definite evidence of function exists", "kesin bir bulgu olmamakla birlikte",
  "Bu alanın işlevine dair kesin bir bulgu olmamakla birlikte", neg=True)
S(p, "INTERP", P, D, "is interpreted as", "diğer Hipojelerle ulaşmak amacıyla yapılmış ve işlevini yitirerek iptal edilmiş bir geçit",
  "diğer Hipojelerle ulaşmak amacıyla yapılmış ve işlevini yitirerek iptal edilmiş bir geçit olabileceği düşünülmektedir",
  h="olabileceği düşünülmektedir")
q = "mezar içerisinde in situ halde birden fazla bireye ait iskelet kalıntılarıyla birlikte, bir adet testi formunda kap tespit edilmiştir"
hh = "İlk incelemelere göre"
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 2, K-16)", "is of kind", "iskelet kalıntıları", q, h=hh)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 2, K-16)", "was found in", "Hipoje 2 mezar içi", q, h=hh)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 2, K-16)", "position in place of finding", "in situ halde", q, h=hh)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 2, K-16)", "count of individuals", "birden fazla birey", q, h=hh)
S(p, "FIND", P, "testi formunda kap (Hipoje 2, K-16)", "is of kind", "testi formunda kap", q, h=hh)
S(p, "FIND", P, "testi formunda kap (Hipoje 2, K-16)", "was found in", "Hipoje 2 mezar içi", q, h=hh)
S(p, "FIND", P, "testi formunda kap (Hipoje 2, K-16)", "count", "bir adet", q, h=hh)
q = "Dağınık halde ele geçirilen cam boncuklar ve bir çift altın küpe de mezar içindeki diğer buluntular arasındadır"
S(p, "FIND", P, "boncuklar (Hipoje 2, K-16)", "is of kind", "boncuk", q)
S(p, "FIND", P, "boncuklar (Hipoje 2, K-16)", "is made of", "cam", q)
S(p, "FIND", P, "boncuklar (Hipoje 2, K-16)", "was found in", "Hipoje 2 mezar içi", q)
S(p, "FIND", P, "boncuklar (Hipoje 2, K-16)", "position in place of finding", "dağınık halde", q)
S(p, "FIND", P, "küpe (Hipoje 2, K-16)", "is of kind", "küpe", q)
S(p, "FIND", P, "küpe (Hipoje 2, K-16)", "is made of", "altın", q)
S(p, "FIND", P, "küpe (Hipoje 2, K-16)", "count", "bir çift", q)
S(p, "FIND", P, "küpe (Hipoje 2, K-16)", "was found in", "Hipoje 2 mezar içi", q)
S(p, "WORK", P, "Hipoje 2 (K-16) iskeletleri ve buluntuları", "was stored", "ayrı kasalara yerleştirilerek muhafaza edilmiştir",
  "ayrı kasalara yerleştirilerek muhafaza edilmiştir")
S(p, "WORK", P, "Hipoje 2 (K-16) iskeletleri ve buluntuları", "was kept for", "laboratuvar ortamında detaylı incelemeler",
  "mezardan çıkarılan tüm iskeletler ve buluntular, laboratuvar ortamında detaylı")
G = "Hipoje 3 (K-16)"
S(p, "INTERP", P, G, "was at first interpreted as", "Hipojeler arası geçiş sağlayan bir koridor",
  "Başlangıçta Hipojeler arası geçiş sağlayan bir koridor olduğu düşünülen Hipoje 3’ün", h="Başlangıçta ... olduğu düşünülen")
q = "aslında bebek ve çocuklar için inşa edilmiş oldukça dar ve küçük bir Hipoje yapısı olduğu anlaşılmıştır"
S(p, "INTERP", P, G, "is interpreted as", "bebek ve çocuklar için inşa edilmiş Hipoje yapısı", q)
S(p, "BUILT", P, G, "is of kind", "oldukça dar ve küçük bir Hipoje yapısı", q)
S(p, "WORK", P, "iskelet kalıntıları (Hipoje 3, K-16)", "was examined by", "Antropolog (detaylı antropolojik incelemeler)",
  "Antropolog tarafından gerçekleştirilen detaylı antropolojik incelemeler")
q = "dört bebeğe ait iskelet kalıntıları tespit edilmiştir"
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 3, K-16)", "is of kind", "bebeğe ait iskelet kalıntıları", q)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 3, K-16)", "was found in", "Hipoje 3", q)
S(p, "FIND", P, "iskelet kalıntıları (Hipoje 3, K-16)", "count of individuals", "dört bebek", q)
q = "İç uzunluğu 258 cm, genişliği 70 cm ve yüksekliği 180 cm olan Hipoje duvarlarında herhangi bir sıva ya da bezeme bulunmamakla birlikte"
S(p, "MEASURE", P, G, "measures (inner length)", "258 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "70 cm", q)
S(p, "MEASURE", P, G, "measures (height)", "180 cm", q)
S(p, "BUILT", P, G + " duvarları", "has plaster", "herhangi bir sıva bulunmamakla", q, neg=True)
S(p, "BUILT", P, G + " duvarları", "has decoration", "herhangi bir bezeme bulunmamakla", q, neg=True)
S(p, "BUILT", P, G + " doğu duvarı", "is built of", "tamamen tuğlayla örülmüş", "doğu duvarı tamamen tuğlayla örülmüşken")
S(p, "BUILT", P, G + " batı duvarı", "masonry", "almaşık düzende örüldüğü", "batı duvarının almaşık")

# ---------------------------------------------------------------- page 119
p = 119
q = "Roma Dönemi nekropol alanında farklı yaş gruplarına yönelik Hipoje yapılarının varlığını ve gömü geleneklerindeki çeşitliliği gözler önüne sermektedir"
S(p, "DATE", P, "nekropol alanı", "is dated to", "Roma Dönemi", q)
S(p, "INTERP", P, "Hipoje 3 incelemesi", "shows existence of", "farklı yaş gruplarına yönelik Hipoje yapıları", q)
S(p, "INTERP", P, "Hipoje 3 incelemesi", "shows", "gömü geleneklerindeki çeşitlilik", q)
S(p, "STRUCT", P, "başlık", "heading reads", "J-17 Plankaresi", "J-17 Plankaresi")
G = "tuğla zemin döşemesi (J-17)"
q = "J-17 plankaresinde kazı çalışmalarında, +97,31 m seviyesinde tuğla zemin döşemesine rastlanmıştır"
S(p, "BUILT", P, G, "is of kind", "tuğla zemin döşemesi", q)
S(p, "BUILT", P, G, "is located in", "J-17 plankaresi", q)
S(p, "BUILT", P, G, "elevation", "+97,31 m", q)
q = "Yüzeye oldukça yakın olan bu zemin döşemesi, 40x40 cm ölçülerinde pişmiş toprak plakalardan oluşmaktadır"
S(p, "BUILT", P, G, "position relative to surface", "yüzeye oldukça yakın", q)
S(p, "BUILT", P, G, "consists of", "pişmiş toprak plakalar", q)
S(p, "MEASURE", P, G + " plakaları", "measures", "40x40 cm", q)
S(p, "BUILT", P, G, "condition", "kırıklar ve çökmeler", "Zeminde kırıklar ve çökmeler gözlenmekle birlikte")
q = "kül toprağı içinden yoğun miktarda irili ufaklı demir çiviler ele geçmiştir"
S(p, "FIND", P, "çiviler (J-17)", "is of kind", "çivi", q)
S(p, "FIND", P, "çiviler (J-17)", "is made of", "demir", q)
S(p, "FIND", P, "çiviler (J-17)", "was found in", "kül toprağı", q)
S(p, "FIND", P, "çiviler (J-17)", "count", "yoğun miktarda", q)
S(p, "FIND", P, "çiviler (J-17)", "size", "irili ufaklı", q)
S(p, "BUILT", P, "kül toprağı (J-17)", "is of kind", "kül toprağı", q)
q = "sınırları kuzey-güney yönünde 4,90 m, doğu-batı yönünde ise 3,04 m olarak ölçülmüştür"
S(p, "MEASURE", P, G, "measures (kuzey-güney, within excavated area)", "4,90 m", q)
S(p, "MEASURE", P, G, "measures (doğu-batı, within excavated area)", "3,04 m", q)
D = "payeler (J-17)"
q = "Tuğla döşemenin batısında birbirinden 174 cm aralıklı 83x70 cm ve 59x75 cm ölçülerinde, sütun kaidesi olabilecek taş ve harçla örülmüş payeler tespit edilmiştir"
S(p, "BUILT", P, D, "is of kind", "paye", q)
S(p, "BUILT", P, D, "is located at", "tuğla döşemenin batısı", q)
S(p, "MEASURE", P, D, "distance between them", "174 cm", q)
S(p, "MEASURE", P, D, "measures (first)", "83x70 cm", q)
S(p, "MEASURE", P, D, "measures (second)", "59x75 cm", q)
S(p, "BUILT", P, D, "is built of", "taş ve harçla örülmüş", q)
S(p, "INTERP", P, D, "is interpreted as", "sütun kaidesi", q, h="olabilecek")
q = "Bu alan muhtemelen Bazilika’nın dışında yer alan atriuma ait döşeme ve Portiko olmalıdır"
S(p, "INTERP", P, "tuğla zemin döşemesi (J-17)", "is interpreted as", "atriuma ait döşeme", q, h="muhtemelen ... olmalıdır")
S(p, "INTERP", P, "payeler (J-17)", "is interpreted as", "Portiko", q, h="muhtemelen ... olmalıdır")
S(p, "BUILT", P, "atrium", "is located at", "Bazilika’nın dışında", q, h="muhtemelen ... olmalıdır")
S(p, "BUILT", P, "ÇM 1 (J-17)", "is of kind", "Çatkı Mezar", "J-17 plankaresinde Çatkı Mezar 1’in")
S(p, "BUILT", P, "ÇM 1 (J-17)", "condition of covers", "kuzey yönündeki ilk kapağı açılabilir",
  "Çatkı Mezar 1’in kuzey yönündeki ilk kapağının açılabilir olduğu")
q = "Çatkı Mezar 2’nin ise kapaklarının büyük çoğunluğunun zemin döşemesinin altında olması sebebiyle"
S(p, "BUILT", P, "ÇM 2 (J-17)", "is of kind", "Çatkı Mezar", q)
S(p, "BUILT", P, "ÇM 2 (J-17)", "lies below", "zemin döşemesi (kapaklarının büyük çoğunluğu)", q)
S(p, "WORK", P, "ÇM 2 (J-17)", "unclear: decision (sentence is broken; not clear whether it also covers ÇM 1)",
  "belgelenerek olduğu haliyle korunması", "belgelenerek olduğu haliyle korunmasına karar verilmiştir")
S(p, "FIGURE", P, "tuğla döşeme ve payeler (J-17)", "is shown in figure", "Resim: 6", "düşünülmektedir (Resim: 6)")
S(p, "STRUCT", P, "başlık", "heading reads", "L-18 Plankaresi", "L-18 Plankaresi")
G = "Hipoje 1 (L-18)"
S(p, "WORK", P, "L-18 plankaresi çalışmaları", "advanced towards", "plankarenin güney yönü",
  "Plankarenin güney yönünde ilerleyen çalışmalar sırasında")
q = "Hipoje 1’e giriş sağlayan 64x64 cm ölçülerindeki terrakota içbükey plaka kapağın tamamı açığa çıkarılmıştır"
S(p, "BUILT", P, G, "unclear: identity (same name as Hipoje 1 of K-16, different measurements)", "Hipoje 1", q)
S(p, "MEASURE", P, G + " plaka kapağı", "measures", "64x64 cm", q)
S(p, "WORK", P, G + " plaka kapağı", "was exposed (extent)", "tamamı", q)
q = "uzunluğu 424 cm, genişliği 230 cm ve yüksekliği 180 cm olan mezarın tonoz bölümünün tuğladan, duvarlarının ise moloz taş ile inşa edildiği"
S(p, "MEASURE", P, G, "measures (inner length)", "424 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "230 cm", q)
S(p, "MEASURE", P, G, "measures (height)", "180 cm", q)
S(p, "BUILT", P, G + " tonoz bölümü", "is built of", "tuğla", q)
S(p, "BUILT", P, G + " duvarları", "is built of", "moloz taş", q)
S(p, "BUILT", P, G, "is coated with", "beyaz renkli bir sıva", "beyaz renkli bir sıva ile kaplandığı belirlenmiştir")
S(p, "BUILT", P, G + " orijinal girişi", "count of entrance points", "iki farklı nokta",
  "Mezarın orijinal girişinin iki farklı noktadan sağlandığı anlaşılmıştır")
q = "mezar tonozunun kuzeydoğu köşesine yerleştirilmiş terrakota içbükey bir plaka kapak ile kapatılmış alanda bulunurken"
S(p, "BUILT", P, G + " ilk girişi", "is located at", "mezar tonozunun kuzeydoğu köşesi", q)
S(p, "BUILT", P, G + " ilk girişi", "is closed with", "terrakota içbükey bir plaka kapak", q)
q = "ikinci girişin güney lunette bölümünde yer alan bir kapı açıklığı (80x48 cm) olduğu düşünülmektedir"
S(p, "INTERP", P, G + " ikinci girişi", "is interpreted as", "güney lunette bölümünde yer alan bir kapı açıklığı", q,
  h="olduğu düşünülmektedir")
S(p, "MEASURE", P, G + " ikinci girişi (kapı açıklığı)", "measures", "80x48 cm", q)
q = "Hipojenin güney kısmında bir kline bulunduğunu, ancak kaçak kazılar sonucu tamamen yok edildiğini ortaya koymuştur"
S(p, "BUILT", P, G + " klinesi", "unclear: is located at (sentence has no subject)", "Hipojenin güney kısmı", q)
S(p, "BUILT", P, G + " klinesi", "was destroyed by", "kaçak kazılar (tamamen)", q)
q = "Mevcut izlere dayanarak yapılan ölçümlere göre, kline yaklaşık 70 cm yüksekliğinde"
S(p, "WORK", P, G + " klinesi", "was measured on the basis of", "mevcut izler", q)
S(p, "MEASURE", P, G + " klinesi", "measures (height)", "70 cm", q, h="yaklaşık")
q = "yönünde 1,05 m, doğu-batı yönünde ise 2,30 m genişliğindedir"
S(p, "MEASURE", P, G + " klinesi", "measures (kuzey-güney)", "1,05 m", q)
S(p, "MEASURE", P, G + " klinesi", "measures (doğu-batı)", "2,30 m", q)
G = "Hipoje 2 (L-18)"
q = "97,87 metre seviyesinde tespit edilen ve kaçak kazıcılar tarafından tahrip edilmiş olan Hipoje 2’de mezar içi çalışmalarına başlanmıştır"
S(p, "BUILT", P, G, "elevation", "97,87 metre", q)
S(p, "BUILT", P, G, "was damaged by", "kaçak kazıcılar", q)
S(p, "WORK", P, G, "work inside the grave started after", "plankare seviye çalışmalarının tamamlanması",
  "Plankare seviye çalışmalarının tamamlanmasının ardından")
q = "tepe kısmında kaçak kazıcılar tarafından açılan 30x50 cm ölçülerindeki bir açıklıktan mezar içine giriş sağlanmıştır"
S(p, "WORK", P, G, "was entered through", "kaçak kazıcılar tarafından açılan açıklık", q)
S(p, "BUILT", P, G + " açıklığı", "is located at", "Hipojenin kuzey kısmı, tepe kısmı", "Hipojenin kuzey kısmında, tepe kısmında")
S(p, "BUILT", P, G + " açıklığı", "was made by", "kaçak kazıcılar", q)
S(p, "MEASURE", P, G + " açıklığı", "measures", "30x50 cm", q)
q = "mezarın tonoz bölümünün tuğla, duvarların ise taş ile örüldüğü ve duvarların inşasında kullanılan harç ile sıvandığı"
S(p, "BUILT", P, G + " tonoz bölümü", "is built of", "tuğla", q)
S(p, "BUILT", P, G + " duvarları", "is built of", "taş", q)
S(p, "BUILT", P, G + " duvarları", "is plastered with", "duvarların inşasında kullanılan harç", q)
S(p, "BUILT", P, G + " klinesi", "is located at", "kuzey cephesi", "kuzey cephesinde bir")
S(p, "BUILT", P, G + " klinesi", "was destroyed by", "kaçak kazıcılar (tamamen)",
  "ancak kaçak kazıcılar tarafından tamamen yok edildiği")
q = "Mevcut izlerden hareketle, klinenin 64 cm yüksekliğinde, doğu-batı yönünde 2,30 m ve"
S(p, "MEASURE", P, G + " klinesi", "measures (height)", "64 cm", q, h="Mevcut izlerden hareketle ... değerlendirilmiştir")
S(p, "MEASURE", P, G + " klinesi", "measures (doğu-batı)", "2,30 m", q, h="Mevcut izlerden hareketle ... değerlendirilmiştir")

# ---------------------------------------------------------------- page 120
p = 120
S(p, "MEASURE", P, G + " klinesi", "measures (kuzey-güney)", "1,05 m",
  "kuzey-güney yönünde 1,05 m ölçülerinde olduğu değerlendirilmiştir", h="Mevcut izlerden hareketle ... değerlendirilmiştir")
q = "İç uzunluğu 326 cm, genişliği 228 cm ve yüksekliği 178 cm olan mezarın orijinal giriş bölümünde merdivenlerin bulunduğu"
S(p, "MEASURE", P, G, "measures (inner length)", "326 cm", q)
S(p, "MEASURE", P, G, "measures (width)", "228 cm", q)
S(p, "MEASURE", P, G, "measures (height)", "178 cm", q)
S(p, "BUILT", P, G + " orijinal giriş bölümü", "has part", "merdivenler", q)
S(p, "BUILT", P, G + " merdiven basamakları", "was removed by", "kaçak kazıcılar (büyük çoğunluğu)",
  "bu merdiven basamaklarının büyük çoğunluğunun kaçak kazıcılar tarafından söküldüğü belirlenmiştir")
S(p, "STRUCT", P, "başlık", "heading reads", "MİMARİ BELGELEME VE KORUMA PROJELERİ", "MİMARİ BELGELEME VE KORUMA PROJELERİ")
S(p, "WORK", P, "mimari belgeleme çalışmaları", "has purpose",
  "Nekropol alanının arkeolojik ve mimari özelliklerini detaylı bir şekilde incelemek ve belgelemek",
  "Nekropol alanının arkeolojik ve mimari özelliklerini detaylı bir şekilde incelemek ve belgelemek amacıyla yürütülmüştür")
q = "alanın mimari belgelerinin hazırlanması süreci, Neval Sarıtekin ile Doruk Bayrak tarafından gerçekleştirilmiştir"
S(p, "PEOPLE", P, "Neval Sarıtekin", "role in the work", "alanın mimari belgelerinin hazırlanması", q)
S(p, "PEOPLE", P, "Doruk Bayrak", "role in the work", "alanın mimari belgelerinin hazırlanması", q)
q = "üç boyutlu vaziyet görüntüleri, plan ve kesit rölöve çizimleriyle kapsamlı bir şekilde belgelenmiştir (Çizim: 2)"
S(p, "WORK", L, "Nekropol (mimari belgeleme)", "was documented with", "üç boyutlu vaziyet görüntüleri", q)
S(p, "WORK", L, "Nekropol (mimari belgeleme)", "was documented with", "plan rölöve çizimleri", q)
S(p, "WORK", L, "Nekropol (mimari belgeleme)", "was documented with", "kesit rölöve çizimleri", q)
S(p, "FIGURE", P, "Nekropol (mimari belgeleme)", "is shown in figure", "Çizim: 2", q)
S(p, "STRUCT", P, "başlık", "heading reads", "Geçici Çatı Örtüsü", "Geçici Çatı Örtüsü")
S(p, "DESCR", P, "arkeolojik kazı alanlarında yapılan çalışmalar", "make necessary", "uygun koruma önlemleri",
  "kazı sürecinin verimli bir şekilde devam etmesini sağlamak için uygun koruma önlemlerini zorunlu kılar")
q = "çevresel faktörlerin (güneş, yağmur, rüzgar vb.) kazı alanına zarar vermesini önlemek amacıyla geçici çatı örtülerinin kullanılması önemlidir"
S(p, "DESCR", P, "geçici çatı örtülerinin kullanılması", "is judged as", "önemlidir", q)
S(p, "DESCR", P, "geçici çatı örtüleri", "has purpose", "çevresel faktörlerin (güneş, yağmur, rüzgar vb.) kazı alanına zarar vermesini önlemek", q)
q = "Kültür ve Turizm Bakanlığından gelen uzmanların incelemeleri sonucunda, mevcut branda ile yapılmış çatı örtülerinin yeterli olmadığı belirlenmiş"
S(p, "ADMIN", P, "mevcut çatı örtüleri", "was inspected by", "Kültür ve Turizm Bakanlığından gelen uzmanlar", q)
S(p, "BUILT", P, "mevcut çatı örtüleri", "is made of", "branda", q)
S(p, "DESCR", P, "mevcut çatı örtüleri", "is sufficient", "yeterli olmadığı", q, neg=True,
  who="Kültür ve Turizm Bakanlığından gelen uzmanlar")
S(p, "WORK", P, "geçici çatı sistemi", "decision", "geçici ancak daha dayanıklı bir sistemin inşa edilmesi",
  "bu yapıların yerine geçici ancak daha dayanıklı bir sistemin inşa edilmesine karar verilmiştir")
q = "Yeni yapılan çatılar, çelik iskelet ve trapez çatı örtüsü kullanılarak oluşturulmuş"
S(p, "BUILT", P, "yeni yapılan çatılar", "is built with", "çelik iskelet", q)
S(p, "BUILT", P, "yeni yapılan çatılar", "is built with", "trapez çatı örtüsü", q)
S(p, "DESCR", P, "yeni yapılan çatılar", "is judged as", "geçici fakat sağlam bir yapı", "bu sayede geçici fakat sağlam bir yapı olması sağlanmıştır")
q = "Çatılar, kazı alanının zeminine müdahale etmeyen ve taşınabilir beton ayaklar ile desteklenmiştir (Resim: 7)"
S(p, "BUILT", P, "yeni yapılan çatılar", "is supported by", "taşınabilir beton ayaklar", q)
S(p, "BUILT", P, "beton ayaklar", "interferes with ground of excavation area", "kazı alanının zeminine müdahale etmeyen", q, neg=True)
S(p, "FIGURE", P, "yeni yapılan çatılar", "is shown in figure", "Resim: 7", q)
q = "Çatıların tasarımında sadece dayanıklılık değil, aynı zamanda işlevsellik ve pratiklik de göz önünde bulundurulmuştur"
for a in ["dayanıklılık", "işlevsellik", "pratiklik"]:
    S(p, "WORK", L, "çatıların tasarımı", "took into account", a, q)
q = "Çalışmalar sırasında yeterli ışık ve hava sirkülasyonu sağlanarak, kazı ekiplerinin verimli bir şekilde çalışması desteklenmiştir"
S(p, "WORK", P, "çatılar", "provides", "yeterli ışık ve hava sirkülasyonu", q)
S(p, "DESCR", P, "çatılar", "supports", "kazı ekiplerinin verimli bir şekilde çalışması", q)
S(p, "DESCR", P, "kullanılan malzemeler", "is judged as", "çevresel etkilere karşı dirençli",
  "Kullanılan malzemelerin çevresel etkilere karşı dirençli olması")
S(p, "DESCR", P, "kullanılan malzemelerin dirençli olması", "effect", "bakım maliyetlerini azaltmakta", "hem bakım maliyetlerini azaltmakta")
S(p, "DESCR", P, "kullanılan malzemelerin dirençli olması", "effect", "sistemin uzun süreli kullanımına olanak tanımaktadır",
  "hem de sistemin uzun süreli kullanımına olanak tanımaktadır")
S(p, "DESCR", P, "bu tür uygulamalar", "contributes to", "kültürel mirasın zarar görmeden geleceğe aktarılması",
  "kültürel mirasın zarar görmeden geleceğe aktarılmasına katkı sağlamaktadır")
S(p, "DESCR", P, "geçici çatı sistemlerinin tasarımı", "is judged as",
  "alanın özgünlüğünü koruyacak hassasiyetin gösterilmesi büyük önem taşımaktadır",
  "alanın özgünlüğünü koruyacak hassasiyetin gösterilmesi büyük önem taşımaktadır")
S(p, "STRUCT", P, "başlık", "heading reads", "SERAMİK VE KÜÇÜK BULUNTU DEĞERLENDİRME ÇALIŞMALARI",
  "SERAMİK VE KÜÇÜK BULUNTU DEĞERLENDİRME ÇALIŞMALARI")
q = "seramik ve küçük buluntu çalışmaları, Gizem Sevinç Memiş ve Beyza Davdav tarafından gerçekleştirilmiştir"
S(p, "PEOPLE", P, "Gizem Sevinç Memiş", "role in the work", "seramik ve küçük buluntu çalışmaları", q)
S(p, "PEOPLE", P, "Beyza Davdav", "role in the work", "seramik ve küçük buluntu çalışmaları", q)
C = "2024 yılı seramikleri"
q = "E-15, E-16, J-15, J-17, J-18, J-K-18, K-16, K-17, K-18, K-L-15-16, L-17 Kuzey Batı Kesit ve L-18 açmasında ele geçen seramik sayısı 1.970 adettir"
S(p, "FIND", P, C, "was found in work season", "2024 yılı çalışma sezonu", "2024 yılı çalışma sezonunda")
for a in ["E-15", "E-16", "J-15", "J-17", "J-18", "J-K-18", "K-16", "K-17", "K-18", "K-L-15-16", "L-17 Kuzey Batı Kesit", "L-18"]:
    S(p, "FIND", L, C, "was found in trench", a, q)
S(p, "FIND", P, C, "count (found)", "1.970 adet", q)
q = "Analizi yapılıp alınan seramik sayısı 559 adet iken atılan seramik sayısı 1.411 adettir"
S(p, "FIND", P, C, "count (analysed and kept)", "559 adet", q)
S(p, "FIND", P, C, "count (discarded)", "1.411 adet", q)

# ---------------------------------------------------------------- page 121
p = 121
q = "çoğunluğu Roma Dönemi’ne (%68) tarihlenmiş, daha sonra sırasıyla Helenistik Dönem (%31) ve çok az sayıda Bizans Dönemi (%1) seramikleri gelmektedir (Çizim: 3)"
S(p, "FIND", L, C, "is dated to (majority)", "Roma Dönemi", q)
S(p, "FIND", L, C, "share of Roma Dönemi", "%68", q)
S(p, "FIND", L, C, "is dated to (second)", "Helenistik Dönem", q)
S(p, "FIND", L, C, "share of Helenistik Dönem", "%31", q)
S(p, "FIND", L, C, "is dated to (third)", "Bizans Dönemi", q)
S(p, "FIND", L, C, "share of Bizans Dönemi", "%1", q)
S(p, "FIND", L, C, "amount of Bizans Dönemi", "çok az sayıda", q)
S(p, "FIGURE", P, C, "is shown in figure", "Çizim: 3", q)


def cer(p, t, bags, qb, per, pct, qp, kinds, pb=None, unclear=False):
    s = "seramikler (%s açması)" % t
    S(pb or p, "FIND", L, s, "count of analysed bags", "%s poşet" % bags, qb)
    S(p, "FIND", L, s, "general majority is dated to", per, qp)
    S(p, "FIND", L, s, ("unclear: " if unclear else "") + "share of majority period", pct, qp)
    for k in kinds:
        name, kper, kdate, kq = k[:4]
        kp = k[4] if len(k) > 4 else p
        ks = "%s (%s açması)" % (name, t)
        S(kp, "FIND", L, ks, "is of kind", name, kq)
        S(kp, "FIND", L, ks, "was found in", t + " açması", kq)
        if kper:
            S(kp, "FIND", L, ks, "is dated to period", kper, kq)
        if kdate:
            S(kp, "FIND", L, ks, "is dated to", kdate, kq)


R, H, B = "Roma Dönemi", "Helenistik Dönem", "Bizans Dönemi"
q1 = "Bu seramiklerin arasında özellikle Mermer Seramikleri ve pişirme kapları da bulunmaktadır"
q2 = "Helenistik Dönem’e ait tam firnisli tabaklar ve Bizans Dönemi’ne ait kırmızı hamurlu tabaklar bulunmaktadır"
cer(p, "E-15", 17, "E-15 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 17 poşet seramik vardır", R, "%77",
    "E-15 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%77)",
    [("Mermer Seramikleri", "", "", q1), ("pişirme kapları", "", "", q1),
     ("tam firnisli tabaklar", H, "", q2), ("kırmızı hamurlu tabaklar", B, "", q2)])
cer(p, "E-16", 11, "E-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 11 poşet seramik vardır", R, "%61",
    "E-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%61)",
    [("tabaklar", R, "", "Bu seramiklerin arasında özellikle Roma Dönemi’ne ait tabaklar bulunmaktadır")])
qx = "J-15 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 1 poşet seramiğin genel yoğunluğu Helenistik Dönem’e aittir (%50)"
cer(p, "J-15", 1, qx, H, "%50", qx,
    [("Tam Firnisli tabaklar", "", "", "Bu seramiklerin arasında özellikle Tam Firnisli tabaklar bulunmaktadır")], unclear=True)
q1 = "Bu seramiklerin arasında özellikle pişirme kapları ve yerel tip kandiller (MS 4.-6. yy.) bulunmaktadır"
cer(p, "J-17", 8, "J-17 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 8 poşet seramik vardır", R, "%85",
    "J-17 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%85)",
    [("pişirme kapları", "", "", q1), ("yerel tip kandiller", "", "MS 4.-6. yy.", q1)])
cer(p, "J-18", 5, "J-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 5 poşet seramik vardır", R, "%58",
    "J-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%58)",
    [("günlük kullanım kapları", R, "", "Bu seramiklerin arasında özellikle Roma Dönemi’ne ait günlük kullanım kapları bulunmaktadır. J-K-18")])
q1 = "Bu seramiklerin arasında özellikle Roma Dönemi’ne ait amphoralar ve mermer seramikleri (MS 3.-4. yy.) bulunmaktadır"
cer(p, "J-K-18", 5, "J-K-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 5 poşet seramik vardır", R, "%62",
    "J-K-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%62)",
    [("amphoralar", R, "", q1), ("mermer seramikleri", R, "MS 3.-4. yy.", q1)])
q2 = "Helenistik Dönem’e (%39) ait Megara kaseleri, gri siyah ve tam firnisli tabaklar bulunmaktadır"
cer(p, "K-16", 10, "K-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 10 poşet seramik vardır", R, "%61",
    "K-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%61)",
    [("günlük kullanım kapları", R, "", "Bu seramiklerin arasında özellikle Roma Dönemi’ne ait günlük kullanım kapları bulunmaktadır. Helenistik"),
     ("Megara kaseleri", H, "", q2), ("gri siyah tabaklar", H, "", q2), ("tam firnisli tabaklar", H, "", q2)])
S(p, "FIND", L, "seramikler (K-16 açması)", "share of Helenistik Dönem", "%39", q2)
q1 = "Roma Dönemi’ne ait Filistin Amphorası (MS 5.-6. yy.), Yerel Tip Kandiller (MS 3.-4. yy.) ve Günlük Kullanım Kapları bulunmaktadır"
cer(p, "K-17", 8, "K-17 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 8 poşet seramik vardır", R, "%77",
    "K-17 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%77)",
    [("Filistin Amphorası", R, "MS 5.-6. yy.", q1), ("Yerel Tip Kandiller", R, "MS 3.-4. yy.", q1),
     ("Günlük Kullanım Kapları", R, "", q1)])
q1 = "Roma Dönemi’ne ait yerel tip kandiller (MS 4.-6. yy.) ve Günlük Kullanım kapları bulunmaktadır"
q2 = "Helenistik Dönem’e (%33) ait basit ve tam firnisli tabaklar da bulunmaktadır"
cer(p, "K-18", 6, "K-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 6 poşet seramik vardır", R, "%67",
    "K-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%67)",
    [("yerel tip kandiller", R, "MS 4.-6. yy.", q1), ("Günlük Kullanım kapları", R, "", q1),
     ("basit firnisli tabaklar", H, "", q2), ("tam firnisli tabaklar", H, "", q2)])
S(p, "FIND", L, "seramikler (K-18 açması)", "share of Helenistik Dönem", "%33", q2)
q1 = "Roma Dönemi’ne ait Yerel Tip Kandiller (MS 4.-6. yy.) ve Günlük Kullanım Kapları bulunmaktadır"
cer(p, "K-L-15-16", 4, "K-L-15-16 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 4 poşet seramik vardır", R, "%74",
    "K-L-15-16 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%74)",
    [("Yerel Tip Kandiller", R, "MS 4.-6. yy.", q1), ("Günlük Kullanım Kapları", R, "", q1)])

# ---------------------------------------------------------------- page 122
p = 122
q1 = "Roma Dönemi’ne ait pişirme kapları, kandil kulbu ve mermer seramikleri bulunmaktadır"
cer(p, "L-17 Kuzey Batı Kesit", 2, "açmasında yapılan kazı çalışmalarında analizi yapılan toplam 2 poşet seramik vardır", R, "%74",
    "Seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%74)",
    [("pişirme kapları", R, "", q1), ("kandil kulbu", R, "", q1), ("mermer seramikleri", R, "", q1)])
q1 = "seramiklerin arasında özellikle Roma Dönemi’ne ait pişirme kapları ve tabaklar bulunmaktadır"
q2 = "Helenistik Dönem’e (%35) ait Megara kaseleri ve basit firnisli tabaklar bulunmaktadır"
cer(p, "L-18", 6, "L-18 açmasında yapılan kazı çalışmalarında analizi yapılan toplam 6 poşet seramik vardır", R, "%63",
    "L-18 açmasından ele geçen seramiklerin genel yoğunluğu Roma Dönemi’ne aittir (%63)",
    [("pişirme kapları", R, "", q1), ("tabaklar", R, "", q1),
     ("Megara kaseleri", H, "", q2), ("basit firnisli tabaklar", H, "", q2)])
S(p, "FIND", L, "seramikler (L-18 açması)", "share of Helenistik Dönem", "%35", q2)
S(p, "STRUCT", P, "başlık", "heading reads", "RESTORASYON VE KONSERVASYON ÇALIŞMALARI", "RESTORASYON VE KONSERVASYON ÇALIŞMALARI")
q = "konservasyon çalışmaları, Arkeolog/Restoratör Tuğçe Güçlü tarafından gerçekleştirilmiştir"
S(p, "PEOPLE", P, "Tuğçe Güçlü", "role in the work", "konservasyon çalışmaları", q)
S(p, "PEOPLE", P, "Tuğçe Güçlü", "has title", "Arkeolog/Restoratör", q)
q = "1 adet pişmiş toprak testi, 1 adet metal obje, bir çift altın küpe ve 6 adet bronz sikke konservasyon amacıyla teslim alınmıştır"
S(p, "LAB", L, "pişmiş toprak testi", "count received for conservation", "1 adet", q)
S(p, "LAB", L, "metal obje", "count received for conservation", "1 adet", q)
S(p, "LAB", L, "altın küpe", "count received for conservation", "bir çift", q)
S(p, "LAB", L, "bronz sikke", "count received for conservation", "6 adet", q)
q = "Eserler, öncelikle kayıt altına alınmış, ardından detaylı konservasyon işlemlerine başlanmıştır"
S(p, "LAB", P, "eserler (konservasyon)", "first step", "kayıt altına alınmış", q)
S(p, "LAB", P, "eserler (konservasyon)", "next step", "detaylı konservasyon işlemlerine başlanmıştır", q)
q = "Metal eserlerin temizliğinde, yüzeydeki korozyonun yumuşatılması amacıyla %50 oranında saf su ve alkol karışımı kullanılmıştır"
S(p, "LAB", P, "metal eserlerin temizliği", "used substance", "%50 oranında saf su ve alkol karışımı", q)
S(p, "LAB", P, "metal eserlerin temizliği", "purpose of substance", "yüzeydeki korozyonun yumuşatılması", q)
q = "eserlerin mikroskop altında mekanik temizliği gerçekleştirilmiştir"
S(p, "LAB", P, "metal eserlerin temizliği", "step", "mekanik temizlik", q)
S(p, "LAB", P, "metal eserlerin temizliği", "was done under", "mikroskop", q)
q = "Bu süreçte bisturi, bambu çubuk, çeşitli fırçalar ve dişçi motoru gibi profesyonel ekipmanlar kullanılmıştır"
for a in ["bisturi", "bambu çubuk", "çeşitli fırçalar", "dişçi motoru"]:
    S(p, "LAB", L, "metal eserlerin mekanik temizliği", "used tool", a, q)
q = "Temizlik işlemi tamamlanan metal eser ve sikkelere, koruma ve stabilizasyon amacıyla %3 oranında Paraloid B72 çözeltisi uygulanmıştır"
S(p, "LAB", P, "metal eser ve sikkeler", "was treated with", "%3 oranında Paraloid B72 çözeltisi", q)
S(p, "LAB", P, "Paraloid B72 çözeltisi uygulaması", "purpose", "koruma ve stabilizasyon", q)
q = "Ardından eserler, uygun koşullarda muhafaza edilmek üzere kaldırılmıştır (Resim: 8)"
S(p, "LAB", P, "metal eser ve sikkeler", "final step", "uygun koşullarda muhafaza edilmek üzere kaldırılmıştır", q)
S(p, "FIGURE", P, "konservasyonu yapılan eserler", "is shown in figure", "Resim: 8", q)
T = "pişmiş toprak testi (Hipoje-2, K16)"
q = "K16 Plankaresi Hipoje-2 içinden çıkarılan pişmiş toprak testinin temizliğinde"
S(p, "FIND", P, T, "is made of", "pişmiş toprak", q)
q = "yüzeydeki kalker tabakasının yumuşaması için %50 oranında saf su ve alkol karışımı kullanılmıştır"
S(p, "LAB", P, T, "surface condition", "kalker tabakası", q)
S(p, "LAB", P, T, "cleaning used substance", "%50 oranında saf su ve alkol karışımı", q)
S(p, "LAB", P, T, "was treated by method", "paketleme yöntemiyle karışım içinde bekletilmiş",
  "eser, paketleme yöntemiyle karışım içinde bekletilmiş")
q = "yumuşayan kalker tabakası çeşitli bisturi uçları kullanılarak mekanik yöntemlerle temizlenmiştir"
S(p, "LAB", P, T, "was cleaned by method", "mekanik yöntemler", q)
S(p, "LAB", P, T, "cleaning used tool", "çeşitli bisturi uçları", q)
q = "Temizlik işlemleri tamamlanan eser, uygun şekilde muhafaza edilmek üzere teslim edilmiştir (Resim: 9)"
S(p, "LAB", P, T, "final step", "uygun şekilde muhafaza edilmek üzere teslim edilmiştir", q)
S(p, "FIGURE", P, T, "is shown in figure", "Resim: 9", q)
S(p, "STRUCT", P, "başlık", "heading reads", "ANTROPOLOJİ ÇALIŞMALARI", "ANTROPOLOJİ ÇALIŞMALARI")
S(p, "PEOPLE", P, "Ruken Zeynep Köse", "role in the work", "antropoloji çalışmaları",
  "antropoloji çalışmaları, Antropolog Ruken Zeynep Köse tarafından gerçekleştirilmiştir")
q = "Önceki yıllarda ortaya çıkarılan Hipoje 2022-1 ve Hipoje 2023-1’e ait iskelet kalıntıları detaylı bir şekilde belgelenmiştir"
for a in ["Hipoje 2022-1", "Hipoje 2023-1"]:
    S(p, "BUILT", P, a, "was exposed in", "önceki yıllar", q)
    S(p, "WORK", P, a + " iskelet kalıntıları", "was documented", "detaylı bir şekilde belgelenmiştir", q)
q = "2024 yılında bulunan Hipojeler, Sanduka Mezar ve Çatkı Mezarlar içinden çıkan iskeletler üzerinde cinsiyet, yaş tayini ve hastalıklarla ilgili detaylı incelemeler yapılmıştır"
for a in ["Hipojeler", "Sanduka Mezar", "Çatkı Mezarlar"]:
    S(p, "LAB", L, "incelenen iskeletler (2024)", "come from", a, q)
for a in ["cinsiyet", "yaş tayini", "hastalıklar"]:
    S(p, "LAB", L, "incelenen iskeletler (2024)", "was examined for", a, q)
S(p, "LAB", P, "cinsiyet belirleme", "examined first", "cranium ve pelvis kemikleri",
  "Cinsiyet belirlemede, ilk olarak cranium ve pelvis kemikleri incelenmiştir")
for a, q in [("craniumda bulunan mastoid çıkıntıların yapısı", "craniumda bulunan mastoid çıkıntıların yapısı"),
             ("kaş kemerleri ve glabellanın belirginliği", "kaş kemerleri ve glabellanın belirginliği"),
             ("orbitaların şekli", "orbitaların şekli"),
             ("mandibula kemiklerinin özellikleri", "mandibula kemiklerinin özellikleri"),
             ("uzun kemiklerdeki kas tutunma izleri", "uzun kemiklerdeki kas tutunma izleri dikkate alınmıştır")]:
    S(p, "LAB", L, "cinsiyet belirleme", "took into account", a, q)
S(p, "LAB", P, "yaş tayini", "method", "yaş grupları için farklı teknik ve yöntem",
  "yaş grupları için farklı teknik ve yöntem kullanılmıştır")
q = "diş sürme süreci ve sağlam olan uzun kemiklerden ölçüm alınarak belirlenmiştir"
S(p, "LAB", P, "yaş tayini (bebek ve çocuklar)", "method", "diş sürme süreci", q)
S(p, "LAB", P, "yaş tayini (bebek ve çocuklar)", "method", "sağlam olan uzun kemiklerden ölçüm", q)

# ---------------------------------------------------------------- page 123
p = 123
q = "epifiz kaynaşması, diş köklerinin kapanma dereceleri dikkate alınmıştır"
S(p, "LAB", P, "yaş tayini (genç erişkinler)", "method", "epifiz kaynaşması", q)
S(p, "LAB", P, "yaş tayini (genç erişkinler)", "method", "diş köklerinin kapanma dereceleri", q)
for a, q in [("cranium sütural kapanma dereceleri", "cranium sütural kapanma dereceleri"),
             ("symphysial yaşlandırma", "symphysial yaşlandırma"),
             ("dental aşınma derecesi", "derecesi ve clavicula kemiğinin uçlarına bakılarak yapılmıştır"),
             ("clavicula kemiğinin uçları", "clavicula kemiğinin uçlarına bakılarak yapılmıştır")]:
    S(p, "LAB", L, "yaş tayini (erişkin bireyler)", "method", a, q)
q = "farklı mezar tipleri, gömü türleri, mezar içindeki yatış pozisyonları ve ritüeller gözlemlenmiştir"
for a in ["farklı mezar tipleri", "gömü türleri", "mezar içindeki yatış pozisyonları", "ritüeller"]:
    S(p, "LAB", L, "antropolojik sonuç", "observed", a, q)
S(p, "DESCR", P, "antropolojik bulgular", "is judged as", "önemli bilgiler sunmaktadır",
  "dönemin sosyo-kültürel yapısı ve inanç sistemleri hakkında önemli bilgiler sunmaktadır")
q = "iskeletler çevresel, fiziksel ve toprak yapısı ile alakalı olarak fazlasıyla zarar görmüştür"
S(p, "FIND", P, "bazı mezarların içerisinde yer alan iskeletler", "condition", "fazlasıyla zarar görmüş", q)
S(p, "INTERP", P, "iskeletlerin zarar görmesi", "is related to", "çevresel, fiziksel ve toprak yapısı", q)
q = "Özellikle Hisardere alanının önceki zamanlarda tarım amaçlı kullanılması bu durumun en önemli sebebidir"
S(p, "HISTORY", P, "Hisardere alanı", "was used for", "tarım (önceki zamanlarda)", q)
S(p, "INTERP", P, "iskeletlerin zarar görmesi", "most important cause", "alanın tarım amaçlı kullanılması", q)
q = "vertebralarda (omurlarda) oluşan Schormol nodülü, osteoartrit gibi hastalıklar"
S(p, "LAB", P, "kemikler", "disease observed", "Schormol nodülü", q)
S(p, "LAB", P, "Schormol nodülü", "is located in", "vertebralar (omurlar)", q)
S(p, "LAB", P, "kemikler", "disease observed", "osteoartrit", q)
S(p, "INTERP", P, "bireyler", "is interpreted as", "ağır ve fiziksel işlerde çalıştığı",
  "bireylerin ağır ve fiziksel işlerde çalıştığını göstermektedir")
q = "dişlerdeki aşınmalar ve kırıklar, dişlerin günlük yaşamda bir alet ya da “üçüncü el” gibi kullanıldığını ortaya koymakta"
S(p, "LAB", P, "dişler", "observed", "aşınmalar", q)
S(p, "LAB", P, "dişler", "observed", "kırıklar", q)
S(p, "INTERP", P, "dişler", "is interpreted as used as", "bir alet ya da “üçüncü el”", q)
S(p, "DESCR", P, "dişlerin alet gibi kullanılması", "gives information on", "bireylerin sosyo-ekonomik koşulları",
  "ekonomik koşulları hakkında bilgi sağlamaktadır")
q = "Dişlerde gözlemlenen hipoplaziler, çocukluk döneminde besin yetersizliğinin ve stres düzeyinin yüksek olduğunun göstergesidir"
S(p, "LAB", P, "dişler", "observed", "hipoplaziler", q)
S(p, "INTERP", P, "hipoplaziler", "indicates", "çocukluk döneminde besin yetersizliği", q)
S(p, "INTERP", P, "hipoplaziler", "indicates", "çocukluk döneminde stres düzeyinin yüksek olduğu", q)
q = "metabolik ve enfeksiyonel hastalıkların varlığı da gözlemlenmiştir"
S(p, "LAB", P, "iskeletler", "disease observed", "metabolik hastalıklar", q)
S(p, "LAB", P, "iskeletler", "disease observed", "enfeksiyonel hastalıklar", q)
S(p, "LAB", P, "metabolik hastalıklar", "observed especially in", "çocuklar", "Özellikle çocuklarda izlenen metabolik hastalıkların nedeni")
q = "beslenme yetersizliği, anne sütü bakımından eksiklik ve hijyen koşulları hakkında ipucu sağlamaktadır"
for a in ["beslenme yetersizliği", "anne sütü bakımından eksiklik", "hijyen koşulları"]:
    S(p, "INTERP", L, "çocuklarda izlenen metabolik hastalıklar", "gives a clue about", a, q, h="ipucu sağlamaktadır")
S(p, "DESCR", P, "antropolojik sonuçlar", "gave information on",
  "popülasyonun sosyo-kültürel durumu, beslenme pratikleri ve yaşam tarzları",
  "kültürel durumu, beslenme pratikleri ve yaşam tarzları hakkında bilgi sağlamıştır")
S(p, "STRUCT", P, "başlık", "heading reads", "SONUÇ", "SONUÇ")
S(p, "DESCR", P, K, "is judged as", "dikkate değer veriler sunmuştur",
  "mimari yapısı ve gömü pratikleriyle ilgili dikkate değer veriler sunmuştur")
S(p, "DESCR", P, K, "manner of work", "titizlikle yürütülmüştür", "ışığında titizlikle yürütülmüştür")
q = "Geleceğe Miras Projesi kapsamındaki çalışmalar E-15 ve E-16, J-17, J-18, J-K/18, K-16, K-17, K-18, K-L/15-16, L-17 ve L-18 plankarelerinde"
S(p, "WORK", L, "Geleceğe Miras Projesi kapsamındaki çalışmalar", "took place in square", "E-15", q)
S(p, "WORK", L, "Geleceğe Miras Projesi kapsamındaki çalışmalar", "took place in square", "E-16", q)
q = "Kazılar sonucunda 7 adet Hipoje, 10 adet Çatkı Mezar, 1 adet Taş Sanduka Mezar ve 2 adet Tuğla Plaka Mezar ortaya çıkarılmıştır"
for a, b in [("Hipoje", "7 adet"), ("Çatkı Mezar", "10 adet"), ("Taş Sanduka Mezar", "1 adet"), ("Tuğla Plaka Mezar", "2 adet")]:
    S(p, "BUILT", L, a + " (2024 kazıları)", "count exposed", b, q)
q = "Ele geçen buluntulardan 7 tanesi envanterlik eser, 6 tanesi ise etütlük eser olarak ayrılmıştır"
S(p, "FIND", P, "envanterlik eser", "count", "7 tanesi", q)
S(p, "FIND", P, "etütlük eser", "count", "6 tanesi", q)
S(p, "INTERP", P, "Nekropol alanı", "is interpreted as",
  "yalnızca bir mezarlık değil, aynı zamanda sosyal ve dini bağlamlarla bütünleşmiş bir yapıya sahip",
  "Nekropol alanının yalnızca bir mezarlık değil, aynı zamanda sosyal ve dini bağlamlarla bütünleşmiş bir yapıya sahip olduğu tespit edilmiştir")
q = "nekropolde mozaik taban döşemeleri, duvar kalıntıları ve farklı gömü türlerini temsil eden mezar yapıları gibi pek çok önemli bulguya da ulaşılmıştır"
for a in ["mozaik taban döşemeleri", "duvar kalıntıları", "farklı gömü türlerini temsil eden mezar yapıları"]:
    S(p, "BUILT", L, "nekropol", "yielded", a, q)
S(p, "DESCR", P, "nekropol bulguları", "is judged as", "pek çok önemli bulgu", q)
S(p, "INTERP", P, "Bazilika ile Nekropol alanındaki mezarlar arasındaki mekânsal ilişki", "is notable in", "Hipoje mezarlar",
  "Hipoje mezarlarda dikkati çekmektedir")
q = "Söz konusu Hipojelerde birden fazla bireye ait iskelet kalıntıları ve beraberlerinde çeşitli mezar hediyeleri ele geçirilmiştir"
S(p, "FIND", P, "iskelet kalıntıları (Hipojeler)", "count of individuals", "birden fazla birey", q)
S(p, "FIND", P, "mezar hediyeleri (Hipojeler)", "is of kind", "çeşitli mezar hediyeleri", q)
S(p, "FIND", P, "mezar hediyeleri (Hipojeler)", "was found in", "Hipojeler", q)
q = "mezarların yalnızca bireysel definler için değil, aile ya da topluluk mezarları olarak kullanıldığını göstermektedir"
S(p, "INTERP", P, "Hipoje mezarlar", "is interpreted as", "aile ya da topluluk mezarları", q)
S(p, "INTERP", P, "Hipoje mezarlar", "was used only for individual burials", "yalnızca bireysel definler için değil", q, neg=True)
S(p, "INTERP", P, "bölge (Nekropol alanı)", "was used in Roma Dönemi as", "gömü alanı",
  "bölgenin Roma Dönemi’nde gömü alanı olarak kullanılırken")
S(p, "INTERP", P, "bölge (Nekropol alanı)", "in Erken Bizans Dönemi had", "dini yapılarla bütünleşmiş bir düzenleme",
  "Erken Bizans Dönemi’nde dini yapılarla bütünleşmiş bir")

# ---------------------------------------------------------------- page 124
p = 124
q = "Bazilika’nın yalnızca bir ibadet mekânı değil, aynı zamanda ölülerle yaşayanlar arasında manevi bir köprü görevi gören Mezarlık Kilisesi olabileceğini göstermektedir"
S(p, "INTERP", P, "Bazilika", "is interpreted as", "Mezarlık Kilisesi", q, h="olabileceğini göstermektedir")
S(p, "DESCR", P, "Mezarlık Kilisesi", "is described as", "ölülerle yaşayanlar arasında manevi bir köprü görevi gören", q,
  h="olabileceğini göstermektedir")
S(p, "DESCR", P, "Hisardere Nekropolü Kazıları", "reveals",
  "Roma Dönemi Nekropol alanlarının mekânsal düzeni, dini ve toplumsal bağlamları açısından dönemin dinamik yapısı",
  "dini ve toplumsal bağlamları açısından dönemin dinamik yapısını gözler önüne sermektedir")
S(p, "DESCR", P, "elde edilen bulgular", "raise", "Roma Dönemi ölü gömme ritüelleri ve mimari planlama konusunda yeni sorular",
  "Roma Dönemi ölü gömme ritüelleri ve mimari planlama konusunda yeni sorular ortaya çıkarırken")
S(p, "DESCR", P, "alan", "need stressed", "korunması ve daha ileri teknolojiyle incelenmesi gerekliliği",
  "korunması ve daha ileri teknolojiyle incelenmesi gerekliliğini de vurgulamaktadır")

# ---------------------------------------------------------------- annex
S(125, "STRUCT", P, "başlık", "heading reads", "EKLER", "EKLER")
for pg, a, b in [
    (125, "Çizim 1", "İznik Hisardere Nekropolü Kazı Alanı."),
    (125, "Çizim 2", "Kesit üzerinde mezarlar arasındaki ilişki."),
    (126, "Çizim 3", "2024 yılı seramik buluntu örnekleri."),
    (127, "Resim 1", "Terrakota Plaka Kapaklı Mezar-1."),
    (127, "Resim 2", "E-15 Plankaresi’nde ortaya çıkarılan mezarlar."),
    (128, "Resim 3", "K-16 Plankaresi’nde ortaya çıkarılan Çatkı Mezar-1."),
    (128, "Resim 4", "K-16 Plankaresi’nde ortaya çıkarılan Hipoje-2."),
    (129, "Resim 5", "K-16 Plankaresi’nde ortaya çıkarılan Hipoje-1."),
    (129, "Resim 6", "J-17 Plankaresi Tuğla Zemin Döşemesi."),
    (130, "Resim 7", "Nekropol alanına yapılan Geçici Koruma Çatısı."),
    (130, "Resim 8", "Konservasyonu yapılan altın küpeler."),
    (131, "Resim 9", "K16 Plankaresi Hipoje-2 içinden çıkarılan pişmiş toprak testi."),
    (131, "Resim 10", "Kemikler üzerinde gözlemlenen hastalıklar."),
]:
    S(pg, "FIGURE", L, a, "has caption", b, "%s: %s" % (a, b))

# ---------------------------------------------------------------- order, number, write
rows.sort(key=lambda r: r["page"])  # stable: keeps order inside a page
out = []
for i, r in enumerate(rows, 1):
    out.append(dict(n=i, page=r["page"], group=r["group"], form=r["form"], subject=r["subject"], says=r["says"],
                    value=r["value"], hedge=r["hedge"], negative=r["negative"], who=r["who"], quote=r["quote"]))
json.dump(out, open(BASE + "readerB/statements.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- check
data = json.load(open(BASE + "readerB/statements.json", encoding="utf-8"))
raw = open(BASE + "paper.txt", encoding="utf-8").read()


def norm(t):
    t = re.sub(r"-\s*\n\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


pages = {115 + i: norm(c) for i, c in enumerate(raw.split("\f"))}
full = norm(raw.replace("\f", "\n"))
KEYS = ["n", "page", "group", "form", "subject", "says", "value", "hedge", "negative", "who", "quote"]
GROUPS = "DOC STRUCT PEOPLE ADMIN WORK PLACE BUILT FIND MEASURE DATE INTERP LAB FIGURE DESCR HISTORY".split()
bad = 0
seen = set()
for r in data:
    e = []
    if list(r.keys()) != KEYS: e.append("keys")
    if r["group"] not in GROUPS: e.append("group")
    if r["form"] not in ("list", "prose"): e.append("form")
    if not isinstance(r["negative"], bool): e.append("negtype")
    qq = norm(r["quote"])
    if len(r["quote"]) > 200: e.append("quote too long %d" % len(r["quote"]))
    if qq not in full: e.append("quote not in paper")
    elif qq not in pages.get(r["page"], ""): e.append("quote not on page")
    if "@" in json.dumps(r, ensure_ascii=False): e.append("email")
    key = (r["subject"], r["says"], r["value"])
    if key in seen: e.append("duplicate")
    seen.add(key)
    if e:
        bad += 1
        print(r["n"], r["page"], e, "|", r["subject"], "|", r["quote"])
print("statements", len(data), "failures", bad)
print("groups", sorted(collections.Counter(r["group"] for r in data).items()))
print("forms", dict(collections.Counter(r["form"] for r in data)))
print("pages", sorted(collections.Counter(r["page"] for r in data).items()))
print("hedged", sum(1 for r in data if r["hedge"]), "negative", sum(1 for r in data if r["negative"]))
print("unclear", [(r["n"], r["page"], r["subject"]) for r in data if r["says"].startswith("unclear")])
