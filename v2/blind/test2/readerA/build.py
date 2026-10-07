# -*- coding: utf-8 -*-
import json, re, collections

PAPER = "/media/tugce/ProgramsVS/tez/v2/blind/test2/paper.txt"
OUT = "/media/tugce/ProgramsVS/tez/v2/blind/test2/readerA/statements.json"
GROUPS = "DOC STRUCT PEOPLE ADMIN WORK PLACE BUILT FIND MEASURE DATE INTERP LAB FIGURE DESCR HISTORY".split()

R = []


def S(p, g, subj, says, val, q, h="", neg=False, who=""):
    R.append(dict(page=p, group=g, subject=subj, says=says, value=val, hedge=h,
                  negative=neg, who=who, quote=q))


HH = "Hacımusalar Höyük"
MK = "Merkezi Kilise"
KY = "Kuzey Yamaç"

# ---------------------------------------------------------------- page 279
p = 279
S(p, "STRUCT", "sayfa üst başlığı", "page header reads", "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1",
  "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1")
S(p, "DOC", "bildiri", "has title", "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK KAZISI 2024 YILI ÇALIŞMALARI",
  "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK KAZISI 2024 YILI ÇALIŞMALARI")
S(p, "DOC", "bildiri", "has author", "Bülent ARIKAN", "Bülent ARIKAN*")
S(p, "PLACE", HH, "is located in (il)", "Antalya", "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK")
S(p, "PLACE", HH, "is located in (ilçe)", "Elmalı", "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK")
S(p, "STRUCT", "başlık", "heading reads", "1. GİRİŞ", "1. GİRİŞ")
S(p, "ADMIN", "arkeolojik araştırmalar", "carried out on behalf of", "T.C. Kültür ve Turizm Bakanlığı (KTB)",
  "T.C. Kültür ve Turizm Bakanlığı (KTB) ile T.C. İstanbul Teknik Üniversitesi (İTÜ) adına")
S(p, "ADMIN", "arkeolojik araştırmalar", "carried out on behalf of", "T.C. İstanbul Teknik Üniversitesi (İTÜ)",
  "T.C. Kültür ve Turizm Bakanlığı (KTB) ile T.C. İstanbul Teknik Üniversitesi (İTÜ) adına")
S(p, "ADMIN", "arkeolojik araştırmalar", "permitted by", "Cumhurbaşkanlığı Kararnamesi",
  "07.07.2022 tarih ve 5777 sayılı Cumhurbaşkanlığı Kararnamesiyle")
S(p, "ADMIN", "Cumhurbaşkanlığı Kararnamesi", "has date", "07.07.2022",
  "07.07.2022 tarih ve 5777 sayılı Cumhurbaşkanlığı Kararnamesiyle")
S(p, "ADMIN", "Cumhurbaşkanlığı Kararnamesi", "has number", "5777",
  "07.07.2022 tarih ve 5777 sayılı Cumhurbaşkanlığı Kararnamesiyle")
S(p, "WORK", "arkeolojik araştırmalar", "took place at", HH,
  "Hacımusalar Höyük’te başkanlığımda yürütülmekte olan arkeolojik araştırmalar")
S(p, "PEOPLE", "Bülent ARIKAN", "role in the work", "başkan (başkanlığımda)",
  "Hacımusalar Höyük’te başkanlığımda yürütülmekte olan arkeolojik araştırmalar")
S(p, "WORK", "arkeolojik araştırmalar (2024)", "took place between", "01.07–27.09.2024",
  "01.07–27.09.2024 tarihleri arasında gerçekleştirilmiştir")
S(p, "WORK", "kazı sezonu", "duration", "üç ay", "Üç aya yayılan kazı sezonunda")
S(p, "PEOPLE", "Selda Baybo", "role in the work", "kazı başkanı yardımcısı",
  "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Selda Baybo", "title", "Dr. Öğr. Üy.", "Dr. Öğr. Üy. Selda Baybo")
S(p, "PEOPLE", "Selda Baybo", "affiliation", "Çanakkale On Sekiz Mart Üniversitesi",
  "Selda Baybo (Çanakkale On Sekiz Mart Üniversitesi)")
S(p, "PEOPLE", "Ergin Tatar", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Ergin Tatar", "affiliation", "Ege Üniversitesi", "Ergin Tatar (Ege Üniversitesi)")
S(p, "PEOPLE", "Fatih Mehmet Çongur", "role in the work", "kazı başkanı yardımcısı",
  "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Fatih Mehmet Çongur", "affiliation", "İstanbul Üniversitesi",
  "Fatih Mehmet Çongur (İstanbul Üniversitesi)")
S(p, "PEOPLE", "Onur Kaya", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Onur Kaya", "affiliation", "İstanbul Üniversitesi", "Onur Kaya (İstanbul Üniversitesi)")
S(p, "ADMIN", "Selma Akgül", "role in the work", "Kültür ve Turizm Bakanlığı temsilcisi",
  "Selma Akgül de Kültür ve Turizm Bakanlığı temsilcisi olarak yer almıştır")
S(p, "ADMIN", "Selma Akgül", "office", "Erzurum Müzesi uzmanı",
  "Erzurum Müzesi uzmanlarından Selma Akgül")
S(p, "PEOPLE", "2024 sezonu çalışmalarına katılanlar", "count", "toplam 41 kişi",
  "2024 sezonu çalışmalarına toplam 41 kişi katılmıştır")
S(p, "PEOPLE", "katılanlar: lisans öğrencisi", "count", "22", "22’si lisans öğrencisi")
S(p, "PEOPLE", "katılanlar: lisansüstü öğrencisi", "count", "6", "6’sı lisansüstü öğrencisi")
S(p, "PEOPLE", "katılanlar: öğretim üyesi", "count", "4", "4’ü öğretim üyesi")
S(p, "PEOPLE", "katılanlar: uzman", "count", "9", "9’u ise uzman")
S(p, "PEOPLE", "uzmanlar", "profession", "arkeolog", "uzman (arkeolog ve jeofizik mühendisi)")
S(p, "PEOPLE", "uzmanlar", "profession", "jeofizik mühendisi", "uzman (arkeolog ve jeofizik mühendisi)")
S(p, "STRUCT", "bildiri", "summarises the work under headings", "aşağıdaki başlıklar altında",
  "Yürütülen çalışmalar aşağıdaki başlıklar altında özetlenmiştir")
S(p, "STRUCT", "başlık", "heading reads", "2-KARELAJ ÇALIŞMASI:", "2-KARELAJ ÇALIŞMASI:")
S(p, "WORK", "karelaj", "was prepared in (year)", "1993", "1993 yılında Antalya Müzesi uzmanlarından Sabri Aydal")
S(p, "WORK", "karelaj", "was prepared by", "Sabri Aydal", "Sabri Aydal tarafından hazırlanan karelajın")
S(p, "ADMIN", "Sabri Aydal", "office", "Antalya Müzesi uzmanı", "Antalya Müzesi uzmanlarından Sabri Aydal")
S(p, "WORK", "karelaj (1993)", "has digital version", "dijital hali", "karelajın dijital hali bulunmadığından",
  neg=True)
S(p, "WORK", "Höyüğün karelajı", "was digitised", "dijital hale getirilmiştir",
  "Höyüğün karelajı 1993 yılındaki plana sadık kalınarak dijital hale getirilmiştir")
S(p, "WORK", "karelajın dijitalleştirilmesi", "method", "1993 yılındaki plana sadık kalınarak",
  "1993 yılındaki plana sadık kalınarak dijital hale getirilmiştir")
S(p, "WORK", "açma kodları", "result of digitising", "birlik sağlanmıştır",
  "Böylece açma kodlarında birlik sağlanmıştır")
S(p, "PLACE", "1993 yılında ölçülen kotlar ile modern ölçümler", "difference between", "yaklaşık 30 metre",
  "modern ölçümler arasında yaklaşık 30 metre farklılık olduğu tespit edilmiştir", h="yaklaşık")
S(p, "WORK", "1993 kotları", "continue to be used", "kullanılmaya devam edilmektedir",
  "1993 kotları kullanılmaya devam edilmektedir")
S(p, "WORK", "1993 kotlarının kullanımı", "reason", "önceki kazı sezonlarının verisiyle uyumu sağlamak",
  "Önceki kazı sezonlarının verisiyle uyumu sağlamak açısından")
S(p, "STRUCT", "başlık", "heading reads", "3-JEOFİZİK ETÜTLERİ:", "3-JEOFİZİK ETÜTLERİ:")
S(p, "WORK", "başkanlığım altında yürütülen kazılar", "first season (year)", "2022",
  "Başkanlığım altında yürütülen kazıların ilk sezonu olan 2022 yılından beri")
S(p, "WORK", "yer radarı çalışmaları", "took place at", "Höyüğün üst düzlüğü",
  "Höyüğün üst düzlüğünde")
S(p, "WORK", "yer radarı çalışmaları", "carried out since", "2022",
  "2022 yılından beri Höyüğün üst düzlüğünde")
S(p, "PEOPLE", "yer radarı çalışmaları", "carried out by",
  "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri",
  "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri ve öğrencileri tarafından yürütülen yer radarı çalışmalarında")
S(p, "PEOPLE", "yer radarı çalışmaları", "carried out by",
  "İTÜ Jeofizik Mühendisliği Bölümü öğrencileri",
  "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri ve öğrencileri tarafından yürütülen yer radarı çalışmalarında")
S(p, "WORK", "yer radarı çalışması (2022 sezonu)", "area scanned", "Merkezi Kilise ile Kuzey Yamaç açmaları arası",
  "2022 sezonunda Merkezi Kilise ile Kuzey Yamaç açmaları arası")
S(p, "WORK", "yer radarı çalışması (2023 sezonu)", "area scanned", "Merkezi Kilise ile Batı Kilise arası",
  "2023 sezonunda ise Merkezi Kilise ile Batı Kilise arası taranmıştı")
S(p, "INTERP", MK, "was used as", "Manastır", "Manastır olarak kullanılan bu yapıya ait binaların kalıntıları")
S(p, "BUILT", "Manastır'a ait binaların kalıntıları", "lie (direction from Merkezi Kilise)", "kuzey",
  "Merkezi Kilise’nin kuzey ve batısında")
S(p, "BUILT", "Manastır'a ait binaların kalıntıları", "lie (direction from Merkezi Kilise)", "batı",
  "Merkezi Kilise’nin kuzey ve batısında")
S(p, "MEASURE", "Manastır'a ait binaların kalıntıları", "depth below surface (top)", "yaklaşık bir metre",
  "kalıntıları yüzeyin yaklaşık bir metre altında", h="yaklaşık")
S(p, "MEASURE", "Manastır'a ait binaların kalıntıları", "extend to depth", "1,5 metre",
  "1,5 metre derinliğe kadar uzandığı tespit edilmiştir")
S(p, "FIGURE", "Manastır'a ait binaların kalıntıları", "is shown in figure", "Resim: 1",
  "uzandığı tespit edilmiştir (Resim: 1)")
S(p, "PEOPLE", "Bülent ARIKAN", "title", "Prof. Dr.", "Prof. Dr. Bülent ARIKAN")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (university)", "İstanbul Teknik Üniversitesi",
  "Prof. Dr. Bülent ARIKAN; İstanbul Teknik Üniversitesi")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (institute)", "Avrasya Yer Bilimleri Enstitüsü",
  "Avrasya Yer Bilimleri Enstitüsü")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (department)", "Evrim ve Ekosistem ABD",
  "Evrim ve Ekosistem ABD")
S(p, "PEOPLE", "Bülent ARIKAN", "address", "Maslak, Sarıyer-İstanbul/TÜRKİYE",
  "Maslak, Sarıyer-İstanbul/TÜRKİYE")
S(p, "PEOPLE", "Bülent ARIKAN", "identifier (ORCID)", "0000-0003-2734-843X", "ORCID: 0000-0003-2734-843X")

# ---------------------------------------------------------------- page 280
p = 280
S(p, "STRUCT", "sayfa üst başlığı", "page header reads", "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ",
  "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ")
S(p, "WORK", "yer radarı çalışması (2024 sezonu)", "area scanned", "Merkezi Kilise’nin güneyi",
  "yer radarı çalışması Merkezi Kilise’nin güneyini kapsayacak şekilde gerçekleştirilmiştir")
S(p, "WORK", "yer radarı çalışması (2024 sezonu)", "was announced in", "2024 sezonu çalışma programı",
  "2024 sezonu çalışma programımızda belirttiğimiz yer radarı çalışması")
S(p, "DATE", MK, "in use from", "Erken Bizans",
  "Erken Bizans’tan başlayarak Orta Bizans Dönemi sonuna kadar kullanımda kalan")
S(p, "DATE", MK, "in use until", "Orta Bizans Dönemi sonu",
  "Erken Bizans’tan başlayarak Orta Bizans Dönemi sonuna kadar kullanımda kalan")
S(p, "WORK", "manastır yapısının çevresi", "was scanned with yer radarı", "neredeyse tamamen taranmıştır",
  "bu manastır yapısının çevresi yer radarı ile neredeyse tamamen taranmıştır", h="neredeyse")
S(p, "WORK", "arazide yapılan ön çalışmalar", "were carried out", "arazide",
  "Arazide yapılan ön çalışmalar sonucunda")
S(p, "BUILT", "Resim 1’de görülen yapılar", "continue toward", "batı",
  "yapıların batı ve güney yönlerinde de devam ettiği tespit edilmiştir")
S(p, "BUILT", "Resim 1’de görülen yapılar", "continue toward", "güney",
  "yapıların batı ve güney yönlerinde de devam ettiği tespit edilmiştir")
S(p, "FIGURE", "yapılar", "is shown in figure", "Resim 1", "Resim 1’de görülen yapıların")
S(p, "INTERP", "Manastır çevresindeki birçok mekân", "is interpreted as", "Manastır’a hizmet veren mekânlar",
  "sinde birçok mekânın da Manastır’a hizmet verdiği yer radarı sonuçlarından anlaşılmaktadır",
  h="anlaşılmaktadır")
S(p, "WORK", "yer radarı çalışmaları (2024 sezonu)", "area scanned", "Höyük düzlüğünün neredeyse tamamı",
  "Höyük düzlüğünün neredeyse tamamı taranmıştır", h="neredeyse")
S(p, "WORK", "yer radarı yöntemi", "gives sound results on sloped areas", "eğimli alanlarda sağlıklı sonuç",
  "eğimli alanlarda sağlıklı sonuç alınamaması", neg=True)
S(p, "WORK", "yer radarı", "depth of effect", "yüzeyin sadece birkaç metre altı",
  "yer radarının yüzeyin sadece birkaç metre altına etki etmesi")
S(p, "WORK", "farklı bir yöntem", "came up for use", "gündeme gelmiştir",
  "farklı bir yöntem kullanılması gündeme gelmiştir")
S(p, "WORK", "kazılar", "carried on since", "1994", "1994 yılından beri sürdürülen kazılarda")
S(p, "MEASURE", "kültür dolgusu", "thickness", "yaklaşık 12 metre",
  "yaklaşık 12 metre kültür dolgusu olduğu tespit edilen Hacımusalar Höyük", h="yaklaşık")
S(p, "WORK", "ERT çalışması", "method", "Elektrik Rezistivite (Özdirenç) Tomografi (ERT)",
  "Elektrik Rezistivite (Özdirenç) Tomografi (ERT) yönteminin kullanılmasına karar verilmiştir")
S(p, "WORK", "ERT çalışması", "aim", "kültür dolgusunun kalınlığını tespit etmek",
  "hem kültür dolgusunun kalınlığını ve kültürel-jeolojik tabaka ayrımlarını tespit etmek")
S(p, "WORK", "ERT çalışması", "aim", "kültürel-jeolojik tabaka ayrımlarını tespit etmek",
  "hem kültür dolgusunun kalınlığını ve kültürel-jeolojik tabaka ayrımlarını tespit etmek")
S(p, "WORK", "ERT çalışması", "aim", "Höyüğün tabanındaki jeolojik yapıyı açığa çıkarmak",
  "hem de Höyüğün tabanındaki jeolojik yapıyı açığa çıkarmak için")
S(p, "ADMIN", "ERT çalışması", "was paid from", "KTB ödeneği", "KTB ödeneğimizden yapılan hizmet alımıyla")
S(p, "ADMIN", "ERT çalışması", "was obtained by", "hizmet alımı", "KTB ödeneğimizden yapılan hizmet alımıyla")
S(p, "WORK", "ERT profilleri (hat)", "count", "10",
  "Höyüğün tamamını farklı yönlerden kesen 10 profil (hat) üzerinde gerçekleştirilmiştir")
S(p, "WORK", "ERT profilleri (hat)", "position", "Höyüğün tamamını farklı yönlerden kesen",
  "Höyüğün tamamını farklı yönlerden kesen 10 profil (hat)")
S(p, "FIGURE", "ERT profilleri", "is shown in figure", "Resim: 2", "(Resim: 2)")
S(p, "MEASURE", "ERT hatları", "length (range)", "yaklaşık 10 metre ile 240 metre arasında",
  "Uzunlukları yaklaşık 10 metre ile 240 metre arasında değişen hatlar", h="yaklaşık")
S(p, "WORK", "elektrodlar", "spacing", "birer metre arayla", "birer metre arayla yerleştirilen elektrodlardan")
S(p, "WORK", "ERT çalışması", "is based on", "elektrodlardan verilip alınan elektrik akımı sonuçları",
  "elektrodlardan verilip alınan elektrik akımı sonuçlarına dayanan")
S(p, "WORK", "ERT çalışması", "reached its aims", "amaçlanan tüm hedeflere ulaşılmıştır",
  "bu çalışmada yukarıda amaçlanan tüm hedeflere ulaşılmıştır")
S(p, "FIGURE", "ERT çalışmasının sonuçları", "is shown in figure", "Resim: 3",
  "ERT çalışmasının sonuçlarına göre (Resim: 3)")
S(p, "PLACE", "Hacımusalar Höyük yukarı düzlüğü", "elevation (rakım)", "yaklaşık 1081 m",
  "yaklaşık 1081 m rakımda olan", h="yaklaşık")
S(p, "WORK", "ERT kesiti", "depth scanned and mapped", "40 metrelik bir kesit",
  "yukarı düzlüğünden itibaren 40 metrelik bir kesit taranmış ve haritalanmıştır")
S(p, "BUILT", "birinci profildeki stratigrafik birimler", "count", "toplam yedi",
  "arkeolojik ve jeolojik olarak toplam yedi stratigrafik birime işaret etmektedir")
S(p, "BUILT", "elektriğe yüksek dirençli (arkeolojik) katmanlar", "extend to depth", "Höyük yüzeyinden itibaren 6 metre",
  "metre derinliğe kadar elektriğe yüksek dirençli (arkeolojik) katmanların varlığı tespit edilmiştir")
S(p, "INTERP", "elektriğe orta direnç gösteren katmanlar", "is interpreted as", "arkeolojik veya jeolojik (kil, ıslak kil, vb.)",
  "elektriğe orta direnç gösteren katmanların arkeolojik veya jeolojik (kil, ıslak kil, vb.) olabileceği",
  h="olabileceği")
S(p, "BUILT", "elektriğe orta direnç gösteren katmanlar", "lies below", "yüksek dirençli (arkeolojik) tabaka",
  "bu tabakanın altında elektriğe orta direnç gösteren katmanların")
S(p, "BUILT", "elektriğe çok düşük direnç gösteren jeolojik katmanlar (su, kil)", "begin at depth",
  "yüzeyden 15 metre derinlikten itibaren",
  "yüzeyden 15 metre derinlikten itibaren ise elektriğe çok düşük direnç gösteren jeolojik katmanların (su, kil) bulunduğu")
S(p, "BUILT", "Höyüğün Ova tabanı ile buluştuğu alanlar", "contain arkeolojik katman", "arkeolojik katman",
  "yapılan ölçümlerde herhangi bir arkeolojik katmana rastlanmamıştır", neg=True)
S(p, "MEASURE", "arkeolojik katmanlar", "reach depth", "yaklaşık olarak 11 metre",
  "laşık olarak 11 metre derinliğe kadar ulaşmakta", h="yaklaşık olarak")
S(p, "BUILT", "arkeolojik katmanların ilk altı metresi", "resistance to electricity", "çok yüksek direnç",
  "bunun ilk altı metresi elektriğe karşı çok yüksek direnç göstermektedir")
S(p, "INTERP", "0-6 metre aralığındaki arkeolojik katmanlar", "is made of", "taş gibi malzemeler",
  "ların taş gibi malzemelerden oluşması beklenmektedir", h="beklenmektedir")
S(p, "INTERP", "6-12 metre arasındaki katmanlar", "nature determined", "niteliği",
  "niteliği elektriğe gösterdikleri orta direnç nedeniyle tam belirlenememiştir", neg=True)
S(p, "INTERP", "6-12 metre arasındaki katmanlar", "is interpreted as",
  "arkeolojik (kerpiç, vb.) ve jeolojik (ıslak kil, vb.) olguların birlikte bulunduğu seviyeler",
  "hem arkeolojik (kerpiç, vb.) hem de jeolojik (ıslak kil, vb.) olguların birlikte",
  h="olabileceği değerlendirilmektedir")
S(p, "INTERP", "yüzeyden 12 metre derinlikten sonraki katmanlar", "contain arkeolojik katman", "arkeolojik katmanlar",
  "Yüzeyden 12 metre derinlikten itibaren elektriğe çok düşük dirençli katmanların (su, kil) varlığı nedeniyle",
  h="düşünülmektedir", neg=True)

# ---------------------------------------------------------------- page 281
p = 281
S(p, "INTERP", "sağlam ele geçirilebilecek arkeolojik katmanlar", "depth below surface", "8-9 metre",
  "ele geçirilebilecek arkeolojik katmanların yüzeyden 8-9 metre derinlikte olabileceği", h="olabileceği")
S(p, "INTERP", "8-9 metreden sonra bulunacak arkeolojik katmanların korunması", "is judged as", "sorunlu",
  "korunmasının alttaki ıslak jeolojik yapı nedeniyle sorunlu olabileceği", h="sorunlu olabileceği")
S(p, "INTERP", "yüzeyin 12 metre altından itibaren", "contains only",
  "su kaynağı ve bununla ilişkili jeolojik katmanlar",
  "sadece su kaynağı ve bununla ilişkili jeolojik katmanların bulunabileceği", h="bulunabileceği")
S(p, "DATE", "Hacımusalar Höyüğün ilk yerleşildiği dönem", "is dated to (period)", "Geç Kalkolitik Dönem",
  "şu andaki bulgulara dayanarak Geç Kalkolitik Dönem’de", h="şu andaki bulgulara dayanarak")
S(p, "DATE", "Geç Kalkolitik Dönem", "is dated to (year)", "y. MÖ 3500", "(y. MÖ 3500)", h="y.")
S(p, "INTERP", "ilk yerleşimde konum tercihi", "is interpreted as", "su kaynağı yakınında olma isteği",
  "su kaynağı yakınında olma isteğine dayandırılabileceğini göstermektedir", h="dayandırılabileceğini")
S(p, "WORK", "paleo-coğrafya çalışmaları", "planned for", "önümüzdeki yıllar",
  "Önümüzdeki yıllarda, Elmalı Ovası genelinde yürütülecek paleo-coğrafya çalışmalarında")
S(p, "WORK", "paleo-coğrafya çalışmaları", "planned area", "Elmalı Ovası geneli",
  "Elmalı Ovası genelinde yürütülecek paleo-coğrafya çalışmalarında")
S(p, "WORK", "paleo-coğrafya çalışmaları", "expected result",
  "Höyüğün iskân gördüğü dönemlerde su tablasının ne kadar yüksek olduğu",
  "Höyüğün iskân gördüğü dönemlerde su tablasının ne kadar yüksek olduğu", h="açıklığa kavuşacaktır")
S(p, "WORK", "paleo-coğrafya çalışmaları", "expected result",
  "göllerin arkeolojik dönemlerde Höyük ile olan ilişkileri",
  "kurutulan göllerin arkeolojik dönemlerde Höyük ile olan ilişkileri açıklığa kavuşacaktır",
  h="açıklığa kavuşacaktır")
S(p, "PLACE", "göller", "is located", "Höyük civarında", "Höyük civarındaki göllerin")
S(p, "HISTORY", "göller", "were drained in", "1970’ler", "1970’lerde kurutulan göllerin")
S(p, "FIGURE", "birinci ERT hattı", "is shown in figure", "Resim 3b", "Resim 3b’de gösterilen birinci ERT hattının")
S(p, "BUILT", "1 No.lu katman", "position on birinci ERT hattı", "20. ve 40. metreleri arasında",
  "birinci ERT hattının 20. ve 40. metreleri arasında")
S(p, "BUILT", "1 No.lu katman", "resistance to electricity", "çok yüksek direnç",
  "çok yüksek direnç gösteren 1 No.lu katman işaretlenmiştir")
S(p, "WORK", "sondajlar", "took place at", "Güney Yamaç", "Güney Yamaç’ta yapılan sondajlardan")
S(p, "WORK", "sondajlar (Güney Yamaç)", "took place in", "önceki kazı dönemleri",
  "Höyük’te önceki kazı dönemlerinde Güney Yamaç’ta yapılan sondajlardan")
S(p, "BUILT", "duvarlar (Güney Yamaç)", "position", "birinci ERT hattının hemen batısında ve doğusunda",
  "bu hattın hemen batısında ve doğusunda")
S(p, "BUILT", "duvarlar (Güney Yamaç)", "is made of", "kireçtaşı", "miş kireçtaşından duvarlar")
S(p, "BUILT", "duvarlar (Güney Yamaç)", "workmanship", "poligonal şekilde işlenerek yüzeyi düzeltilmiş",
  "poligonal şekilde işlenerek yüzeyi düzeltilmiş kireçtaşından duvarlar")
S(p, "DATE", "duvarlar (Güney Yamaç)", "is dated to", "Helenistik/Roma dönemleri",
  "Helenistik/Roma dönemlerine ait olabilecek", h="ait olabilecek")
S(p, "BUILT", "duvar blokları (Güney Yamaç)", "shape", "dikdörtgen prizma",
  "dikdörtgen prizma şeklinde duvar blokları tespit edilmiştir")
S(p, "WORK", "Güney Yamaç’taki açma (2023 sezonu)", "exposed", "duvarın bir kısmı daha",
  "2023 sezonunda Güney Yamaç’taki açmada bu duvarın bir kısmı daha açığa çıkarılmıştır")
S(p, "BUILT", "savunma sistemi", "position", "Höyüğün güney yamacını doğudan batıya çevreleyen",
  "Höyüğün güney yamacını doğudan batıya çevreleyen")
S(p, "DATE", "savunma sistemi", "is dated to", "Helenistik/Roma dönemleri",
  "üslubu açısından Helenistik/Roma dönemlerine tarihlenebilecek bir savunma sisteminin",
  h="tarihlenebilecek")
S(p, "DATE", "savunma sistemi", "dating is based on", "yapı üslubu",
  "üslubu açısından Helenistik/Roma dönemlerine tarihlenebilecek")
S(p, "MEASURE", "savunma sistemi", "extends north from güney yamaç (length)", "20 metre daha",
  "bu sistemin Höyüğün güney yamacından kuzeye doğru 20 metre daha uzandığı tespit edilmiştir")
S(p, "PLACE", "savunma sisteminin uzandığı alan", "is", "Höyüğün en düşük kotta olduğu nokta",
  "Bu alan, Höyüğün en düşük kotta olduğu")
S(p, "PLACE", "savunma sisteminin uzandığı alan", "is", "yaya olarak Höyüğün yukarı düzlüğüne rahatça ulaşılabilecek nokta",
  "yaya olarak Höyüğün yukarı düzlüğüne rahatça ulaşılabilecek noktadır")
S(p, "PLACE", "Höyüğün üstüne çıkmak için kullanılan yol", "is located in", "bu alan (güney yamaç)",
  "ğün üstüne çıkmak için kullanılan yol burada yer almaktadır")
S(p, "PLACE", "Höyüğün güney kısmı", "topography", "yükselen bir topografya",
  "Höyüğün güney kısmında yükselen bir topografya karşımıza çıkmaktadır")
S(p, "INTERP", "Hacımusalar Höyüğün güney yamacındaki yapı", "is interpreted as", "giriş alanı veya anıtsal kapı yapısı",
  "alanı veya anıtsal kapı yapısının bulunabileceğini düşündürmektedir",
  h="bulunabileceğini düşündürmektedir")
S(p, "MEASURE", "giriş alanı veya anıtsal kapı yapısı", "measures (length)", "yaklaşık 20 metre",
  "yamacında yaklaşık 20 metre uzunluğa sahip", h="yaklaşık")
S(p, "INTERP", "giriş alanı veya anıtsal kapı yapısı", "is made of", "taş malzeme",
  "olasılıkla taş malzemeden oluşan bir giriş", h="olasılıkla")
S(p, "INTERP", "giriş alanı / anıtsal kapı yorumu", "is based on",
  "Höyük topografyası, Helenistik/Roma Dönemi savunma sistemi ve ERT verisi",
  "savunma sistemi, ERT verisi ile birlikte değerlendirildiğinde")
S(p, "WORK", "çift yöntemli jeofizik", "methods", "yer radarı ve yer manyetik ölçümleri",
  "yöntemli jeofizik (yer radarı ve yer manyetik ölçümleri) hizmeti alınmıştır")
S(p, "ADMIN", "çift yöntemli jeofizik", "was obtained by", "hizmet alımı",
  "yöntemli jeofizik (yer radarı ve yer manyetik ölçümleri) hizmeti alınmıştır")
S(p, "WORK", "çift yöntemli jeofizik", "took place after", "ERT çalışması",
  "ERT çalışması sonrasında yapılan değerlendirmelerde")
S(p, "WORK", "çift yöntemli jeofizik", "area", "güney yamacın batısındaki yükseltinin ardı, Höyük yukarı düzlüğüne doğru inildiği nokta",
  "Höyük yukarı düzlüğüne doğru inildiği noktada")
S(p, "WORK", "çift yöntemli jeofizik", "aim", "herhangi bir yapı bulunup bulunmadığına ilişkin soruları cevaplandırmak",
  "herhangi bir yapı bulunup bulunmadığına ilişkin sorular cevaplandırmak için")
S(p, "INTERP", "taranan alan", "position", "anıtsal girişin ardında", "olasılıkla anıtsal girişin", h="olasılıkla")
S(p, "MEASURE", "taranan alan", "area (unclear: text reads 'yaklaşım 2000 m2')", "2000 m2",
  "çilen yaklaşım 2000 m2 alanın eğimli bir topografyaya sahip olması nedeniyle")
S(p, "PLACE", "taranan alan", "topography", "eğimli", "alanın eğimli bir topografyaya sahip olması nedeniyle")
S(p, "WORK", "iki yöntemin birlikte kullanılması", "reason", "farklı yapı malzemelerinin tanınabilmesi",
  "yapı malzemelerinin tanınabilmesi amacıyla bu iki yöntemin birlikte kullanılması tercih")
S(p, "BUILT", "arkeolojik yapı kalıntıları (taranan alan)", "begin at depth", "yüzeyin 0.5 metre altından itibaren",
  "yüzeyin 0.5 metre altından itibaren plan")
S(p, "BUILT", "arkeolojik yapı kalıntıları (taranan alan)", "give a plan", "plan veren",
  "arkeolojik yapı kalıntılarına rastlanmıştır")
S(p, "INTERP", "yapılardan bazıları (taranan alan)", "is interpreted as",
  "fırın veya ocak gibi yoğun ateş kullanımı gösteren mekanlar",
  "veya ocak gibi yoğun ateş kullanımı gösteren mekanlar olabileceği değerlendirilmiştir",
  h="olabileceği değerlendirilmiştir")
S(p, "INTERP", "fırın veya ocak yorumu", "is based on", "yer manyetik yöntem sonuçları",
  "tılarının yer manyetik yöntemle tarandığında verdiği sonuçlar")

# ---------------------------------------------------------------- page 282
p = 282
S(p, "STRUCT", "başlık", "heading reads", "4- ARKEOLOJİK KAZILAR:", "4- ARKEOLOJİK KAZILAR:")
S(p, "WORK", "arkeolojik kazı çalışmaları (2024)", "took place at", "Kuzey Yamaç alanı",
  "zey Yamaç alanında beş arkeolog")
S(p, "WORK", "Kuzey Yamaç kazısı", "took place between", "16.07.2024–26.08.2024",
  "16.07.2024–26.08.2024 tarihleri arasında gerçekleştirilmiştir")
S(p, "PEOPLE", "Kuzey Yamaç kazısı: arkeolog", "count", "beş", "beş arkeolog, öğrenciler")
S(p, "PEOPLE", "Kuzey Yamaç kazısı: öğrenciler", "took part", "öğrenciler", "beş arkeolog, öğrenciler")
S(p, "ADMIN", "Kuzey Yamaç kazısı: işçi", "count", "iki", "TYP bünyesinde çalıştırılan iki işçi")
S(p, "ADMIN", "Kuzey Yamaç kazısı: işçiler", "employed under", "TYP", "TYP bünyesinde çalıştırılan iki işçi")
S(p, "MEASURE", "Merkezi Kilise 1. Etap kazı alanı", "area", "333 m2", "Merkezi Kilise 1. Etap 333 m2 alanda")
S(p, "WORK", "Merkezi Kilise 1. Etap kazısı", "hafriyat removed", "120 m3", "120 m3 hafriyat kaldırılan arkeolojik kazı")
S(p, "ADMIN", "Merkezi Kilise 1. Etap kazısı", "carried out under", "GMP", "GMP bünyesinde iki arkeolog")
S(p, "PEOPLE", "Merkezi Kilise 1. Etap kazısı: arkeolog", "count", "iki", "iki arkeolog, bir mimar ve altı işçinin katılımıyla")
S(p, "PEOPLE", "Merkezi Kilise 1. Etap kazısı: mimar", "count", "bir", "iki arkeolog, bir mimar ve altı işçinin katılımıyla")
S(p, "ADMIN", "Merkezi Kilise 1. Etap kazısı: işçi", "count", "altı", "iki arkeolog, bir mimar ve altı işçinin katılımıyla")
S(p, "WORK", "Merkezi Kilise 1. Etap kazısı", "took place between", "29.08.2024–27.09.2024",
  "29.08.2024–27.09.2024 tarihleri arasında")
S(p, "STRUCT", "başlık", "heading reads", "4.1 KUZEY YAMAÇ", "4.1 KUZEY YAMAÇ")
S(p, "PLACE", "P2 noktası", "is located in", "Kuzey Yamaç alanı", "Bu alandaki P2 noktasında")
S(p, "PLACE", "P2 noktası (Höyük yüzeyi)", "elevation (kot)", "1055.37 m",
  "P2 noktasında Höyük yüzeyi 1055.37 m kottadır")
S(p, "BUILT", "Demir Çağı sur duvarı", "is located in", "C4a8 açması", "Önceki sezonlarda C4a8")
S(p, "BUILT", "Demir Çağı sur duvarı", "is made of", "kerpiç", "taş temel üzerinde kerpiçle inşa edilen Demir Çağı sur")
S(p, "BUILT", "Demir Çağı sur duvarı", "foundation is made of", "taş", "taş temel üzerinde kerpiçle inşa edilen Demir Çağı sur")
S(p, "DATE", "sur duvarı", "is dated to", "Demir Çağı", "kerpiçle inşa edilen Demir Çağı sur")
S(p, "WORK", "Demir Çağı sur duvarı", "was removed along", "beş metrelik bir hat",
  "duvarı beş metrelik bir hat boyunca kaldırılmış")
S(p, "WORK", "C4a8 açmasındaki çalışmalar", "took place in", "önceki sezonlar", "Önceki sezonlarda C4a8")
S(p, "BUILT", "ETÇ yapı kalıntıları (C4a8)", "lies below", "Demir Çağı sur duvarı",
  "bunun altında yapılan kazılarda Erken")
S(p, "DATE", "yapı kalıntıları (C4a8)", "is dated to", "Erken Tunç Çağı (ETÇ)",
  "Tunç Çağı’na (ETÇ) ait yapı kalıntılarına")
S(p, "PLACE", "ETÇ yapı kalıntıları (C4a8)", "elevation (kot)", "yaklaşık 1049 m", "(yaklaşık 1049 m kotta)",
  h="yaklaşık")
S(p, "MEASURE", "ETÇ yapı kalıntılarına ulaşılan alan", "measures", "2x2 metre",
  "çok dar bir alanda (2x2 metre) ulaşılmıştır")
S(p, "WORK", "Kuzey Yamaç’ta açılan açmalar (1994’ten beri)", "count", "bir düzineden fazla",
  "Kuzey Yamaç’ta açılan bir düzineden fazla açmada")
S(p, "WORK", "Kuzey Yamaç açmaları", "opened since", "1994", "1994 yılından beri Kuzey Yamaç’ta açılan")
S(p, "WORK", "Kuzey Yamaç açmaları", "reached ETÇ seviyeleri", "ETÇ seviyeleri",
  "yeterince derinleşilmediğinden ETÇ seviyelerine inilememiştir", neg=True)
S(p, "WORK", "ETÇ seviyelerine inilememesi", "reason", "yeterince derinleşilmediğinden",
  "yeterince derinleşilmediğinden ETÇ seviyelerine inilememiştir")
S(p, "WORK", "C4a7-C4b7 açmaları", "were started in", "2023 sezonu", "2023 sezonunda başlatılan C4a7-C4b7 açmalarında")
S(p, "WORK", "Kuzey Yamaç kazıları (2024 sezonundan itibaren)", "aim", "C4a7-C4b7 açmalarında derinleşerek ETÇ seviyelerine doğru devam etmek",
  "leşerek ETÇ seviyelerine doğru devam ederken")
S(p, "PLACE", "C5b1 ve C5b2 açmaları", "level left at", "en yüksek kot", "en yüksek kotta bırakılan C5b1 ve C5b2")
S(p, "WORK", "Kuzey Yamaç kazıları (2024 sezonundan itibaren)", "aim",
  "C5b1 ve C5b2 açmalarını C4b10 ve C4c10 açmalarının bulunduğu kotlara indirmek",
  "açmalarında derinleşerek bunları C4b10 ve C4c10 açmalarının bulunduğu kotlara")
S(p, "WORK", "yedi açma (C4b9 ile birlikte)", "planned to be lowered to", "C4b8 seviyesi",
  "Yakın gelecekte C4b9 ile birlikte, yedi açmanın tamamı, C4b8 seviyesine", h="Yakın gelecekte")
S(p, "INTERP", "C4a8 açmasındaki ETÇ katlarının devamı", "expected depth below current level of C4b8", "yaklaşık 1.5 metre aşağıda",
  "C4b8 açmasının şu anki seviyesinden yaklaşık 1.5 metre aşağıda C4a8 açmasındaki",
  h="değerlendirilmektedir")
S(p, "FIGURE", "Kuzey Yamaç açmaları", "is shown in figure", "Resim: 4", "(Resim: 4)")
S(p, "PLACE", "C4a7-C4b7 açmaları", "is located in", "Kuzey Yamaç", "Kuzey Yamaç’ta 2023 sezonunda açılan C4a7-C4b7 açmalarında")
S(p, "WORK", "C4a7-C4b7 kazısı (2024)", "began with removal of", "dağınık duvar kalıntısı",
  "belgelenen dağınık duvar kalıntısı ve çöp çukurunun")
S(p, "WORK", "C4a7-C4b7 kazısı (2024)", "began with removal of", "çöp çukuru",
  "belgelenen dağınık duvar kalıntısı ve çöp çukurunun")
S(p, "WORK", "dağınık duvar kalıntısı ve çöp çukuru (C4a7-C4b7)", "were found and documented in", "2023 sezonu",
  "sezonunda tespit edilen, belgelenen dağınık duvar kalıntısı")
S(p, "WORK", "C4b7 açması", "was extended", "güneyine doğru 30 cm",
  "açmanın C4b7’nin güneyine doğru 30 cm genişletilmesine karar verilmiş")
S(p, "BUILT", "duvar (C4b7 güney genişletmesi)", "kind", "duvar", "yüksekliğinde bir duvar 4.3 metre uzunlukta yakalanmıştır")
S(p, "BUILT", "duvar (C4b7 güney genişletmesi)", "condition", "oldukça düzgün", "burada oldukça düzgün, iki sıra genişliğinde")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (width)", "iki sıra", "iki sıra genişliğinde tek sıra")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (height)", "tek sıra", "iki sıra genişliğinde tek sıra")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (length)", "4.3 metre", "bir duvar 4.3 metre uzunlukta yakalanmıştır")
S(p, "MEASURE", "C4a7-C4b7 alanı (genişleme sonrası)", "measures", "5x8 metre",
  "redeyse 5x8 metre boyutlarına gelen bu alan", h="neredeyse")
S(p, "WORK", "kazı (2024)", "was limited to", "sadece C4a7", "sadece C4a7 içinde (5x5 m) kazı yapılmıştır")
S(p, "MEASURE", "C4a7 açması", "measures", "5x5 m", "sadece C4a7 içinde (5x5 m) kazı yapılmıştır")
S(p, "WORK", "sadece C4a7 içinde kazı yapılması", "reason", "iş gücü ve zamandan tasarruf etmek",
  "iş gücü ve zamandan tasarruf etmek")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "kind", "kerpiç dolgu", "kadar uzayan kerpiç dolgu")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "condition", "oldukça sert", "2023 yılında bu açmada oldukça")
S(p, "INTERP", "kerpiç dolgu (C4a7)", "is interpreted as", "Demir Çağı sur duvarından dökülmüş",
  "sert, Demir Çağı sur duvarından döküldüğü değerlendirilen", h="değerlendirilen")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "extends to", "C4b7 açma sınırı",
  "rına kadar uzayan kerpiç dolgu", h="neredeyse")
S(p, "WORK", "kerpiç dolgunun kazısı", "was started in", "2023", "2023 yılında bu açmada oldukça")
S(p, "WORK", "kerpiç dolgunun kaldırılması", "continued in", "2024 sezonu",
  "zılarda kerpiç dolgunun kaldırılması işlemine devam edilmiştir")
S(p, "MEASURE", "C4a7 kazısı (2024)", "depth excavated", "yaklaşık 1.3 metre", "1.3 metre derinleşilmiş olup",
  h="yaklaşık")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "continues", "dağınık halde",
  "kerpiç dolgunun dağınık halde devam ettiği gözlemlenmiştir")
S(p, "MEASURE", "Demir Çağı sur duvarı", "measures (width)", "3 metreyi aşkın",
  "Demir Çağı sur duvarının genişliğinin 3 metreyi aşkın olduğu düşünüldüğünde")
S(p, "INTERP", "kerpiç üst yapı (sur duvarı üzerindeki)", "is interpreted as", "duvarın iç kısmına (güneyine) yıkılmış",
  "kerpiç üst yapının duvarın iç kısmına (güneyine) yıkıldığı düşünülmektedir", h="düşünülmektedir")
S(p, "INTERP", "C4a7 açmasında kazılacak kerpiç duvar enkazı", "expected further depth", "yaklaşık 1.5 metre daha",
  "C4a7 açmasında yaklaşık 1.5 metre daha kerpiç duvar enkazı kazılacağı", h="düşünülmektedir")
S(p, "FIND", "iyi korunmuş kerpiç parçası (kerpiç üst yapı enkazı)", "was found", "iyi korunmuş bir kerpiç parçası",
  "iyi korunmuş bir kerpiç parçasının", neg=True)
S(p, "WORK", "sondaj", "took place in", "C4a6 açması", "C4a6 açmasına kuzeybatı açma sınırından")
S(p, "WORK", "sondaj (C4a6)", "position", "kuzeybatı açma sınırından", "C4a6 açmasına kuzeybatı açma sınırından")
S(p, "MEASURE", "sondaj (C4a6)", "measures (length)", "2 metre", "sınırından 2 metre uzunluğunda")
S(p, "MEASURE", "sondaj (C4a6)", "measures (width)", "1 metre", "genişliğinde bir sondaj açılmıştır")
S(p, "WORK", "sondaj (C4a6)", "aim", "kerpiç üst yapı enkazının uzantısının tespit edilebilmesi",
  "aynı zamanda kerpiç üst yapı enkazının uzantısının tespit")

# ---------------------------------------------------------------- page 283
p = 283
S(p, "FIND", "kayda değer buluntu (C4a6 sondajı)", "was found", "kayda değer bir buluntu",
  "ele geçmemesine karşın iki unsur gözlemlenmiştir", neg=True)
S(p, "WORK", "C4a6 sondajı", "elements observed (count)", "iki unsur", "iki unsur gözlemlenmiştir")
S(p, "FIND", "kerpiç blok", "kind", "kerpiç blok", "cm olan bir kerpiç blok in situ")
S(p, "FIND", "kerpiç blok", "count", "bir", "cm olan bir kerpiç blok in situ")
S(p, "FIND", "kerpiç blok", "measures (unclear: text 35x3x12 cm, caption of Resim 5 gives 35x35x12 cm)", "35x3x12 cm",
  "yaklaşık boyutları 35x3x12", h="yaklaşık")
S(p, "FIND", "kerpiç blok", "position", "in situ (yerinde)", "bir kerpiç blok in situ (yerinde)")
S(p, "FIND", "kerpiç blok", "condition", "iyi korunmuş", "in situ (yerinde) ve iyi korunmuş olarak")
S(p, "FIND", "kerpiç blok", "depth below surface", "yaklaşık 1 metre", "yüzeyin yaklaşık 1 metre",
  h="yaklaşık")
S(p, "FIND", "kerpiç blok", "was found in", "C4a6’daki sondaj", "C4a6’daki sondajda sürdürülen kazı çalışmaları")
S(p, "FIGURE", "kerpiç blok", "is shown in figure", "Resim: 5", "altında tespit edilmiştir (Resim: 5)")
S(p, "FIND", "öküze ait kafatası", "kind", "kafatası", "durumda bir öküze ait kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "kafatası", "belongs to animal", "öküz", "durumda bir öküze ait kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "öküze ait kafatası", "was found in", "C4a6’daki sondaj", "C4a6’daki sondajda sürdürülen kazı çalışmaları")
S(p, "FIND", "öküze ait kafatası", "position (horizontal)", "kerpiç bloğun yaklaşık bir metre doğusunda",
  "bu kerpiç bloğun yaklaşık bir metre doğusunda", h="yaklaşık")
S(p, "FIND", "öküze ait kafatası", "position (vertical)", "kerpiç bloğun birkaç santimetre altında",
  "doğusunda ve birkaç santimetre altında in situ")
S(p, "FIND", "öküze ait kafatası", "position", "in situ", "birkaç santimetre altında in situ")
S(p, "FIND", "boynuz", "kind", "boynuz", "kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "boynuz", "count", "bir", "kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "boynuz", "was found with", "öküze ait kafatası", "kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "boynuz", "was found in", "C4a6’daki sondaj", "C4a6’daki sondajda sürdürülen kazı çalışmaları")
S(p, "DATE", "kerpiç üst yapı enkazı (C4a7)", "is dated to", "Demir Çağı",
  "C4a7 açmasında sürdürülen kazı çalışmalarında Demir Çağı’na ait kerpiç üst yapı")
S(p, "BUILT", "kerpiç üst yapı enkazı (C4a7)", "is cut by", "üç çöp çukuru",
  "üç çöp çukuru tarafından kesildiği tespit edilmiştir")
S(p, "BUILT", "çöp çukurları (C4a7)", "count", "üç", "üç çöp çukuru tarafından kesildiği tespit edilmiştir")
S(p, "DATE", "çöp çukurları (C4a7)", "is dated relative to kerpiç üst yapı enkazı", "daha sonraki dönemler",
  "kazının kaldırılmasına devam edilmiş ve bu enkazın daha sonraki dönemlerde")
S(p, "FIGURE", "çöp çukurları (C4a7)", "is shown in figure", "Resim: 6", "kesildiği tespit edilmiştir (Resim: 6)")
S(p, "INTERP", "çöp çukurlarının ikisi (C4a7)", "is compared to", "Kuzey Yamaç’ta daha önceki kazılarda açığa çıkarılanlar",
  "ikisi, Kuzey Yamaç’ta daha önceki kazılarda açığa çıkarılanlarla benzerdir")
S(p, "MEASURE", "çöp çukurları (C4a7)", "measures (diameter)", "bir metreyi aşmakta", "rının çapı bir metreyi aşmakta")
S(p, "BUILT", "çöp çukurları (C4a7)", "fill", "küllü ve kireçli dolgu", "içindeki küllü ve kireçli dolgudan")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "kind", "seramik parçaları",
  "ve vermeyen Demir Çağı seramik parçaları")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "count", "çok sayıda", "dolgudan çok sayıda profile veren")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "condition", "profile veren ve vermeyen",
  "çok sayıda profile veren ve vermeyen Demir Çağı seramik parçaları")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "period", "Demir Çağı", "ve vermeyen Demir Çağı seramik parçaları")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının küllü ve kireçli dolgusu",
  "içindeki küllü ve kireçli dolgudan")
S(p, "FIND", "insan kemiği parçaları (C4a7 çöp çukurları)", "kind", "insan kemiği parçaları",
  "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "FIND", "insan kemiği parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının küllü ve kireçli dolgusu",
  "içindeki küllü ve kireçli dolgudan")
S(p, "FIND", "hayvan kemiği parçaları (C4a7 çöp çukurları)", "kind", "hayvan kemiği parçaları",
  "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "FIND", "hayvan kemiği parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının küllü ve kireçli dolgusu",
  "içindeki küllü ve kireçli dolgudan")
S(p, "BUILT", "çöp çukurlarından birisi (C4a7)", "floor", "kireç kaplı taban",
  "Çöp çukurlarından birisi, genel kurala uygun olarak kireç kaplı tabana sahipken")
S(p, "INTERP", "kireç kaplı taban", "is compared to", "genel kural", "genel kurala uygun olarak kireç kaplı tabana")
S(p, "WORK", "çöp çukuru (çakıl taşı tabanlı, C4a7)", "part excavated", "sadece kuzey yarısı",
  "sadece kuzey yarısı kazılan çöp çukurunun")
S(p, "BUILT", "çöp çukuru (kuzey yarısı kazılan, C4a7)", "floor", "çakıl taşı kaplama",
  "çöp çukurunun tabanında çakıl taşı kaplama tespit edilmiştir")
S(p, "MEASURE", "çöp çukurları (C4a7): en derini", "measures (depth)", "bir metre", "en derini bir metre en sığ olanı ise")
S(p, "MEASURE", "çöp çukurları (C4a7): en sığ olanı", "measures (depth)", "10 santimetre", "10 santimetre derinliğe sahiptir")
S(p, "FIND", "at figürinleri (C4a7)", "kind", "at figürini", "ele geçen at figürinlerinden bulunmuştur")
S(p, "FIND", "at figürinleri (C4a7)", "was found in", "C4a7 açması, kerpiç üst yapı enkazı",
  "C4a7 açmasında kerpiç üst yapı enkazının kazısı sırasında")
S(p, "INTERP", "at figürinleri (C4a7)", "is compared to", "daha önceki yıllarda Kuzey Yamaç kazılarında tüm veya parça halinde ele geçen at figürinleri",
  "Yamaç kazılarında tüm veya parça halinde ele geçen at figürinlerinden bulunmuştur")
S(p, "FIND", "at figürinleri (C4a7)", "parts preserved", "baş veya gövde kısımları",
  "figürinlerin baş veya gövde kısımlarının olduğu")
S(p, "FIND", "at figürinleri (C4a7): gövdeler", "condition", "ayak veya baş kısımları kopartılmış/kopmuş",
  "gövdelerin ayak veya baş kısımlarının kopartılmış/kopmuş olduğu")
S(p, "FIND", "at figürinleri (C4a7): baş kısımları", "workmanship", "detaylı olarak işlenmiş",
  "ele geçen figürinlerin baş kısımlarının detaylı olarak işlendiği")
S(p, "FIND", "at figürinleri (C4a7): baş kısımları", "surface treatment", "boyanmış", "ve olasılıkla boyandığı gözlemlenmiştir",
  h="olasılıkla")
S(p, "WORK", "C5b1-C5b2 açmaları", "excavated so far", "bu alanda en az kazılmış olan",
  "Kuzey Yamaç açmalarındaki kazı çalışmaları, bu alanda en az kazılmış olan")
S(p, "PLACE", "C5b1-C5b2 açmaları", "position", "Kuzey Yamaç alanının en doğusundaki açmalar",
  "Bu açmalar, Kuzey Yamaç alanının en doğusundaki")
S(p, "DESCR", "C5b1-C5b2 açmalarında derinleşilmesi", "is judged as", "ETÇ tabakalarının daha geniş bir alanda açığa çıkarılması açısından önemli",
  "bir alanda açığa çıkarılması açısından önemlidir")
S(p, "PLACE", "poligon noktası", "elevation (kot)", "1055.31 m", "1055.31 m kottaki poligon noktasından")
S(p, "PLACE", "C5b1-C5b2 açmaları (2024 sezonu başında)", "level below poligon noktası", "yaklaşık bir metre aşağıda",
  "1055.31 m kottaki poligon noktasından yaklaşık bir metre", h="yaklaşık")
S(p, "WORK", "C5b1 ve C5b2 kazıları (2024)", "started from", "Locus 70",
  "Her iki açmada da 2024 kazıları Locus 70’den başlatılmıştır")
S(p, "BUILT", "çöp çukuru (C5b1)", "kind", "çöp çukuru", "ve dairesel formda bir çöp çukurunun kazıldığı anlaşılmaktadır")
S(p, "BUILT", "çöp çukuru (C5b1)", "shape", "dairesel form", "ve dairesel formda bir çöp çukurunun kazıldığı anlaşılmaktadır")
S(p, "MEASURE", "çöp çukuru (C5b1)", "measures (diameter)", "yaklaşık 3 metre", "oldukça geniş (yaklaşık 3 metre",
  h="yaklaşık")
S(p, "WORK", "çöp çukuru (C5b1)", "was excavated at", "açmanın son kazısının yapıldığı tarih",
  "açmanın son kazısının yapıldığı tarihte", h="anlaşılmaktadır")
S(p, "FIGURE", "çöp çukuru (C5b1)", "is shown in figure", "Resim: 7", "kazıldığı anlaşılmaktadır (Resim: 7)")
S(p, "BUILT", "çöp çukuru (C5b1)", "condition", "zamanla formunu kaybetmiş", "çukurun zamanla formunu kaybettiği açmada")
S(p, "WORK", "C5b1 açması", "step", "çukurun etrafı taban seviyesine indirilerek açma içindeki seviye eşitlendi",
  "çukurun etrafı taban seviyesine indirilerek")
S(p, "WORK", "C5b1 açması", "step", "tüm karenin kazılmasına devam edilmiştir",
  "C5b1 açmasında tüm karenin kazılmasına devam")
S(p, "WORK", "C5b2 açması kazısı", "took place at the same time as", "C5b1 açması kazısı",
  "Bununla eş zamanda, C5b2 açmasının kazısı yürütülmüş")
S(p, "WORK", "rampa (toprak tahliyesi için)", "count", "iki",
  "C5b1 açmasından toprak tahliyesi için iki rampa hazırlanmıştır")
S(p, "FIND", "seramik parçaları (C5b1 ve C5b2)", "kind", "seramik parçaları",
  "ETÇ-Demir Çağı arasında dağılım gösteren seramik parçaları")
S(p, "FIND", "seramik parçaları (C5b1 ve C5b2)", "period", "ETÇ-Demir Çağı arasında dağılım gösteren",
  "ETÇ-Demir Çağı arasında dağılım gösteren seramik parçaları")
S(p, "FIND", "seramik parçaları (C5b1 ve C5b2)", "was found in", "C5b1 ve C5b2 açmaları",
  "Her iki açmada da derin")
S(p, "BUILT", "duvarlar (C5b1 ve C5b2)", "kind", "basit duvarlar", "orta boy taşlardan oluşan duvarlar tespit edilmiştir")
S(p, "BUILT", "duvarlar (C5b1 ve C5b2)", "is made of", "orta boy taşlar", "orta boy taşlardan oluşan duvarlar tespit edilmiştir")
S(p, "MEASURE", "duvarlar (C5b1 ve C5b2)", "measures (width)", "iki sıra", "basit (iki sıra genişliğinde ve birkaç sıra")
S(p, "MEASURE", "duvarlar (C5b1 ve C5b2)", "measures (height)", "birkaç sıra", "basit (iki sıra genişliğinde ve birkaç sıra")
S(p, "DATE", "duvarlar (C5b1 ve C5b2)", "is dated to", "Demir Çağı", "Kuzey Yamaç’ta Demir Çağı’na tarihlenen basit")
S(p, "BUILT", "duvarlar (C5b1 ve C5b2)", "give a plan", "belirgin bir plan", "Bu duvarlar belirgin", neg=True)
S(p, "WORK", "duvarlar (C5b1 ve C5b2)", "were documented by", "fotoğraflanarak",
  "kazı ekibi tarafından fotoğraflanarak kaldırılmıştır")
S(p, "WORK", "duvarlar (C5b1 ve C5b2)", "were removed by", "kazı ekibi",
  "kazı ekibi tarafından fotoğraflanarak kaldırılmıştır")
S(p, "PLACE", "C4c10 açması", "position", "bu açma grubunun (C5b1-C5b2) batısında",
  "açma grubunun batısında kalan C4c10 açmasının kesitine bakıldığında")
S(p, "INTERP", "duvarların benzerleri", "were found and removed in", "önceki sezonlarda yapılan kazı çalışmaları",
  "benzerlerinin önceki sezonlarda yapılan kazı çalışmalarında da tespit edildiği", h="anlaşılmaktadır")
S(p, "INTERP", "duvarların benzerleri", "is based on", "C4c10 açmasının kesiti",
  "C4c10 açmasının kesitine bakıldığında")

# ---------------------------------------------------------------- page 284
p = 284
S(p, "BUILT", "çöp çukurları (C5b1 ve C5b2, kazılan)", "count", "iki", "çöp çukurlarından ikisi kazılmış olup")
S(p, "MEASURE", "çöp çukurları (C5b1 ve C5b2, kazılan)", "size compared to other pits", "daha küçük",
  "bunlar alandaki diğer çöp çukurlarına kıyasla daha")
S(p, "BUILT", "çöp çukurları (C5b1 ve C5b2, kazılan)", "floor", "kireç sıvalı",
  "tabanlarının kireç sıvalı olduğu dikkat çekmiştir")
S(p, "FIND", "kırık seramik parçaları (C5b1-C5b2 çöp çukurları)", "kind", "kırık seramik parçaları",
  "bunlar da kırık seramik parçaları ve hayvan kemikleri, kül dolgu içermektedir")
S(p, "FIND", "hayvan kemikleri (C5b1-C5b2 çöp çukurları)", "kind", "hayvan kemikleri",
  "bunlar da kırık seramik parçaları ve hayvan kemikleri, kül dolgu içermektedir")
S(p, "BUILT", "çöp çukurları (C5b1 ve C5b2, kazılan)", "fill", "kül dolgu",
  "bunlar da kırık seramik parçaları ve hayvan kemikleri, kül dolgu içermektedir")
S(p, "BUILT", "alandaki tüm çöp çukurları", "contents", "kırık seramik parçaları, hayvan kemikleri, kül dolgu",
  "Alandaki tüm çöp çu")
S(p, "FIND", "at figürinleri (C5b1 ve C5b2)", "kind", "at figürinleri",
  "at figürinleri, heykelcikler, ağırşaklar ve diğer küçük buluntulardan örnekler")
S(p, "FIND", "heykelcikler (C5b1 ve C5b2)", "kind", "heykelcikler",
  "at figürinleri, heykelcikler, ağırşaklar ve diğer küçük buluntulardan örnekler")
S(p, "FIND", "ağırşaklar (C5b1 ve C5b2)", "kind", "ağırşaklar",
  "at figürinleri, heykelcikler, ağırşaklar ve diğer küçük buluntulardan örnekler")
S(p, "FIND", "diğer küçük buluntular (C5b1 ve C5b2)", "kind", "diğer küçük buluntular",
  "at figürinleri, heykelcikler, ağırşaklar ve diğer küçük buluntulardan örnekler")
S(p, "FIND", "at figürinleri, heykelcikler, ağırşaklar ve diğer küçük buluntular", "was found in", "C5b1 ve C5b2 açmaları",
  "C5b1 ve C5b2 açmalarının kazısı sırasında")
S(p, "INTERP", "C5b1 ve C5b2 küçük buluntuları", "is compared to", "Kuzey Yamaç’taki önceki kazılardan bilinenler",
  "C5b1 ve C5b2 açmalarının kazısı sırasında Kuzey Yamaç’taki önceki kazılardan")
S(p, "FIND", "heykelcik parçası", "kind", "küçük bir heykelciğin baş tarafına ait parça",
  "bir heykelciğin baş tarafına ait olan parça")
S(p, "FIND", "heykelcik parçası", "period", "Helenistik/Roma Dönemi",
  "Helenistik/Roma Dönemi’ne tarihlenebilecek olan", h="tarihlenebilecek")
S(p, "FIND", "heykelcik parçası", "was found in", "kazılan dolgu", "kazılan dolgu içinden ele geçirilmiştir")
S(p, "BUILT", "çöp çukuru (C5b2, oval)", "is located in", "C5b2 açması", "C5b2")
S(p, "BUILT", "çöp çukuru (C5b2, oval)", "position", "açmanın doğu sınırına yakın",
  "açmanın doğu sınırına yakın, oval formda")
S(p, "BUILT", "çöp çukuru (C5b2, oval)", "shape", "oval form", "açmanın doğu sınırına yakın, oval formda")
S(p, "MEASURE", "çöp çukuru (C5b2, oval)", "measures (depth)", "yaklaşık olarak 1.5 metre",
  "1.5 metre derinlikte bir çöp çukuru tespit edilmiştir", h="yaklaşık olarak")
S(p, "FIGURE", "çöp çukuru (C5b2, oval)", "is shown in figure", "Resim: 6",
  "bir çöp çukuru tespit edilmiştir (Resim: 6)")
S(p, "BUILT", "ikinci çöp çukuru (C5b2)", "position", "oval çöp çukuruna bitişik", "sırasında buna bitişik ve çok daha küçük")
S(p, "MEASURE", "ikinci çöp çukuru (C5b2)", "size", "çok daha küçük", "sırasında buna bitişik ve çok daha küçük")
S(p, "BUILT", "ikinci çöp çukuru (C5b2)", "has distinct shape", "belirgin bir form",
  "belirgin bir forma sahip olmayan ve çok sığ ikinci", neg=True)
S(p, "MEASURE", "ikinci çöp çukuru (C5b2)", "depth", "çok sığ", "belirgin bir forma sahip olmayan ve çok sığ ikinci")
S(p, "FIND", "kemik parçaları (C5b2 çöp çukurları)", "kind", "kemik parçası",
  "Her iki çöp çukurundan çok sayıda kemik")
S(p, "FIND", "kemik parçaları (C5b2 çöp çukurları)", "count", "çok sayıda", "Her iki çöp çukurundan çok sayıda kemik")
S(p, "FIND", "seramik parçaları (C5b2 çöp çukurları)", "kind", "seramik parçası", "ve seramik parçası ele geçirilmiştir")
S(p, "FIND", "seramik parçaları (C5b2 çöp çukurları)", "count", "çok sayıda", "Her iki çöp çukurundan çok sayıda kemik")
S(p, "FIND", "kemik ve seramik parçaları", "was found in", "her iki çöp çukuru (C5b2)",
  "Her iki çöp çukurundan çok sayıda kemik")
S(p, "BUILT", "oval çöp çukuru (C5b2)", "fill", "kalın ve birkaç farklı seviyede kül dolgu",
  "farklı seviyede kül dolgunun homojen olmayarak dolduğu tespit edilmiştir")
S(p, "BUILT", "oval çöp çukurundaki kül dolgu", "is homogeneous", "homojen",
  "farklı seviyede kül dolgunun homojen olmayarak dolduğu tespit edilmiştir", neg=True)
S(p, "MEASURE", "C5b1 ve C5b2 açmaları (2024 sezonu sonu)", "level below Höyük yüzeyi", "yaklaşık 2.4 metre",
  "Höyük yüzeyinden yaklaşık 2.4 metre", h="yaklaşık")
S(p, "WORK", "C5b1 ve C5b2 açmaları (2024)", "Locus excavated (count)", "toplam 5 Locus",
  "aşağıdadır ve toplam 5 Locus kazılmıştır")
S(p, "PLACE", "C4b10 açması", "is located in", "Kuzey Yamaç", "C4b10 açması Kuzey Yamaç’ta en derin açmalardan olup")
S(p, "PLACE", "C4b10 açması", "is", "Kuzey Yamaç’ta en derin açmalardan",
  "C4b10 açması Kuzey Yamaç’ta en derin açmalardan olup")
S(p, "WORK", "C4b10 kazısı (2024)", "duration", "yaklaşık sekiz gün", "kiz gün süren bir kazı çalışmasına sahne olmuştur",
  h="yaklaşık")
S(p, "PLACE", "C4b10 açılış kotları", "depth relative to yüzeydeki 1055.31 metre kotu", "iki metre",
  "Açılış kotları yüzeydeki 1055.31 metre kotuna kıyasla iki metre derinlik göstermektedir")
S(p, "BUILT", "çöp çukuru (C4b10)", "position", "C4b9 açmasıyla olan sınırında",
  "daki C4b9 açmasıyla olan sınırında geniş ve dairesel formda bir çöp çukuru")
S(p, "BUILT", "çöp çukuru (C4b10)", "shape", "geniş ve dairesel form",
  "daki C4b9 açmasıyla olan sınırında geniş ve dairesel formda bir çöp çukuru", h="anlaşılmaktadır")
S(p, "PLACE", "C4b9 açması", "position", "C4b10 açmasının batısında", "Açmanın son kazıldığı sezonda batısın")
S(p, "WORK", "C4b10 kazısı (2024)", "started from", "Locus 60", "2024 kazıları bu açmada Locus 60’dan başlatılmıştır")
S(p, "WORK", "C4b10 kazısı (2024)", "step (first)", "açmanın çöp çukurunun taban seviyesine indirilmesi",
  "runun taban seviyesine indirilmesi")
S(p, "WORK", "C4b10 kazısı (2024)", "step (then)", "tüm açma yüzeyinde kazı çalışması yapılması",
  "sonra da tüm açma yüzeyinde kazı çalışması yapılması")
S(p, "MEASURE", "C4b10 kazısı (2024)", "depth excavated", "yaklaşık 40 santimetre",
  "yaklaşık 40 santimetre derinleşilmiştir", h="yaklaşık")
S(p, "PLACE", "C4b10 açma merkezi", "closing elevation (kapanış kotu)", "1052.803 metre",
  "kezinde kapanış kotu 1052.803 metre olup")
S(p, "MEASURE", "C4b10 açması", "depth reached below Höyük yüzeyi", "2.5 metre", "Höyük yüzeyinden 2.5 metre inilmiştir")
S(p, "FIGURE", "C4b10 açması", "is shown in figure", "Resim: 8", "2.5 metre inilmiştir (Resim:")
S(p, "FIND", "seramik parçaları (C4b10)", "kind", "seramik parçaları",
  "Orta ve Geç Tunç çağlarına ait seramik parçalarının ele geçirildiği tespit edilmiştir")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "ETÇ III", "tespit edilmeyen ETÇ III,")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "Orta Tunç çağı", "Orta ve Geç Tunç çağlarına ait seramik parçalarının")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "Geç Tunç çağı", "Orta ve Geç Tunç çağlarına ait seramik parçalarının")
S(p, "FIND", "seramik parçaları (C4b10)", "was found in", "C4b10 açması", "Bu açmanın kazısı sırasında")
S(p, "FIND", "ETÇ III, Orta ve Geç Tunç çağı seramik parçaları", "found before in nearby trenches", "civardaki açmalar",
  "daha önce civardaki açmalarda tespit edilmeyen ETÇ III", neg=True)
S(p, "FIND", "tezgâh ağırlığı", "kind", "tezgâh ağırlığı", "küçük bir tezgâh ağırlığı envanterlik olarak kaydedilmiştir")
S(p, "FIND", "tezgâh ağırlığı", "count", "bir", "küçük bir tezgâh ağırlığı envanterlik olarak kaydedilmiştir")
S(p, "FIND", "tezgâh ağırlığı", "size", "küçük", "küçük bir tezgâh ağırlığı envanterlik olarak kaydedilmiştir")
S(p, "FIND", "tezgâh ağırlığı", "was found in", "bu alanda yüzeyde", "alanda yüzeyde bulunan küçük bir tezgâh ağırlığı")
S(p, "FIND", "tezgâh ağırlığı", "was registered as", "envanterlik", "küçük bir tezgâh ağırlığı envanterlik olarak kaydedilmiştir")
S(p, "WORK", "C4c10 açması", "is", "Kuzey Yamaç’ta 2024 sezonunda kazısı yapılan son açma",
  "Kuzey Yamaç’ta 2024 sezonunda kazısı yapılan son açma C4c10’dur")
S(p, "WORK", "C4c10 kazısı (2024)", "duration", "sadece iki gün", "Sadece iki gün")
S(p, "WORK", "C4c10 açması", "step", "kenarlardan ve kesitten düşerek açma yüzeyinde biriken taşlar toplanmış ve açma dışına çıkarılmıştır",
  "kenarlardan ve kesitten düşerek açma yüzeyinde biriken taşlar")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "removal was started", "kaldırılmasına başlanmıştır",
  "Demir Devri duvarların kaldırılmasına başlanmıştır")
S(p, "DATE", "duvarlar (C4c10)", "is dated to", "Demir Devri", "Demir Devri duvarların kaldırılmasına başlanmıştır")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were exposed in", "açmadaki son kazı sezonu",
  "açmadaki son kazı sezonunda açığa")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were documented by", "fotoğraflanarak",
  "fotoğraflanarak çizimi yapılan Demir Devri duvarların")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were documented by", "çizim",
  "fotoğraflanarak çizimi yapılan Demir Devri duvarların")
S(p, "BUILT", "dolgu (C4c10)", "condition", "oldukça sert", "oldukça sert bir dolgu yaklaşık 20")
S(p, "MEASURE", "dolgu (C4c10)", "depth excavated", "yaklaşık 20 santimetre", "oldukça sert bir dolgu yaklaşık 20",
  h="yaklaşık")
S(p, "BUILT", "sert dolgu (C4c10)", "lies below", "Demir Devri duvarlar",
  "Duvarlar kaldırıldıktan sonra yapılan kazı çalışmasında oldukça sert bir dolgu")
S(p, "WORK", "bu açmalardaki kazı çalışmaları", "will continue in", "2025 sezonu",
  "Bu açmalarda kazı çalışmaları 2025 sezonunda devam edecek")
S(p, "WORK", "bu alan", "planned to be lowered to", "diğer açmaların kotu",
  "alanın da diğer açmaların kotuna indirilmesi için çalışılacaktır")
S(p, "BUILT", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "kind", "Tunç Çağı sonrası katman",
  "bir Tunç Çağı sonrası (Demir Devri, Arkaik, Klasik,")
S(p, "MEASURE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "thickness", "yaklaşık 4-5 metre",
  "yaklaşık 4-5 metre kalınlığında", h="yaklaşık")
for per, q in [("Demir Devri", "(Demir Devri, Arkaik, Klasik,"), ("Arkaik", "(Demir Devri, Arkaik, Klasik,"),
               ("Klasik", "(Demir Devri, Arkaik, Klasik,"), ("Helenistik/Roma", "Helenistik/Roma, Bizans) katmanı"),
               ("Bizans", "Helenistik/Roma, Bizans) katmanı")]:
    S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", per, q)
S(p, "INTERP", "Tunç Çağı sonrası katmanının tespiti", "is based on", "1994 yılından beri yürütülen kazı çalışmaları ve ERT yönteminin sonuçları",
  "yük genelinde uygulanan ERT yönteminin sonuçlarıyla birlikte ele alındığında")
S(p, "MEASURE", "Kuzey Yamaç’ta kazılan alan", "measures", "yaklaşık 20x30 metre", "(yaklaşık 20x30 metre alanda)",
  h="yaklaşık")
S(p, "BUILT", "kalın dolgu (Kuzey Yamaç)", "contains stratigraphy with sound architectural plans", "sağlam mimari planlar veren, somut maddi kültür kalıntısı sağlayan stratigrafi",
  "maddi kültür kalıntısı sağlayan stratigrafiye rastlanmamıştır", neg=True)

# ---------------------------------------------------------------- page 285
p = 285
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "kırık seramik parçaları",
  "tamamen kırık seramik parçaları, figürin parçaları ve diğer küçük buluntulardan oluşan")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "figürin parçaları",
  "tamamen kırık seramik parçaları, figürin parçaları ve diğer küçük buluntulardan oluşan")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "diğer küçük buluntular",
  "tamamen kırık seramik parçaları, figürin parçaları ve diğer küçük buluntulardan oluşan")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "is disturbed by", "çöp çukurları",
  "sıklıkla çöp çukurları tarafından tahrip edilmiş bir stratigrafik karaktere sahiptir", h="sıklıkla")
S(p, "INTERP", "Kuzey Yamaç’ta Tunç Çağları tabakalarına kadar sağlam mimari ve maddi kültür kalıntısı bulma", "likelihood",
  "oldukça zayıf", "kültür kalıntısı bulma ihtimali oldukça zayıftır", h="ihtimali oldukça zayıftır")
S(p, "DESCR", "C4a8 açmasındaki ETÇ yapı katları", "is judged as", "mimari ve küçük buluntu açısından oldukça sağlam bulgular sunan",
  "buluntu açısından oldukça sağlam bulgular sunduğu")
S(p, "INTERP", "karışık ve sağlam mimari plan/buluntu vermeyen dolgu", "will not end until", "tüm açmalarda 1049 metre kota erişilinceye kadar",
  "1049 metre kota erişilinceye kadar bu karışık ve sağlam mimari plan/buluntu vermeyen", h="açıktır")
S(p, "STRUCT", "başlık", "heading reads", "4.2 MERKEZİ KİLİSE (Geleceğe Miras Projesi ödeneğiyle)",
  "4.2 MERKEZİ KİLİSE (Geleceğe Miras Projesi ödeneğiyle)")
S(p, "ADMIN", "Merkezi Kilise kazısı", "was funded by", "Geleceğe Miras Projesi ödeneği",
  "(Geleceğe Miras Projesi ödeneğiyle)")
S(p, "ADMIN", "Geleceğe Miras Projesi", "belongs to body", "Kültür Varlıkları ve Müzeler Genel Müdürlüğü",
  "Kültür Varlıkları ve Müzeler Genel Müdürlüğünün Geleceğe Miras Proje")
S(p, "WORK", "Merkezi Kilise kazısı (2024)", "name of the work", "Merkezi Kilise 1. Etap 333 m2 Alan İçerisinde El İle Kazı",
  "“Merkezi Kilise 1. Etap 333 m2 Alan İçerisinde El İle")
S(p, "WORK", "Merkezi Kilise kazısı (2024)", "method", "el ile kazı", "Alan İçerisinde El İle")
S(p, "WORK", "Merkezi Kilise açmaları", "count", "yedi adet", "yedi adet 5x5")
S(p, "MEASURE", "Merkezi Kilise açmaları", "measures", "5x5 metre", "yedi adet 5x5")
S(p, "FIGURE", "Merkezi Kilise kazısı (2024)", "is shown in table", "Tablo: 1", "(Tablo: 1, Resim: 9)")
S(p, "FIGURE", "Merkezi Kilise kazısı (2024)", "is shown in figure", "Resim: 9", "(Tablo: 1, Resim: 9)")
S(p, "WORK", "Merkezi Kilise kazıları", "aim", "Merkezi Kilise (Manastır) yapısının çevresini genişleterek restitüsyon ve restorasyon projelerine yeterli zemini ve alanı sağlamak",
  "amacı Merkezi Kilise (Manastır) yapısının çevresini genişleterek ileriki yıllarda yapılacak")
S(p, "WORK", "restitüsyon projesi (Merkezi Kilise)", "planned for", "ileriki yıllar",
  "restitüsyon ve restorasyon projelerine yeterli zemini ve alanı sağlamaktır")
S(p, "WORK", "restorasyon projesi (Merkezi Kilise)", "planned for", "ileriki yıllar",
  "restitüsyon ve restorasyon projelerine yeterli zemini ve alanı sağlamaktır")

# table
hdr = "Açma Açılış tarihi Açılış kotu Kapanış tarihi Kapanış kotu Kazılan m3"
for h_ in ["Açma", "Açılış tarihi", "Açılış kotu", "Kapanış tarihi", "Kapanış kotu", "Kazılan m3"]:
    S(p, "STRUCT", "Tablo 1", "has column heading", h_, hdr)
rows = [
    ("E4d9", "29.08.2024", "1052.52", "01.09.2024", "1051.25", "11.7"),
    ("E4d10", "03.09.2024", "1052.27", "05.09.2024", "1050.72", "11.02"),
    ("E5d1", "05.09.2024", "1052.16", "10.09.2024", "1050.00", "17.75"),
    ("E5c3", "07.09.2024", "1051.79", "12.09.2024", "1049.93", "12.2"),
    ("E5c4", "08.09.2024", "1051.85", "14.09.2024", "1050.13", "21.41"),
    ("E5c5", "12.08.2024", "1051.79", "17.09.2024", "1050.13", "12.89"),
    ("E5b6", "17.09.2024", "1051.76", "26.09.2024", "1050.08", "33.81"),
]
for r in rows:
    q = " ".join(r)
    S(p, "WORK", "Tablo 1 satırı", "trench (Açma)", r[0], q)
    unclear = " (unclear: earlier than the start date 29.08.2024 given for the whole work)" if r[0] == "E5c5" else ""
    S(p, "WORK", r[0] + " açması", "opening date (Açılış tarihi)" + unclear, r[1], q)
    S(p, "PLACE", r[0] + " açması", "opening elevation (Açılış kotu)", r[2], q)
    S(p, "WORK", r[0] + " açması", "closing date (Kapanış tarihi)", r[3], q)
    S(p, "PLACE", r[0] + " açması", "closing elevation (Kapanış kotu)", r[4], q)
    S(p, "WORK", r[0] + " açması", "volume excavated (Kazılan m3)", r[5], q)
tq = "TOPLAM 29.08.2024 27.09.2024 120.78"
S(p, "STRUCT", "Tablo 1", "has row label", "TOPLAM", tq)
S(p, "WORK", "TOPLAM (Tablo 1)", "opening date (Açılış tarihi)", "29.08.2024", tq)
S(p, "WORK", "TOPLAM (Tablo 1)", "closing date (Kapanış tarihi)", "27.09.2024", tq)
S(p, "WORK", "TOPLAM (Tablo 1)", "volume excavated (Kazılan m3)", "120.78", tq)
S(p, "FIGURE", "Tablo 1", "caption",
  "Merkezi Kilise’de 2024 sezonunda kazı yapılan açmalar, açılış-kapanış tarihleri, açılış-kapanış kotları ve toplam hafriyat miktarı (m3).",
  "Tablo 1: Merkezi Kilise’de 2024 sezonunda kazı yapılan açmalar, açılış-kapanış tarihleri, açılış-kapanış kotları ve toplam hafriyat miktarı (m3).")
S(p, "ADMIN", "Merkezi Kilise çalışmasına ait ayrıntılı rapor", "was submitted to", "T.C. Antalya Valiliği, İl Kültür ve Turizm Müdürlüğü",
  "ayrıntılı rapor T.C. Antalya Valiliği, İl Kültür ve Tu")
S(p, "STRUCT", "Merkezi Kilise çalışması", "is reported in detail here", "detaylı bir şekilde",
  "burada detaylı bir şekilde aktarılmayacaktır", neg=True)
S(p, "BUILT", "Manastır yapısına ait farklı mekanların duvarları", "condition", "sağlam",
  "farklı mekanların duvarlarının sağlam olarak ele geçirilmesidir")
S(p, "BUILT", "Manastır yapısına ait farklı mekanların duvarları", "was found in", "Manastır yapısının güney sınırı boyunca açılan tüm açmalar",
  "bulgu Manastır yapısının güney sınırı boyunca açılan tüm açmalarda")
S(p, "DESCR", "mekan duvarlarının sağlam ele geçirilmesi", "is judged as", "1. Etap kazılarında elde edilen en önemli bulgu",
  "1. Etap kazılarında elde edilen en önemli")
S(p, "BUILT", "Merkezi Kilise", "is built with", "ikincil malzeme (spolia)",
  "sında sıklıkla kullanılan ikincil malzeme (spolia)", h="sıklıkla")
S(p, "BUILT", "Manastır yapısını çevreleyen mekanlar", "is built with", "ikincil malzeme (spolia)",
  "ikincil malzeme (spolia) Manastır yapısını çevreleyen mekanlarda")
S(p, "FIGURE", "ikincil malzeme (spolia)", "is shown in figure", "Resim: 10", "da gözlemlenmiştir (Resim: 10)")

# ---------------------------------------------------------------- page 286
p = 286
S(p, "BUILT", "büyük sarnıç", "is part of", "Manastır yapısı", "Manastır yapısının parçası olan büyük sarnıç")
S(p, "BUILT", "büyük sarnıç", "was exposed", "ortaya çıkarıldığı",
  "Manastır yapısının parçası olan büyük sarnıç ve onu çevreleyen yapıların da ortaya")
S(p, "BUILT", "sarnıcı çevreleyen yapılar", "was exposed", "ortaya çıkarıldığı",
  "büyük sarnıç ve onu çevreleyen yapıların da ortaya")
S(p, "BUILT", "yol", "kind", "taban döşemesi olan bir yol", "ayrıca taban döşemesi olan bir yol da bulunmuştur")
S(p, "FIGURE", "yol / sarnıç", "is shown in figure", "Resim: 11", "yol da bulunmuştur (Resim: 11)")
S(p, "BUILT", "Manastır yapısını çevreleyen yapılar", "plan (unclear: sentence is garbled, 'ise çok Manastır yapısını')", "çok evreli planlar",
  "alanın kuzeyine, Kilise’nin apsis yapısına doğru ise çok Manastır yapısını çevreleyen")
S(p, "BUILT", "çok evreli yapılar", "position", "bu alanın kuzeyine, Kilise’nin apsis yapısına doğru",
  "alanın kuzeyine, Kilise’nin apsis yapısına doğru")
S(p, "BUILT", "Kilise", "has part", "apsis yapısı", "Kilise’nin apsis yapısına doğru")
S(p, "WORK", "GMP bünyesinde yürütülen kazılar", "last day", "27.09.2024",
  "olan 27.09.2024 tarihi itibarıyla")
S(p, "FIGURE", "Merkezi Kilise’de kazı yapılan alanların görünümü", "is shown in figure", "Resim 12",
  "Merkezi Kilise’de kazı yapılan alanların görünümü Resim")
S(p, "FIND", "işli mimari parçalar", "kind", "işli mimari parçalar", "Merkezi Kilise kazılarında ele geçen işli mimari parçalar")
S(p, "FIND", "işli mimari parçalar", "was found in", "Merkezi Kilise kazıları",
  "Merkezi Kilise kazılarında ele geçen işli mimari parçalar")
S(p, "FIND", "işli mimari parçalar", "was stored in (either)", "Höyük üzerindeki taş havuzu",
  "vuzuna konmuş ya da kazı deposuna getirtilmiştir")
S(p, "FIND", "işli mimari parçalar", "was stored in (or)", "kazı deposu",
  "vuzuna konmuş ya da kazı deposuna getirtilmiştir")
S(p, "FIND", "sikkeler", "kind", "sikke", "bakır sikkeler ve takı (bilezik?)")
S(p, "FIND", "sikkeler", "is made of", "bakır", "bakır sikkeler ve takı (bilezik?)")
S(p, "FIND", "sikkeler", "condition", "oldukça korozyona uğramış", "sında oldukça korozyona uğramış bakır sikkeler")
S(p, "FIND", "takı", "kind", "takı", "bakır sikkeler ve takı (bilezik?)")
S(p, "FIND", "takı", "is identified as", "bilezik", "takı (bilezik?)", h="?")
S(p, "FIND", "takı", "is made of (unclear: whether 'bakır' and 'korozyona uğramış' also apply to takı)", "bakır",
  "sında oldukça korozyona uğramış bakır sikkeler ve takı (bilezik?)")
S(p, "FIND", "liturji (ayin) objeleri", "kind", "liturji (ayin) objeleri", "demirden imal edilmiş liturji (ayin) objeleri")
S(p, "FIND", "liturji (ayin) objeleri", "is made of", "demir", "demirden imal edilmiş liturji (ayin) objeleri")
S(p, "FIND", "boncuk", "kind", "boncuk", "pişmiş topraktan boncuk")
S(p, "FIND", "boncuk", "is made of", "pişmiş toprak", "pişmiş topraktan boncuk")
S(p, "FIND", "küçük buluntular (Merkezi Kilise)", "is classed as", "etütlük",
  "gibi etütlük sayılacak buluntular vardır", h="sayılacak")
S(p, "FIND", "küçük buluntular (sikkeler, takı, liturji objeleri, boncuk)", "was found in", "Merkezi Kilise kazıları",
  "Kazılardan çıkan küçük buluntular ara")
S(p, "STRUCT", "başlık", "heading reads", "5- KAMU YARARINA FAALİYETLER:", "5- KAMU YARARINA FAALİYETLER:")
S(p, "WORK", "Hacımusalar Höyük Kazısı", "includes", "disiplinler arası araştırmalar",
  "Hacımusalar Höyük Kazısı kapsamında yürütülen disiplinler arası araştırmaların")
S(p, "WORK", "disiplinler arası araştırmalar", "aim", "güncel sorunların çözümüne katkı sağlamak",
  "çözümüne ve Elmalı Ovası’ndaki refahın artırılmasına katkı")
for v in ["iklim değişikliği", "tarımsal üretimde verim kaybı", "erozyon", "ani ve şiddetli meteorolojik olaylar"]:
    S(p, "DESCR", "güncel sorunlar", "example named", v,
      "(iklim değişikliği, tarımsal üretimde verim kaybı, erozyon, ani ve şiddet")
S(p, "WORK", "disiplinler arası araştırmalar", "aim", "Elmalı Ovası’ndaki refahın artırılmasına katkı sağlamak",
  "çözümüne ve Elmalı Ovası’ndaki refahın artırılmasına katkı")
S(p, "WORK", "etkinlikler", "frequency", "her yıl", "sağlaması amacıyla her yıl ilçenin yöneticileri")
for v in ["ilçenin yöneticileri", "kamu görevlileri", "halk"]:
    S(p, "WORK", "etkinlikler", "audience", v,
      "her yıl ilçenin yöneticileri, kamu görevlileri ve halkı için düzenlenen")
S(p, "WORK", "etkinlikler", "content", "çalışmalarımızdan kesitler", "etkinliklerde çalışmalarımızdan kesitler sunmaktayız")
S(p, "WORK", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "date", "12.10.2024", "12.10.2024 tarihinde El")
S(p, "ADMIN", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "was organised by", "Elmalı Belediyesi",
  "malı Belediyesi ve Elmalı Vakfı tarafından düzenlenen")
S(p, "ADMIN", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "was organised by", "Elmalı Vakfı",
  "malı Belediyesi ve Elmalı Vakfı tarafından düzenlenen")
S(p, "WORK", "konuşma", "was given at", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu",
  "düzenlenen Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu’nda")
S(p, "WORK", "konuşma", "has title", "Elmalı Ovası’nın Geçmiş İklimi ve Kültür Tarihi",
  "“Elmalı Ovası’nın Geçmiş İklimi ve Kültür Tarihi”")
S(p, "WORK", "konuşma", "topic", "bölgedeki arkeolojik kültürler", "hem bölgedeki arkeolojik kültürlere hem de geçmiş insanların")
S(p, "WORK", "konuşma", "topic", "geçmiş insanların yaşadıkları çevresel sorunlar",
  "yaşadıkları çevresel sorunlara dikkat çekilmiştir")

# ---------------------------------------------------------------- page 287
p = 287
S(p, "STRUCT", "başlık", "heading reads", "EKLER", "EKLER")
S(p, "FIGURE", "Resim 1", "caption",
  "Merkezi Kilise’nin kuzey ve batısındaki alanlarda 2022, 2023 ve 2024 sezonlarında gerçekleştirilen yer radarı çalışmalarının sonuçları.",
  "Resim 1: Merkezi Kilise’nin kuzey ve batısındaki alanlarda 2022, 2023 ve 2024 sezonlarında gerçekleştirilen yer radarı çalışmalarının sonuçları.")
S(p, "FIGURE", "Resim 2", "caption",
  "Hacımusalar Höyük’te gerçekleştirilen Elektrik Rezistivite (Özdirenç) Tomografi (ERT) çalışmasında taranan 10 profilin konumunu gösteren harita.",
  "Resim 2: Hacımusalar Höyük’te gerçekleştirilen Elektrik Rezistivite (Özdirenç) Tomografi (ERT) çalışmasında taranan 10 profilin konumunu gösteren harita.")

# ---------------------------------------------------------------- page 288
p = 288
S(p, "FIGURE", "Resim 3", "caption",
  "(a) Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline ait ölçüm haritaları, (b) topoğrafik düzeltmesi yapılmış olan hat haritası üzerinde işaretlenen arkeolojik (1,4,5,6) ve jeolojik (2,3,7) katmanlar.",
  "Resim 3: (a) Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline ait ölçüm haritaları")
S(p, "MEASURE", "birinci ERT profili", "measures (length)", "240 metre", "240 metre uzunluktaki birinci ERT profiline")
S(p, "FIGURE", "birinci ERT profili", "is shown in figure", "Resim 2", "Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline")
S(p, "WORK", "hat haritası", "processing", "topoğrafik düzeltmesi yapılmış",
  "topoğrafik düzeltmesi yapılmış olan hat haritası")
S(p, "INTERP", "katmanlar 1, 4, 5, 6", "is interpreted as", "arkeolojik", "arkeolojik (1,4,5,6) ve jeolojik (2,3,7) katmanlar")
S(p, "INTERP", "katmanlar 2, 3, 7", "is interpreted as", "jeolojik", "arkeolojik (1,4,5,6) ve jeolojik (2,3,7) katmanlar")
S(p, "FIGURE", "Resim 4", "caption",
  "Önceki kazı sezonlarında kısmen kazılan, her biri farklı seviyelerde bırakılan açmalar. 2024 kazı sezonunda kazısı yapılan açmalar C4b10, C4c10, C5b1, C5b2 olmuştur. Bu fotoğraf aynı zamanda 2024 sezonu sonunda Kuzey Yamaç açmalarının kapanış durumunu göstermektedir.",
  "Resim 4: Önceki kazı sezonlarında kısmen kazılan, her biri farklı seviyelerde bırakılan açmalar.")
S(p, "WORK", "Kuzey Yamaç açmaları", "state after previous seasons", "kısmen kazılan, her biri farklı seviyelerde bırakılan",
  "Önceki kazı sezonlarında kısmen kazılan, her biri farklı seviyelerde bırakılan")
S(p, "WORK", "2024 kazı sezonunda kazısı yapılan açmalar", "are", "C4b10, C4c10, C5b1, C5b2",
  "2024 kazı sezonunda kazısı yapılan açmalar C4b10, C4c10, C5b1, C5b2")
S(p, "FIGURE", "Resim 4", "shows", "2024 sezonu sonunda Kuzey Yamaç açmalarının kapanış durumu",
  "Bu fotoğraf aynı zamanda 2024 sezonu sonunda Kuzey Yamaç açmalarının")

# ---------------------------------------------------------------- page 289
p = 289
S(p, "FIGURE", "Resim 5", "caption",
  "C4a6 açmasında yüzeyin 1 metre altında tespit edilen in situ kerpiç blok (35x35x12 cm).",
  "Resim 5: C4a6 açmasında yüzeyin 1 metre altında tespit edilen in situ kerpiç blok (35x35x12 cm).")
S(p, "FIND", "kerpiç blok", "measures (unclear: caption 35x35x12 cm, text gives 35x3x12 cm)", "35x35x12 cm",
  "in situ kerpiç blok (35x35x12 cm)")

# ---------------------------------------------------------------- page 290
p = 290
S(p, "FIGURE", "Resim 6", "caption",
  "C4a6-C4a7-C4b7 açmalarının İHA görüntüsü. C4a6’daki 2x1 m sondajda bulunan kerpiç bloğu korumak üzere naylon örtü vardır. [...]",
  "Resim 6: C4a6-C4a7-C4b7 açmalarının İHA görüntüsü.")
S(p, "WORK", "Resim 6 görüntüsü", "was taken with", "İHA", "C4a6-C4a7-C4b7 açmalarının İHA görüntüsü")
S(p, "LAB", "kerpiç blok (C4a6 sondajı)", "is protected by", "naylon örtü",
  "bulunan kerpiç bloğu korumak üzere naylon örtü vardır")
S(p, "BUILT", "çöp çukuru (kuzey yarısı)", "position", "C4a7 açmasını C4b7 açmasından ayıran eşiğin hemen altında",
  "C4a7 açmasını C4b7 açmasından ayıran eşiğin hemen altında")
S(p, "BUILT", "çöp çukuru (kuzey yarısı)", "shape", "dairesel form",
  "naylon örtü altında dairesel formda bir çöp çukurunun kuzey")
S(p, "LAB", "çöp çukuru (kuzey yarısı)", "is covered by", "naylon örtü",
  "naylon örtü altında dairesel formda bir çöp çukurunun kuzey")
S(p, "BUILT", "eşik", "separates", "C4a7 açması ile C4b7 açması", "C4a7 açmasını C4b7 açmasından ayıran eşiğin")
S(p, "BUILT", "diğer çöp çukuru", "position", "açmanın ortasında",
  "açmanın ortasında ise dairesel formda diğer bir çöp çukuru görülmektedir")
S(p, "BUILT", "diğer çöp çukuru", "shape", "dairesel form",
  "açmanın ortasında ise dairesel formda diğer bir çöp çukuru görülmektedir")
S(p, "BUILT", "üçüncü çöp çukuru", "position", "açmanın güneydoğu köşesinde",
  "çöp çukuru açmanın güneydoğu köşesinde birkaç santimetre aşağıda çıkacaktır", h="çıkacaktır")
S(p, "BUILT", "üçüncü çöp çukuru", "depth below current level", "birkaç santimetre aşağıda",
  "çöp çukuru açmanın güneydoğu köşesinde birkaç santimetre aşağıda çıkacaktır", h="çıkacaktır")
S(p, "FIGURE", "Resim 7", "caption",
  "C4b10 açmasının 2024 kazı sezonu sonundaki görünümü. Fotoğrafın sol alt köşesine (batıya) doğru C4b9 açması yer almaktadır; bu Kuzey Yamaç’taki en derin açmadır.",
  "Resim 7: C4b10 açmasının 2024 kazı sezonu sonundaki görünümü.")
S(p, "FIGURE", "C4b9 açması", "position in the photograph", "fotoğrafın sol alt köşesine (batıya) doğru",
  "köşesine (batıya) doğru C4b9 açması yer almaktadır")
S(p, "PLACE", "'bu' (unclear: C4b9 or C4b10)", "is (unclear: referent of 'bu' not certain)", "Kuzey Yamaç’taki en derin açma",
  "bu Kuzey Yamaç’taki en derin")

# ---------------------------------------------------------------- page 291
p = 291
S(p, "FIGURE", "Resim 8", "caption",
  "Merkezi Kilise’nin karelajlarını gösteren harita. Bu İHA görüntüsü 2024 kazıları başlamadan önce alınmış olup Merkezi Kilise’nin güney sınırı boyunca (kabaca A4 ve A3 noktaları arasında) kazı yapılan açmaları göstermektedir. Kazılan açmalar kırmızı okun üst kısmındadır.",
  "Resim 8: Merkezi Kilise’nin karelajlarını gösteren harita.")
S(p, "WORK", "Resim 8 İHA görüntüsü", "was taken", "2024 kazıları başlamadan önce",
  "Bu İHA görüntüsü 2024")
S(p, "PLACE", "kazı yapılan açmalar (Merkezi Kilise)", "position", "Merkezi Kilise’nin güney sınırı boyunca",
  "Merkezi Kilise’nin güney sınırı boyunca (kabaca")
S(p, "PLACE", "kazı yapılan açmalar (Merkezi Kilise)", "lie between points", "A4 ve A3 noktaları arasında",
  "A4 ve A3 noktaları arasında) kazı yapılan açmaları göstermektedir", h="kabaca")
S(p, "FIGURE", "kazılan açmalar", "position in the image", "kırmızı okun üst kısmında",
  "Kazılan açmalar kırmızı okun üst kısmındadır")
S(p, "FIGURE", "Resim 9", "caption",
  "E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi; tüm yapı malzemesi ikincil kullanımdır.",
  "Resim 9: E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi; tüm yapı malzemesi ikincil kullanımdır.")
S(p, "BUILT", "kapı eşiği", "was found in", "E4d10 açması",
  "E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi")
S(p, "BUILT", "kapı dikmesi", "was found in", "E4d10 açması",
  "E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi")
S(p, "BUILT", "kapı eşiği ve dikmesi (E4d10)", "building material", "tüm yapı malzemesi ikincil kullanım",
  "malzemesi ikincil kullanımdır")

# ---------------------------------------------------------------- page 292
p = 292
S(p, "FIGURE", "Resim 10", "caption",
  "E5c4 açmasında sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi ve üzerindeki duvar örgüsünü gösteren fotoğraf.",
  "Resim 10: E5c4 açmasında sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi ve üzerindeki duvar örgüsünü gösteren fotoğraf.")
S(p, "BUILT", "sarnıç", "is located in", "E5c4 açması", "E5c4 açmasında sarnıcın hemen solunda")
S(p, "BUILT", "taban döşemesi (E5c4)", "position", "sarnıcın hemen solunda (kuzeydoğusunda)",
  "sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi")
S(p, "BUILT", "duvar örgüsü (E5c4)", "lies above", "taban döşemesi", "taban döşemesi ve üzerindeki duvar örgüsünü")
S(p, "FIGURE", "Resim 11", "caption",
  "E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının birden fazla evresine ait duvarları gösteren fotoğraf.",
  "Resim 11: E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının birden fazla evresine ait duvarları gösteren fotoğraf.")
S(p, "BUILT", "duvarlar (E5b6)", "belong to", "Merkezi Kilise yapısının çevresinde bulunan yapının birden fazla evresi",
  "yapının birden fazla evresine ait duvarları")
S(p, "BUILT", "duvarlar (birden fazla evreli yapı)", "is located in", "E5b6 açması",
  "E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının")

# ---------------------------------------------------------------- page 293
p = 293
S(p, "FIGURE", "Resim 12", "caption",
  "Merkezi Kilise’nin güney sınırı boyunca kazılan yedi 5x5 metre boyutlarındaki açmanın kapanış günündeki durumunu gösteren İHA fotoğrafı. Kazı yapılan açmalar kırmızı okun üst kısmındadır.",
  "Resim 12: Merkezi Kilise’nin güney sınırı boyunca kazılan yedi 5x5 metre boyutlarındaki açmanın kapanış günündeki durumunu gösteren İHA fotoğrafı.")
S(p, "WORK", "Resim 12 fotoğrafı", "was taken with", "İHA", "kapanış günündeki durumunu gösteren İHA fotoğrafı")
S(p, "WORK", "Resim 12 fotoğrafı", "was taken on", "kapanış günü", "kapanış günündeki durumunu gösteren İHA fotoğrafı")

# ---------------------------------------------------------------- output + check
for i, r in enumerate(R, 1):
    r["n"] = i
KEYS = ["n", "page", "group", "subject", "says", "value", "hedge", "negative", "who", "quote"]
R = [{k: r[k] for k in KEYS} for r in R]
json.dump(R, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# check
data = json.load(open(OUT, encoding="utf-8"))
raw = open(PAPER, encoding="utf-8").read()


def norm(t):
    t = re.sub(r"-[ \t]*\n\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


pages = raw.split("\f")
pnorm = {}
for pg in pages:
    nums = re.findall(r"^\s*(\d{3})\s*$", pg, flags=re.M)
    if nums:
        pnorm[int(nums[-1])] = norm(pg)
full = norm(raw.replace("\f", "\n"))
bad = 0
for r in data:
    if list(r.keys()) != KEYS:
        print("KEYS", r["n"]); bad += 1
    if r["group"] not in GROUPS:
        print("GROUP", r["n"]); bad += 1
    q = norm(r["quote"])
    if len(r["quote"]) > 200:
        print("LONG", r["n"], len(r["quote"])); bad += 1
    if not q or q not in full:
        print("QUOTE-NOT-FOUND", r["n"], r["page"], q); bad += 1
    elif q not in pnorm.get(r["page"], ""):
        print("QUOTE-WRONG-PAGE", r["n"], r["page"], q, [k for k, v in pnorm.items() if q in v]); bad += 1
print("pages found", sorted(pnorm))
print("bad", bad, "total", len(data))
print("groups", dict(collections.Counter(r["group"] for r in data)))
print("pages", dict(sorted(collections.Counter(r["page"] for r in data).items())))
print("hedged", sum(1 for r in data if r["hedge"]), "negative", sum(1 for r in data if r["negative"]))
print("unclear", [(r["n"], r["page"]) for r in data if "unclear" in r["says"] or "unclear" in r["subject"]])
