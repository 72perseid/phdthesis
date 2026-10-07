# -*- coding: utf-8 -*-
import json

ST = []


def S(page, group, subject, says, value, quote, hedge="", neg=False, who=""):
    ST.append({
        "n": len(ST) + 1, "page": page, "group": group, "subject": subject,
        "says": says, "value": value, "hedge": hedge, "negative": neg,
        "who": who, "quote": quote,
    })


HH = "Hacımusalar Höyük"
MK = "Merkezi Kilise"
KY = "Kuzey Yamaç"

# ---------------------------------------------------------------- page 279
p = 279
S(p, "STRUCT", "sayfa üst başlığı", "page header reads", "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1",
  "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1")
S(p, "DOC", "bildiri", "is published in", "45. Kazı Sonuçları Toplantısı Bildirileri, Cilt 1",
  "45. KAZI SONUÇLARI TOPLANTISI BİLDİRİLERİ/ CİLT 1")
S(p, "DOC", "bildiri", "has title", "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK KAZISI 2024 YILI ÇALIŞMALARI",
  "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK KAZISI 2024 YILI ÇALIŞMALARI")
S(p, "DOC", "bildiri", "has author", "Bülent ARIKAN", "Bülent ARIKAN*")
S(p, "PLACE", HH, "is located in (province)", "Antalya ili", "ANTALYA İLİ ELMALI İLÇESİ HACIMUSALAR HÖYÜK")
S(p, "PLACE", HH, "is located in (district)", "Elmalı ilçesi", "ELMALI İLÇESİ HACIMUSALAR HÖYÜK")
S(p, "WORK", "Hacımusalar Höyük Kazısı", "year of work reported", "2024", "HACIMUSALAR HÖYÜK KAZISI 2024 YILI")
S(p, "STRUCT", "başlık", "heading reads", "1. GİRİŞ", "1. GİRİŞ")
S(p, "ADMIN", "Hacımusalar Höyük arkeolojik araştırmaları", "is carried out on behalf of", "T.C. Kültür ve Turizm Bakanlığı (KTB)",
  "T.C. Kültür ve Turizm Bakanlığı (KTB) ile")
S(p, "ADMIN", "Hacımusalar Höyük arkeolojik araştırmaları", "is carried out on behalf of", "T.C. İstanbul Teknik Üniversitesi (İTÜ)",
  "T.C. İstanbul Teknik Üniversitesi (İTÜ) adına")
S(p, "ADMIN", "Hacımusalar Höyük arkeolojik araştırmaları", "permit kind", "Cumhurbaşkanlığı Kararnamesi",
  "5777 sayılı Cumhurbaşkanlığı Kararnamesiyle")
S(p, "ADMIN", "Cumhurbaşkanlığı Kararnamesi", "has date", "07.07.2022", "07.07.2022 tarih ve 5777 sayılı")
S(p, "ADMIN", "Cumhurbaşkanlığı Kararnamesi", "has number", "5777", "5777 sayılı Cumhurbaşkanlığı Kararnamesiyle")
S(p, "PEOPLE", "Bülent ARIKAN", "role in the work", "kazı başkanı (başkanlığımda)",
  "başkanlığımda yürütülmekte olan arkeolojik araştırmalar")
S(p, "WORK", "arkeolojik araştırmalar (2024)", "took place between", "01.07–27.09.2024",
  "01.07–27.09.2024 tarihleri arasında gerçekleştirilmiştir")
S(p, "WORK", "kazı sezonu (2024)", "duration", "üç ay", "Üç aya yayılan kazı sezonunda")
S(p, "PEOPLE", "Selda Baybo", "title", "Dr. Öğr. Üy.", "Dr. Öğr. Üy. Selda Baybo")
S(p, "PEOPLE", "Selda Baybo", "affiliation", "Çanakkale On Sekiz Mart Üniversitesi",
  "Selda Baybo (Çanakkale On Sekiz Mart Üniversitesi)")
S(p, "PEOPLE", "Selda Baybo", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Ergin Tatar", "affiliation", "Ege Üniversitesi", "Ergin Tatar (Ege Üniversitesi)")
S(p, "PEOPLE", "Ergin Tatar", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Fatih Mehmet Çongur", "affiliation", "İstanbul Üniversitesi",
  "Fatih Mehmet Çongur (İstanbul Üniversitesi)")
S(p, "PEOPLE", "Fatih Mehmet Çongur", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Onur Kaya", "affiliation", "İstanbul Üniversitesi", "Onur Kaya (İstanbul Üniversitesi)")
S(p, "PEOPLE", "Onur Kaya", "role in the work", "kazı başkanı yardımcısı", "kazı başkanı yardımcıları olarak")
S(p, "PEOPLE", "Selma Akgül", "role in the work", "Kültür ve Turizm Bakanlığı temsilcisi",
  "Selma Akgül de Kültür ve Turizm Bakanlığı temsilcisi olarak")
S(p, "PEOPLE", "Selma Akgül", "office", "Erzurum Müzesi uzmanı", "Erzurum Müzesi uzmanlarından Selma Akgül")
S(p, "PEOPLE", "2024 sezonu çalışmalarına katılanlar", "count (total)", "41 kişi",
  "2024 sezonu çalışmalarına toplam 41 kişi katılmıştır")
S(p, "PEOPLE", "lisans öğrencisi", "count", "22", "22’si lisans öğrencisi")
S(p, "PEOPLE", "lisansüstü öğrencisi", "count", "6", "6’sı lisansüstü öğrencisi")
S(p, "PEOPLE", "öğretim üyesi", "count", "4", "4’ü öğretim üyesi")
S(p, "PEOPLE", "uzman", "count", "9", "9’u ise uzman")
S(p, "PEOPLE", "uzman", "kind of specialist", "arkeolog", "uzman (arkeolog ve jeofizik mühendisi)")
S(p, "PEOPLE", "uzman", "kind of specialist", "jeofizik mühendisi", "uzman (arkeolog ve jeofizik mühendisi)")
S(p, "STRUCT", "bildiri", "work is summarised under headings", "aşağıdaki başlıklar",
  "Yürütülen çalışmalar aşağıdaki başlıklar altında özetlenmiştir")
S(p, "STRUCT", "başlık", "heading reads", "2-KARELAJ ÇALIŞMASI:", "2-KARELAJ ÇALIŞMASI:")
S(p, "WORK", "karelaj", "was prepared in (year)", "1993", "1993 yılında Antalya Müzesi uzmanlarından Sabri Aydal")
S(p, "WORK", "karelaj", "was prepared by", "Sabri Aydal", "Sabri Aydal tarafından hazırlanan karelajın")
S(p, "PEOPLE", "Sabri Aydal", "office", "Antalya Müzesi uzmanı", "Antalya Müzesi uzmanlarından Sabri Aydal")
S(p, "WORK", "karelaj", "has digital version", "dijital hali", "karelajın dijital hali bulunmadığından", neg=True)
S(p, "WORK", "Höyüğün karelajı", "was made digital", "dijital hale getirilmiştir",
  "Höyüğün karelajı 1993 yılındaki plana sadık kalınarak dijital hale getirilmiştir")
S(p, "WORK", "Höyüğün karelajı", "digitising follows", "1993 yılındaki plan", "1993 yılındaki plana sadık kalınarak")
S(p, "WORK", "açma kodları", "result of digitising", "birlik sağlanmıştır", "Böylece açma kodlarında birlik sağlanmıştır")
S(p, "PLACE", "Höyüğün 1993 kotları ile modern ölçümler", "difference between", "yaklaşık 30 metre",
  "modern ölçümler arasında yaklaşık 30 metre farklılık olduğu tespit edilmiştir")
S(p, "PLACE", "Höyüğün kotları", "were measured in (year)", "1993", "Höyüğün 1993 yılında ölçülen kotları")
S(p, "WORK", "1993 kotları", "continue to be used", "kullanılmaya devam edilmektedir",
  "1993 kotları kullanılmaya devam edilmektedir")
S(p, "WORK", "1993 kotları", "reason for use", "önceki kazı sezonlarının verisiyle uyumu sağlamak",
  "Önceki kazı sezonlarının verisiyle uyumu sağlamak")
S(p, "STRUCT", "başlık", "heading reads", "3-JEOFİZİK ETÜTLERİ:", "3-JEOFİZİK ETÜTLERİ:")
S(p, "WORK", "Bülent Arıkan başkanlığındaki kazılar", "first season", "2022",
  "Başkanlığım altında yürütülen kazıların ilk sezonu olan 2022")
S(p, "WORK", "yer radarı çalışmaları", "carried out since", "2022 yılından beri", "2022 yılından beri")
S(p, "WORK", "yer radarı çalışmaları", "were carried out at", "Höyüğün üst düzlüğü", "Höyüğün üst düzlüğünde")
S(p, "WORK", "yer radarı çalışmaları", "were carried out by", "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri",
  "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri ve öğrencileri")
S(p, "WORK", "yer radarı çalışmaları", "were carried out by", "İTÜ Jeofizik Mühendisliği Bölümü öğrencileri",
  "İTÜ Jeofizik Mühendisliği Bölümü öğretim üyeleri ve öğrencileri")
S(p, "WORK", "yer radarı çalışması (2022 sezonu)", "area scanned", "Merkezi Kilise ile Kuzey Yamaç açmaları arası",
  "2022 sezonunda Merkezi Kilise ile Kuzey Yamaç açmaları arası")
S(p, "WORK", "yer radarı çalışması (2023 sezonu)", "area scanned", "Merkezi Kilise ile Batı Kilise arası",
  "2023 sezonunda ise Merkezi Kilise ile Batı Kilise arası taranmıştı")
S(p, "INTERP", MK, "was used as", "Manastır", "Manastır olarak kullanılan bu yapıya")
S(p, "BUILT", "Manastır'a ait binaların kalıntıları", "lie at (side of Merkezi Kilise)", "kuzey",
  "Merkezi Kilise’nin kuzey ve batısında")
S(p, "BUILT", "Manastır'a ait binaların kalıntıları", "lie at (side of Merkezi Kilise)", "batı",
  "Merkezi Kilise’nin kuzey ve batısında")
S(p, "MEASURE", "Manastır'a ait binaların kalıntıları", "depth below surface (top)", "yaklaşık bir metre",
  "kalıntıları yüzeyin yaklaşık bir metre altında")
S(p, "MEASURE", "Manastır'a ait binaların kalıntıları", "extend to depth", "1,5 metre",
  "1,5 metre derinliğe kadar uzandığı tespit edilmiştir")
S(p, "FIGURE", "Manastır'a ait binaların kalıntıları", "is shown in figure", "Resim: 1", "tespit edilmiştir (Resim: 1)")
S(p, "PEOPLE", "Bülent ARIKAN", "title", "Prof. Dr.", "Prof. Dr. Bülent ARIKAN")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (university)", "İstanbul Teknik Üniversitesi",
  "Prof. Dr. Bülent ARIKAN; İstanbul Teknik Üniversitesi")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (institute)", "Avrasya Yer Bilimleri Enstitüsü", "Avrasya Yer Bilimleri Enstitüsü")
S(p, "PEOPLE", "Bülent ARIKAN", "affiliation (department)", "Evrim ve Ekosistem ABD", "Evrim ve Ekosistem ABD")
S(p, "PEOPLE", "Bülent ARIKAN", "address", "Maslak, Sarıyer-İstanbul/TÜRKİYE", "Maslak, Sarıyer-İstanbul/TÜRKİYE")
S(p, "PEOPLE", "Bülent ARIKAN", "identifier (ORCID)", "0000-0003-2734-843X", "ORCID: 0000-0003-2734-843X")

# ---------------------------------------------------------------- page 280
p = 280
S(p, "STRUCT", "sayfa üst başlığı", "page header reads", "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ",
  "KÜLTÜR VARLIKLARI VE MÜZELER GENEL MÜDÜRLÜĞÜ")
S(p, "WORK", "yer radarı çalışması (2024 sezonu)", "area covered", "Merkezi Kilise’nin güneyi",
  "yer radarı çalışması Merkezi Kilise’nin güneyini kapsayacak şekilde gerçekleştirilmiştir")
S(p, "WORK", "yer radarı çalışması (2024 sezonu)", "was announced in", "2024 sezonu çalışma programı",
  "2024 sezonu çalışma programımızda belirttiğimiz yer radarı çalışması")
S(p, "DATE", MK, "in use from", "Erken Bizans", "Erken Bizans’tan başlayarak")
S(p, "DATE", MK, "in use until", "Orta Bizans Dönemi sonu", "Orta Bizans Dönemi sonuna kadar kullanımda kalan")
S(p, "BUILT", MK, "kind", "manastır yapısı", "kalan bu manastır yapısının")
S(p, "WORK", "Merkezi Kilise'nin çevresi", "was scanned by yer radarı", "neredeyse tamamen taranmıştır",
  "çevresi yer radarı ile neredeyse tamamen taranmıştır", hedge="neredeyse")
S(p, "BUILT", "Resim 1'de görülen yapılar", "continue toward", "batı", "yapıların batı ve güney yönlerinde de devam ettiği")
S(p, "BUILT", "Resim 1'de görülen yapılar", "continue toward", "güney", "yapıların batı ve güney yönlerinde de devam ettiği")
S(p, "WORK", "Resim 1'de görülen yapıların devamı", "was detected by", "arazide yapılan ön çalışmalar",
  "Arazide yapılan ön çalışmalar sonucunda")
S(p, "FIGURE", "yapılar (yer radarı)", "is shown in figure", "Resim 1", "Resim 1’de görülen yapıların")
S(p, "INTERP", "Manastır çevresindeki birçok mekân", "is interpreted as", "Manastır’a hizmet veren mekânlar",
  "birçok mekânın da Manastır’a hizmet verdiği yer radarı sonuçlarından anlaşılmaktadır",
  hedge="yer radarı sonuçlarından anlaşılmaktadır")
S(p, "WORK", "Höyük düzlüğü", "was scanned by yer radarı (2024)", "neredeyse tamamı",
  "Höyük düzlüğünün neredeyse tamamı taranmıştır", hedge="neredeyse")
S(p, "WORK", "yer radarı yöntemi", "gives sound results in sloped areas", "eğimli alanlarda sağlıklı sonuç",
  "eğimli alanlarda sağlıklı sonuç alınamaması", neg=True)
S(p, "WORK", "yer radarı", "depth of effect", "yüzeyin sadece birkaç metre altı",
  "yer radarının yüzeyin sadece birkaç metre altına etki etmesi")
S(p, "WORK", "jeofizik çalışmaları", "need raised", "farklı bir yöntem kullanılması",
  "farklı bir yöntem kullanılması gündeme gelmiştir")
S(p, "WORK", "Hacımusalar Höyük kazıları", "carried on since", "1994", "1994 yılından beri sürdürülen kazılarda")
S(p, "MEASURE", "kültür dolgusu (Hacımusalar Höyük)", "thickness", "yaklaşık 12 metre",
  "yaklaşık 12 metre kültür dolgusu olduğu tespit edilen")
S(p, "WORK", HH, "method decided", "Elektrik Rezistivite (Özdirenç) Tomografi (ERT)",
  "Elektrik Rezistivite (Özdirenç) Tomografi (ERT) yönteminin kullanılmasına karar verilmiştir")
S(p, "WORK", "ERT yöntemi", "aim", "kültür dolgusunun kalınlığını tespit etmek", "hem kültür dolgusunun kalınlığını")
S(p, "WORK", "ERT yöntemi", "aim", "kültürel-jeolojik tabaka ayrımlarını tespit etmek",
  "kültürel-jeolojik tabaka ayrımlarını tespit etmek")
S(p, "WORK", "ERT yöntemi", "aim", "Höyüğün tabanındaki jeolojik yapıyı açığa çıkarmak",
  "Höyüğün tabanındaki jeolojik yapıyı açığa çıkarmak")
S(p, "ADMIN", "ERT çalışması", "was funded by", "KTB ödeneği", "KTB ödeneğimizden yapılan hizmet alımıyla")
S(p, "ADMIN", "ERT çalışması", "was obtained by", "hizmet alımı", "hizmet alımıyla gerçekleştirilen ERT çalışması")
S(p, "WORK", "ERT profilleri (hat)", "count", "10", "10 profil (hat) üzerinde gerçekleştirilmiştir")
S(p, "WORK", "ERT profilleri (hat)", "position", "Höyüğün tamamını farklı yönlerden kesen",
  "Höyüğün tamamını farklı yönlerden kesen 10 profil")
S(p, "FIGURE", "ERT profilleri (hat)", "is shown in figure", "Resim: 2", "(Resim: 2)")
S(p, "WORK", "ERT hatları", "measures (length, range)", "yaklaşık 10 metre ile 240 metre arası",
  "Uzunlukları yaklaşık 10 metre ile 240 metre arasında değişen hatlar")
S(p, "WORK", "elektrodlar", "spacing", "birer metre", "birer metre arayla yerleştirilen elektrodlardan")
S(p, "WORK", "ERT çalışması", "is based on", "elektrodlardan verilip alınan elektrik akımı sonuçları",
  "elektrodlardan verilip alınan elektrik akımı sonuçlarına")
S(p, "WORK", "ERT çalışması", "aims reached", "amaçlanan tüm hedeflere ulaşılmıştır",
  "yukarıda amaçlanan tüm hedeflere ulaşılmıştır")
S(p, "FIGURE", "ERT çalışmasının sonuçları", "is shown in figure", "Resim: 3",
  "ERT çalışmasının sonuçlarına göre (Resim: 3)")
S(p, "PLACE", "Hacımusalar Höyük yukarı düzlüğü", "elevation", "yaklaşık 1081 m", "yaklaşık 1081 m rakımda olan")
S(p, "WORK", "ERT kesiti", "depth scanned and mapped", "40 metre",
  "yukarı düzlüğünden itibaren 40 metrelik bir kesit taranmış")
S(p, "BUILT", "birinci profil (ERT)", "count of stratigraphic units", "toplam yedi stratigrafik birim",
  "toplam yedi stratigrafik birime işaret etmektedir")
S(p, "BUILT", "birinci profildeki stratigrafik birimler", "kind", "arkeolojik ve jeolojik", "arkeolojik ve jeolojik olarak toplam yedi")
S(p, "DESCR", "birinci profil (ERT)", "is taken as", "örnek olarak ele alınabilecek",
  "örnek olarak ele alınabilecek birinci profildeki sonuçlar")
S(p, "BUILT", "elektriğe yüksek dirençli (arkeolojik) katmanlar", "present down to depth", "Höyük yüzeyinden itibaren 6 metre",
  "Höyük yüzeyinden itibaren 6 metre derinliğe kadar elektriğe yüksek dirençli (arkeolojik) katmanların")
S(p, "BUILT", "elektriğe orta direnç gösteren katmanlar", "lies below", "yüksek dirençli tabaka",
  "bu tabakanın altında elektriğe orta direnç gösteren katmanların")
S(p, "INTERP", "elektriğe orta direnç gösteren katmanlar", "is interpreted as", "arkeolojik veya jeolojik (kil, ıslak kil, vb.)",
  "katmanların arkeolojik veya jeolojik (kil, ıslak kil, vb.) olabileceği", hedge="olabileceği")
S(p, "BUILT", "elektriğe çok düşük direnç gösteren jeolojik katmanlar (su, kil)", "present from depth", "yüzeyden 15 metre derinlikten itibaren",
  "yüzeyden 15 metre derinlikten itibaren ise elektriğe çok düşük direnç gösteren jeolojik katmanların (su, kil)")
S(p, "BUILT", "Höyüğün Ova tabanı ile buluştuğu alanlar", "archaeological layer found", "arkeolojik katman",
  "herhangi bir arkeolojik katmana rastlanmamıştır", neg=True)
S(p, "MEASURE", "arkeolojik katmanlar (Hacımusalar Höyük)", "reach depth", "yaklaşık olarak 11 metre",
  "arkeolojik katmanlar yaklaşık olarak 11 metre derinliğe kadar ulaşmakta")
S(p, "BUILT", "arkeolojik katmanların ilk altı metresi", "resistance to electricity", "çok yüksek direnç",
  "bunun ilk altı metresi elektriğe karşı çok yüksek direnç göstermektedir")
S(p, "INTERP", "0-6 metre aralığındaki arkeolojik katmanlar", "is made of", "taş gibi malzemeler",
  "0-6 metre aralığındaki arkeolojik katmanların taş gibi malzemelerden oluşması beklenmektedir", hedge="beklenmektedir")
S(p, "INTERP", "6-12 metre arasındaki katmanlar", "nature determined", "niteliği tam belirlenememiştir",
  "niteliği elektriğe gösterdikleri orta direnç nedeniyle tam belirlenememiştir", neg=True)
S(p, "BUILT", "6-12 metre arasındaki katmanlar", "resistance to electricity", "orta direnç",
  "elektriğe gösterdikleri orta direnç nedeniyle")
S(p, "INTERP", "6-12 metre arasındaki katmanlar", "is interpreted as", "arkeolojik (kerpiç, vb.) ve jeolojik (ıslak kil, vb.) olguların birlikte bulunduğu seviyeler",
  "hem arkeolojik (kerpiç, vb.) hem de jeolojik (ıslak kil, vb.) olguların birlikte bulunduğu seviyeler olabileceği değerlendirilmektedir",
  hedge="olabileceği değerlendirilmektedir")
S(p, "BUILT", "12 metreden sonraki seviyeler", "resistance to electricity", "çok düşük direnç",
  "12 metreden sonraki çok düşük direnç seviyelerine")
S(p, "INTERP", "yüzeyden 12 metre derinlikten itibaren", "archaeological layers present", "arkeolojik katmanlar",
  "Yüzeyden 12 metre derinlikten itibaren elektriğe çok düşük dirençli katmanların (su, kil) varlığı nedeniyle",
  hedge="düşünülmektedir", neg=True)

# ---------------------------------------------------------------- page 281
p = 281
S(p, "INTERP", "sağlam ele geçirilebilecek arkeolojik katmanlar", "depth below surface", "8-9 metre",
  "arkeolojik katmanların yüzeyden 8-9 metre derinlikte olabileceği", hedge="olabileceği")
S(p, "INTERP", "8-9 metreden sonra bulunacak arkeolojik katmanlar", "preservation", "sorunlu",
  "korunmasının alttaki ıslak jeolojik yapı nedeniyle sorunlu olabileceği", hedge="olabileceği")
S(p, "INTERP", "yüzeyin 12 metre altı", "contains only", "su kaynağı ve bununla ilişkili jeolojik katmanlar",
  "sadece su kaynağı ve bununla ilişkili jeolojik katmanların bulunabileceği", hedge="bulunabileceği")
S(p, "DATE", "Hacımusalar Höyüğün ilk yerleşildiği dönem", "is dated to", "Geç Kalkolitik Dönem",
  "şu andaki bulgulara dayanarak Geç Kalkolitik Dönem’de", hedge="şu andaki bulgulara dayanarak")
S(p, "DATE", "Geç Kalkolitik Dönem", "is dated to", "y. MÖ 3500", "(y. MÖ 3500)", hedge="y.")
S(p, "INTERP", "Hacımusalar Höyüğün konum tercihi", "is interpreted as", "su kaynağı yakınında olma isteği",
  "su kaynağı yakınında olma isteğine dayandırılabileceğini göstermektedir", hedge="dayandırılabileceğini")
S(p, "WORK", "paleo-coğrafya çalışmaları", "planned for", "önümüzdeki yıllar", "Önümüzdeki yıllarda")
S(p, "WORK", "paleo-coğrafya çalışmaları", "planned at", "Elmalı Ovası geneli",
  "Elmalı Ovası genelinde yürütülecek paleo-coğrafya çalışmalarında")
S(p, "WORK", "paleo-coğrafya çalışmaları", "will clarify", "Höyüğün iskân gördüğü dönemlerde su tablasının ne kadar yüksek olduğu",
  "Höyüğün iskân gördüğü dönemlerde su tablasının ne kadar yüksek olduğu")
S(p, "WORK", "paleo-coğrafya çalışmaları", "will clarify", "göllerin arkeolojik dönemlerde Höyük ile olan ilişkileri",
  "göllerin arkeolojik dönemlerde Höyük ile olan ilişkileri açıklığa kavuşacaktır")
S(p, "PLACE", "göller", "lie", "Höyük civarında", "Höyük civarındaki göllerin")
S(p, "HISTORY", "Höyük civarındaki göller", "were drained in", "1970’ler", "1970’lerde kurutulan göllerin")
S(p, "FIGURE", "birinci ERT hattı", "is shown in figure", "Resim 3b", "Resim 3b’de gösterilen birinci ERT hattının")
S(p, "BUILT", "1 No.lu katman", "position on first ERT line", "20. ve 40. metreleri arası",
  "birinci ERT hattının 20. ve 40. metreleri arasında")
S(p, "BUILT", "1 No.lu katman", "resistance to electricity", "çok yüksek direnç",
  "çok yüksek direnç gösteren 1 No.lu katman işaretlenmiştir")
S(p, "WORK", "sondajlar (Güney Yamaç)", "were made in", "önceki kazı dönemleri",
  "önceki kazı dönemlerinde Güney Yamaç’ta yapılan sondajlardan")
S(p, "BUILT", "kireçtaşından duvarlar (Güney Yamaç)", "position", "birinci ERT hattının hemen batısı",
  "bu hattın hemen batısında ve doğusunda")
S(p, "BUILT", "kireçtaşından duvarlar (Güney Yamaç)", "position", "birinci ERT hattının hemen doğusu",
  "bu hattın hemen batısında ve doğusunda")
S(p, "DATE", "kireçtaşından duvarlar (Güney Yamaç)", "is dated to", "Helenistik/Roma dönemleri",
  "Helenistik/Roma dönemlerine ait olabilecek", hedge="olabilecek")
S(p, "BUILT", "duvarlar (Güney Yamaç)", "is made of", "kireçtaşı", "kireçtaşından duvarlar")
S(p, "BUILT", "duvarlar (Güney Yamaç)", "working of stone", "poligonal şekilde işlenerek yüzeyi düzeltilmiş",
  "poligonal şekilde işlenerek yüzeyi düzeltilmiş kireçtaşından duvarlar")
S(p, "BUILT", "duvar blokları (Güney Yamaç)", "shape", "dikdörtgen prizma",
  "dikdörtgen prizma şeklinde duvar blokları tespit edilmiştir")
S(p, "WORK", "Güney Yamaç’taki açma (2023 sezonu)", "exposed", "duvarın bir kısmı daha",
  "2023 sezonunda Güney Yamaç’taki açmada bu duvarın bir kısmı daha açığa çıkarılmıştır")
S(p, "BUILT", "savunma sistemi", "position", "Höyüğün güney yamacını doğudan batıya çevreleyen",
  "Höyüğün güney yamacını doğudan batıya çevreleyen")
S(p, "DATE", "savunma sistemi", "is dated to", "Helenistik/Roma dönemleri",
  "Helenistik/Roma dönemlerine tarihlenebilecek bir savunma sisteminin", hedge="tarihlenebilecek")
S(p, "DATE", "savunma sistemi", "dating is based on", "yapı üslubu", "yapı üslubu açısından")
S(p, "INTERP", "Güney Yamaç duvarları", "is interpreted as", "savunma sistemi", "bir savunma sisteminin varlığı bilinmektedir")
S(p, "MEASURE", "savunma sistemi", "extends further (from south slope to north)", "20 metre",
  "Höyüğün güney yamacından kuzeye doğru 20 metre daha uzandığı tespit edilmiştir")
S(p, "PLACE", "savunma sisteminin uzandığı alan", "is", "Höyüğün en düşük kotta olduğu nokta",
  "Bu alan, Höyüğün en düşük kotta olduğu")
S(p, "PLACE", "savunma sisteminin uzandığı alan", "access", "yaya olarak Höyüğün yukarı düzlüğüne rahatça ulaşılabilecek nokta",
  "yaya olarak Höyüğün yukarı düzlüğüne rahatça ulaşılabilecek noktadır")
S(p, "PLACE", "Höyüğün üstüne çıkmak için kullanılan yol", "is located in", "bu alan (güney yamaç)",
  "Höyüğün üstüne çıkmak için kullanılan yol burada yer almaktadır")
S(p, "PLACE", "Höyüğün güney kısmı", "topography", "yükselen bir topografya",
  "Höyüğün güney kısmında yükselen bir topografya karşımıza çıkmaktadır")
S(p, "INTERP", "Hacımusalar Höyüğün güney yamacı", "is interpreted as having", "giriş alanı veya anıtsal kapı yapısı",
  "bir giriş alanı veya anıtsal kapı yapısının bulunabileceğini düşündürmektedir",
  hedge="bulunabileceğini düşündürmektedir")
S(p, "MEASURE", "giriş alanı veya anıtsal kapı yapısı", "measures (length)", "yaklaşık 20 metre",
  "yaklaşık 20 metre uzunluğa sahip", hedge="bulunabileceğini düşündürmektedir")
S(p, "INTERP", "giriş alanı veya anıtsal kapı yapısı", "is made of", "taş malzeme",
  "olasılıkla taş malzemeden oluşan", hedge="olasılıkla")
S(p, "INTERP", "giriş alanı veya anıtsal kapı yapısı", "interpretation is based on", "Höyük topografyası, savunma sistemi ve ERT verisi",
  "ERT verisi ile birlikte değerlendirildiğinde")
S(p, "WORK", "çift yöntemli jeofizik", "was obtained by", "hizmet alımı",
  "çift yöntemli jeofizik (yer radarı ve yer manyetik ölçümleri) hizmeti alınmıştır")
S(p, "WORK", "çift yöntemli jeofizik", "method", "yer radarı", "(yer radarı ve yer manyetik ölçümleri)")
S(p, "WORK", "çift yöntemli jeofizik", "method", "yer manyetik ölçümleri", "(yer radarı ve yer manyetik ölçümleri)")
S(p, "WORK", "çift yöntemli jeofizik", "was done after", "ERT çalışması", "ERT çalışması sonrasında yapılan değerlendirmelerde")
S(p, "WORK", "çift yöntemli jeofizik", "question to answer", "herhangi bir yapı bulunup bulunmadığı",
  "herhangi bir yapı bulunup bulunmadığına ilişkin sorular cevaplandırmak için")
S(p, "PLACE", "çift yöntemli jeofizik alanı", "is located", "güney yamacın batısındaki yükseltinin ardında",
  "güney yamacın batısındaki yükseltinin ardında")
S(p, "PLACE", "çift yöntemli jeofizik alanı", "is located", "Höyük yukarı düzlüğüne doğru inildiği nokta",
  "Höyük yukarı düzlüğüne doğru inildiği noktada")
S(p, "PLACE", "çift yöntemli jeofizik alanı", "is located", "anıtsal girişin ardında",
  "olasılıkla anıtsal girişin ardında", hedge="olasılıkla")
S(p, "MEASURE", "çift yöntemli jeofizik alanı", "[unclear] area", "2000 m2",
  "seçilen yaklaşım 2000 m2 alanın", hedge="yaklaşım [unclear: yaklaşık?]")
S(p, "PLACE", "çift yöntemli jeofizik alanı", "topography", "eğimli bir topografya",
  "alanın eğimli bir topografyaya sahip olması nedeniyle")
S(p, "WORK", "iki yöntemin birlikte kullanılması", "reason", "farklı yapı malzemelerinin tanınabilmesi",
  "farklı yapı malzemelerinin tanınabilmesi amacıyla bu iki yöntemin birlikte kullanılması tercih edilmiştir")
S(p, "BUILT", "arkeolojik yapı kalıntıları (çift yöntemli jeofizik alanı)", "found from depth", "yüzeyin 0.5 metre altından itibaren",
  "yüzeyin 0.5 metre altından itibaren plan veren arkeolojik yapı kalıntılarına rastlanmıştır")
S(p, "BUILT", "arkeolojik yapı kalıntıları (çift yöntemli jeofizik alanı)", "gives plan", "plan veren",
  "plan veren arkeolojik yapı kalıntılarına")
S(p, "INTERP", "bazı yapılar (çift yöntemli jeofizik alanı)", "is interpreted as", "fırın veya ocak gibi yoğun ateş kullanımı gösteren mekanlar",
  "fırın veya ocak gibi yoğun ateş kullanımı gösteren mekanlar olabileceği değerlendirilmiştir",
  hedge="olabileceği değerlendirilmiştir")
S(p, "INTERP", "fırın veya ocak yorumu", "is based on", "yer manyetik yöntem sonuçları",
  "yer manyetik yöntemle tarandığında verdiği sonuçlar")

# ---------------------------------------------------------------- page 282
p = 282
S(p, "STRUCT", "başlık", "heading reads", "4- ARKEOLOJİK KAZILAR:", "4- ARKEOLOJİK KAZILAR:")
S(p, "WORK", "arkeolojik kazı çalışmaları (2024)", "took place at", "Kuzey Yamaç alanı", "Kuzey Yamaç alanında")
S(p, "PEOPLE", "Kuzey Yamaç kazısı arkeologları", "count", "beş arkeolog", "Kuzey Yamaç alanında beş arkeolog")
S(p, "PEOPLE", "Kuzey Yamaç kazısı", "took part", "öğrenciler", "beş arkeolog, öğrenciler ve")
S(p, "ADMIN", "Kuzey Yamaç kazısı işçileri", "count", "iki işçi", "TYP bünyesinde çalıştırılan iki işçi")
S(p, "ADMIN", "Kuzey Yamaç kazısı işçileri", "were employed under", "TYP", "TYP bünyesinde çalıştırılan iki işçi")
S(p, "WORK", "Kuzey Yamaç kazısı (2024)", "took place between", "16.07.2024–26.08.2024",
  "16.07.2024–26.08.2024 tarihleri arasında gerçekleştirilmiştir")
S(p, "MEASURE", "Merkezi Kilise 1. Etap kazı alanı", "area", "333 m2", "Merkezi Kilise 1. Etap 333 m2 alanda")
S(p, "WORK", "Merkezi Kilise 1. Etap kazısı", "excavated volume", "120 m3", "120 m3 hafriyat kaldırılan arkeolojik kazı")
S(p, "ADMIN", "Merkezi Kilise 1. Etap kazısı", "was carried out under", "GMP", "GMP bünyesinde")
S(p, "PEOPLE", "Merkezi Kilise 1. Etap kazısı arkeologları", "count", "iki arkeolog", "GMP bünyesinde iki arkeolog")
S(p, "PEOPLE", "Merkezi Kilise 1. Etap kazısı mimarı", "count", "bir mimar", "bir mimar ve altı işçinin katılımıyla")
S(p, "ADMIN", "Merkezi Kilise 1. Etap kazısı işçileri", "count", "altı işçi", "bir mimar ve altı işçinin katılımıyla")
S(p, "WORK", "Merkezi Kilise 1. Etap kazısı", "took place between", "29.08.2024–27.09.2024",
  "29.08.2024–27.09.2024 tarihleri arasında")
S(p, "STRUCT", "başlık", "heading reads", "4.1 KUZEY YAMAÇ", "4.1 KUZEY YAMAÇ")
S(p, "PLACE", "P2 noktası (Kuzey Yamaç)", "elevation of Höyük surface", "1055.37 m",
  "P2 noktasında Höyük yüzeyi 1055.37 m kottadır")
S(p, "BUILT", "Demir Çağı sur duvarı", "is located in", "C4a8 açması", "C4a8 açmasında yapılan çalışmalarda")
S(p, "DATE", "sur duvarı (C4a8)", "is dated to", "Demir Çağı", "Demir Çağı sur duvarı")
S(p, "BUILT", "Demir Çağı sur duvarı", "foundation is made of", "taş", "taş temel üzerinde kerpiçle inşa edilen")
S(p, "BUILT", "Demir Çağı sur duvarı", "is built of", "kerpiç", "taş temel üzerinde kerpiçle inşa edilen")
S(p, "WORK", "Demir Çağı sur duvarı", "was removed along", "beş metrelik bir hat", "beş metrelik bir hat boyunca kaldırılmış")
S(p, "WORK", "Demir Çağı sur duvarının kaldırılması", "was done in", "önceki sezonlar", "Önceki sezonlarda C4a8")
S(p, "BUILT", "ETÇ yapı kalıntıları (C4a8)", "lies below", "Demir Çağı sur duvarı", "bunun altında yapılan kazılarda")
S(p, "DATE", "yapı kalıntıları (C4a8)", "is dated to", "Erken Tunç Çağı (ETÇ)",
  "Erken Tunç Çağı’na (ETÇ) ait yapı kalıntılarına")
S(p, "PLACE", "ETÇ yapı kalıntıları (C4a8)", "elevation", "yaklaşık 1049 m", "(yaklaşık 1049 m kotta)")
S(p, "MEASURE", "ETÇ yapı kalıntılarına ulaşılan alan (C4a8)", "measures", "2x2 metre", "çok dar bir alanda (2x2 metre)")
S(p, "WORK", "Kuzey Yamaç açmaları", "count opened since 1994", "bir düzineden fazla",
  "Kuzey Yamaç’ta açılan bir düzineden fazla açmada")
S(p, "WORK", "Kuzey Yamaç açmaları", "ETÇ levels reached", "ETÇ seviyeleri",
  "yeterince derinleşilmediğinden ETÇ seviyelerine inilememiştir", neg=True)
S(p, "WORK", "Kuzey Yamaç açmaları", "excavated deep enough", "yeterince derinleşilmediğinden",
  "yeterince derinleşilmediğinden", neg=True)
S(p, "WORK", "Kuzey Yamaç kazıları (2024 sezonundan itibaren)", "aim", "C4a7-C4b7 açmalarında derinleşerek ETÇ seviyelerine doğru devam etmek",
  "C4a7-C4b7 açmalarında derinleşerek ETÇ seviyelerine doğru devam ederken")
S(p, "WORK", "C4a7-C4b7 açmaları", "were started in", "2023 sezonu", "2023 sezonunda başlatılan C4a7-C4b7 açmalarında")
S(p, "PLACE", "C5b1 ve C5b2 açmaları", "were left at", "en yüksek kot", "en yüksek kotta bırakılan C5b1 ve C5b2")
S(p, "WORK", "Kuzey Yamaç kazıları (2024 sezonundan itibaren)", "aim", "C5b1 ve C5b2 açmalarını C4b10 ve C4c10 açmalarının kotlarına indirmek",
  "bunları C4b10 ve C4c10 açmalarının bulunduğu kotlara indirmektir")
S(p, "WORK", "yedi açma (C4b9 ile birlikte)", "will be lowered to", "C4b8 seviyesi",
  "yedi açmanın tamamı, C4b8 seviyesine indirilecektir")
S(p, "WORK", "yedi açmanın C4b8 seviyesine indirilmesi", "planned for", "yakın gelecek", "Yakın gelecekte C4b9 ile birlikte")
S(p, "INTERP", "C4a8 açmasındaki ETÇ katlarının devamı", "expected at depth", "C4b8 açmasının şu anki seviyesinden yaklaşık 1.5 metre aşağıda",
  "ETÇ katlarının devamının yakalanacağı değerlendirilmektedir", hedge="değerlendirilmektedir")
S(p, "FIGURE", "Kuzey Yamaç açmaları", "is shown in figure", "Resim: 4", "değerlendirilmektedir (Resim: 4)")
S(p, "WORK", "C4a7-C4b7 açmaları (2024 kazısı)", "began with removal of", "dağınık duvar kalıntısı", "dağınık duvar kalıntısı ve çöp çukurunun")
S(p, "WORK", "C4a7-C4b7 açmaları (2024 kazısı)", "began with removal of", "çöp çukuru", "dağınık duvar kalıntısı ve çöp çukurunun")
S(p, "WORK", "dağınık duvar kalıntısı ve çöp çukuru (C4a7-C4b7)", "were detected and documented in", "2023 sezonu",
  "sezonunda tespit edilen, belgelenen dağınık duvar kalıntısı")
S(p, "WORK", "açma (C4b7)", "was extended toward", "C4b7’nin güneyi", "açmanın C4b7’nin güneyine doğru")
S(p, "MEASURE", "açma genişletmesi (C4b7)", "measures", "30 cm", "güneyine doğru 30 cm genişletilmesine karar verilmiş")
S(p, "BUILT", "duvar (C4b7 güney genişletmesi)", "kind", "duvar", "bir duvar 4.3 metre uzunlukta yakalanmıştır")
S(p, "BUILT", "duvar (C4b7 güney genişletmesi)", "quality", "oldukça düzgün", "burada oldukça düzgün")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (width)", "iki sıra", "iki sıra genişliğinde tek sıra yüksekliğinde")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (height)", "tek sıra", "iki sıra genişliğinde tek sıra yüksekliğinde")
S(p, "MEASURE", "duvar (C4b7 güney genişletmesi)", "measures (length)", "4.3 metre", "4.3 metre uzunlukta yakalanmıştır")
S(p, "MEASURE", "C4a7-C4b7 alanı (genişleme sonrası)", "measures", "neredeyse 5x8 metre",
  "neredeyse 5x8 metre boyutlarına gelen bu alan", hedge="neredeyse")
S(p, "WORK", "C4a7-C4b7 alanı", "excavated only in", "C4a7", "sadece C4a7 içinde (5x5 m) kazı yapılmıştır")
S(p, "MEASURE", "C4a7 açması", "measures", "5x5 m", "C4a7 içinde (5x5 m)")
S(p, "WORK", "sadece C4a7'de kazı yapılması", "reason", "iş gücü ve zamandan tasarruf etmek", "iş gücü ve zamandan tasarruf etmek")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "consistency", "oldukça sert", "bu açmada oldukça sert")
S(p, "INTERP", "kerpiç dolgu (C4a7)", "is interpreted as", "Demir Çağı sur duvarından dökülen",
  "Demir Çağı sur duvarından döküldüğü değerlendirilen", hedge="değerlendirilen")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "extends to", "neredeyse C4b7 açma sınırına kadar",
  "neredeyse C4b7 açma sınırına kadar uzayan kerpiç dolgu", hedge="neredeyse")
S(p, "WORK", "kerpiç dolgu (C4a7)", "excavation began in", "2023", "2023 yılında bu açmada")
S(p, "WORK", "kerpiç dolgu (C4a7)", "removal continued in", "2024 sezonu",
  "kerpiç dolgunun kaldırılması işlemine devam edilmiştir")
S(p, "WORK", "C4a7 açması (2024 kazıları)", "deepened by", "yaklaşık 1.3 metre", "yaklaşık 1.3 metre derinleşilmiş")
S(p, "BUILT", "kerpiç dolgu (C4a7)", "continues", "dağınık halde", "kerpiç dolgunun dağınık halde devam ettiği gözlemlenmiştir")
S(p, "MEASURE", "Demir Çağı sur duvarı", "measures (width)", "3 metreyi aşkın",
  "Demir Çağı sur duvarının genişliğinin 3 metreyi aşkın olduğu", hedge="düşünüldüğünde")
S(p, "INTERP", "kerpiç üst yapı (sur duvarı)", "collapsed toward", "duvarın iç kısmı (güneyi)",
  "kerpiç üst yapının duvarın iç kısmına (güneyine) yıkıldığı düşünülmektedir", hedge="düşünülmektedir")
S(p, "WORK", "kerpiç duvar enkazı (C4a7)", "still to be excavated", "yaklaşık 1.5 metre daha",
  "yaklaşık 1.5 metre daha kerpiç duvar enkazı kazılacağı", hedge="düşünülmektedir")
S(p, "FIND", "iyi korunmuş kerpiç parçası (C4a7 kerpiç üst yapı enkazı)", "was found", "ele geçmemesi",
  "iyi korunmuş bir kerpiç parçasının ele geçmemesi nedeniyle", neg=True)
S(p, "WORK", "sondaj (C4a6)", "was opened in", "C4a6 açması", "C4a6 açmasına kuzeybatı açma sınırından")
S(p, "PLACE", "sondaj (C4a6)", "position", "kuzeybatı açma sınırından", "kuzeybatı açma sınırından")
S(p, "MEASURE", "sondaj (C4a6)", "measures (length)", "2 metre", "2 metre uzunluğunda")
S(p, "MEASURE", "sondaj (C4a6)", "measures (width)", "1 metre", "1 metre genişliğinde bir sondaj açılmıştır")
S(p, "WORK", "sondaj (C4a6)", "purpose", "kerpiç üst yapı enkazının uzantısının tespit edilebilmesi",
  "kerpiç üst yapı enkazının uzantısının tespit edilebilmesi için")
S(p, "FIND", "sondaj (C4a6)", "notable find was found", "kayda değer bir buluntu",
  "Bu sondajın kazısı sırasında kayda değer bir buluntu", neg=True)

# ---------------------------------------------------------------- page 283
p = 283
S(p, "BUILT", "sondaj (C4a6)", "count of elements observed", "iki unsur", "iki unsur gözlemlenmiştir")
S(p, "FIND", "kerpiç blok", "kind", "kerpiç blok", "bir kerpiç blok in situ")
S(p, "MEASURE", "kerpiç blok", "[unclear] measures (text and caption of Resim 5 differ)", "35x3x12 cm",
  "yaklaşık boyutları 35x3x12 cm olan", hedge="yaklaşık")
S(p, "FIND", "kerpiç blok", "position", "in situ (yerinde)", "in situ (yerinde)")
S(p, "FIND", "kerpiç blok", "condition", "iyi korunmuş", "iyi korunmuş olarak")
S(p, "FIND", "kerpiç blok", "depth below surface", "yaklaşık 1 metre", "yüzeyin yaklaşık 1 metre altında tespit edilmiştir",
  hedge="yaklaşık")
S(p, "FIGURE", "kerpiç blok", "is shown in figure", "Resim: 5", "tespit edilmiştir (Resim: 5)")
S(p, "FIND", "kerpiç blok", "was found in", "C4a6’daki sondaj", "C4a6’daki sondajda")
S(p, "FIND", "öküz kafatası", "kind", "bir öküze ait kafatası", "bir öküze ait kafatası")
S(p, "FIND", "öküz kafatası", "was found in", "C4a6’daki sondaj", "C4a6’daki sondajda sürdürülen kazı çalışmaları")
S(p, "FIND", "öküz kafatası", "position (horizontal)", "kerpiç bloğun yaklaşık bir metre doğusunda",
  "bu kerpiç bloğun yaklaşık bir metre doğusunda", hedge="yaklaşık")
S(p, "FIND", "öküz kafatası", "position (vertical)", "kerpiç bloğun birkaç santimetre altında", "birkaç santimetre altında")
S(p, "FIND", "öküz kafatası", "condition", "in situ durumda", "in situ durumda bir öküze ait kafatası")
S(p, "FIND", "boynuz", "kind", "boynuz", "kafatası ile bir boynuz bulunmuştur")
S(p, "FIND", "boynuz", "count", "bir", "bir boynuz bulunmuştur")
S(p, "FIND", "boynuz", "was found in", "C4a6’daki sondaj", "kafatası ile bir boynuz bulunmuştur")
S(p, "DATE", "kerpiç üst yapı enkazı (C4a7)", "is dated to", "Demir Çağı", "Demir Çağı’na ait kerpiç üst yapı enkazının")
S(p, "WORK", "kerpiç üst yapı enkazı (C4a7)", "removal continued", "kaldırılmasına devam edilmiş",
  "kerpiç üst yapı enkazının kaldırılmasına devam edilmiş")
S(p, "BUILT", "kerpiç üst yapı enkazı (C4a7)", "is cut by", "üç çöp çukuru", "üç çöp çukuru tarafından kesildiği tespit edilmiştir")
S(p, "DATE", "çöp çukurları (C4a7)", "is dated to", "daha sonraki dönemler", "bu enkazın daha sonraki dönemlerde")
S(p, "FIGURE", "çöp çukurları (C4a7)", "is shown in figure", "Resim: 6", "kesildiği tespit edilmiştir (Resim: 6)")
S(p, "INTERP", "çöp çukurlarının ikisi (C4a7)", "is similar to", "Kuzey Yamaç’ta daha önceki kazılarda açığa çıkarılanlar",
  "ikisi, Kuzey Yamaç’ta daha önceki kazılarda açığa çıkarılanlarla benzerdir")
S(p, "MEASURE", "çöp çukurları (C4a7)", "measures (diameter)", "bir metreyi aşmakta", "çapı bir metreyi aşmakta")
S(p, "BUILT", "çöp çukurları (C4a7)", "fill", "küllü ve kireçli dolgu", "içindeki küllü ve kireçli dolgudan")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "kind", "profile veren ve vermeyen seramik parçaları",
  "profile veren ve vermeyen Demir Çağı seramik parçaları")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "count", "çok sayıda", "çok sayıda profile veren")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "period", "Demir Çağı", "Demir Çağı seramik parçaları")
S(p, "FIND", "seramik parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının küllü ve kireçli dolgusu",
  "içindeki küllü ve kireçli dolgudan")
S(p, "FIND", "insan kemiği parçaları (C4a7 çöp çukurları)", "kind", "insan kemiği parçaları", "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "FIND", "insan kemiği parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının dolgusu", "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "FIND", "hayvan kemiği parçaları (C4a7 çöp çukurları)", "kind", "hayvan kemiği parçaları", "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "FIND", "hayvan kemiği parçaları (C4a7 çöp çukurları)", "was found in", "çöp çukurlarının dolgusu", "insan ve hayvan kemiği parçaları çıkmaktadır")
S(p, "BUILT", "çöp çukurlarından birisi (C4a7)", "floor", "kireç kaplı taban", "kireç kaplı tabana sahipken")
S(p, "BUILT", "çöp çukurları (Kuzey Yamaç)", "general rule of floor", "kireç kaplı taban", "genel kurala uygun olarak kireç kaplı tabana")
S(p, "WORK", "çöp çukuru (C4a7, çakıl taşı tabanlı)", "part excavated", "sadece kuzey yarısı", "sadece kuzey yarısı kazılan çöp çukurunun")
S(p, "BUILT", "çöp çukuru (C4a7, kuzey yarısı kazılan)", "floor", "çakıl taşı kaplama",
  "tabanında çakıl taşı kaplama tespit edilmiştir")
S(p, "MEASURE", "çöp çukurları (C4a7), en derini", "measures (depth)", "bir metre", "en derini bir metre")
S(p, "MEASURE", "çöp çukurları (C4a7), en sığ olanı", "measures (depth)", "10 santimetre",
  "en sığ olanı ise 10 santimetre derinliğe sahiptir")
S(p, "FIND", "at figürinleri (C4a7)", "kind", "at figürini", "at figürinlerinden bulunmuştur")
S(p, "FIND", "at figürinleri (C4a7)", "was found in", "C4a7 açması", "C4a7 açmasında kerpiç üst yapı enkazının kazısı sırasında")
S(p, "FIND", "at figürinleri (C4a7)", "position inside place", "kerpiç üst yapı enkazı", "kerpiç üst yapı enkazının kazısı sırasında")
S(p, "INTERP", "at figürinleri (C4a7)", "is similar to", "daha önceki yıllarda Kuzey Yamaç kazılarında ele geçen at figürinleri",
  "daha önceki yıllarda Kuzey Yamaç kazılarında tüm veya parça halinde ele geçen at figürinlerinden")
S(p, "FIND", "at figürinleri (önceki yıllar, Kuzey Yamaç)", "condition", "tüm veya parça halinde", "tüm veya parça halinde ele geçen")
S(p, "FIND", "at figürinleri (C4a7)", "parts preserved", "baş veya gövde kısımları", "Bu figürinlerin baş veya gövde kısımlarının olduğu")
S(p, "FIND", "at figürinleri (C4a7), gövdeler", "condition", "ayak veya baş kısımları kopartılmış/kopmuş",
  "gövdelerin ayak veya baş kısımlarının kopartılmış/kopmuş olduğu", hedge="kopartılmış/kopmuş")
S(p, "FIND", "at figürinleri (C4a7), baş kısımları", "workmanship", "detaylı olarak işlenmiş",
  "baş kısımlarının detaylı olarak işlendiği")
S(p, "FIND", "at figürinleri (C4a7), baş kısımları", "surface", "boyanmış", "ve olasılıkla boyandığı gözlemlenmiştir", hedge="olasılıkla")
S(p, "BUILT", "C5b1-C5b2 açmaları", "degree of excavation", "bu alanda en az kazılmış olan", "bu alanda en az kazılmış olan")
S(p, "PLACE", "C5b1-C5b2 açmaları", "position", "Kuzey Yamaç alanının en doğusundaki açmalar",
  "Kuzey Yamaç alanının en doğusundaki açmaları temsil etmekte")
S(p, "DESCR", "C5b1-C5b2 açmalarında derinleşilmesi", "is judged", "ETÇ tabakalarının daha geniş bir alanda açığa çıkarılması açısından önemli",
  "ETÇ tabakalarının daha geniş bir alanda açığa çıkarılması açısından önemlidir")
S(p, "PLACE", "poligon noktası (Kuzey Yamaç)", "elevation", "1055.31 m", "1055.31 m kottaki poligon noktasından")
S(p, "PLACE", "C5b1-C5b2 açmaları (2024 sezonu başı)", "level below poligon noktası", "yaklaşık bir metre aşağı",
  "1055.31 m kottaki poligon noktasından yaklaşık bir metre", hedge="yaklaşık")
S(p, "WORK", "C5b1-C5b2 açmaları (2024 kazıları)", "started from locus", "Locus 70", "2024 kazıları Locus 70’den başlatılmıştır")
S(p, "BUILT", "çöp çukuru (C5b1)", "kind", "çöp çukuru", "dairesel formda bir çöp çukurunun kazıldığı anlaşılmaktadır")
S(p, "MEASURE", "çöp çukuru (C5b1)", "measures (diameter)", "yaklaşık 3 metre", "oldukça geniş (yaklaşık 3 metre çapında)", hedge="yaklaşık")
S(p, "BUILT", "çöp çukuru (C5b1)", "shape", "dairesel form", "dairesel formda bir çöp çukurunun")
S(p, "WORK", "çöp çukuru (C5b1)", "was excavated at", "açmanın son kazısının yapıldığı tarih",
  "açmanın son kazısının yapıldığı tarihte", hedge="anlaşılmaktadır")
S(p, "FIGURE", "çöp çukuru (C5b1)", "is shown in figure", "Resim: 7", "anlaşılmaktadır (Resim: 7)")
S(p, "BUILT", "çöp çukuru (C5b1)", "condition", "zamanla formunu kaybetmiş", "Bu çukurun zamanla formunu kaybettiği")
S(p, "WORK", "C5b1 açması", "step", "çukurun etrafı taban seviyesine indirilerek açma içindeki seviye eşitlendi",
  "çukurun etrafı taban seviyesine indirilerek açma içindeki seviye eşitlendikten sonra")
S(p, "WORK", "C5b1 açması", "step", "tüm karenin kazılmasına devam edilmiştir", "C5b1 açmasında tüm karenin kazılmasına devam edilmiştir")
S(p, "WORK", "C5b2 açması", "was excavated at the same time as", "C5b1 açması", "Bununla eş zamanda, C5b2 açmasının kazısı yürütülmüş")
S(p, "WORK", "rampa (C5b1)", "count", "iki", "iki rampa hazırlanmıştır")
S(p, "WORK", "rampa (C5b1)", "purpose", "toprak tahliyesi", "C5b1 açmasından toprak tahliyesi için")
S(p, "FIND", "seramik parçaları (C5b1-C5b2)", "kind", "seramik parçaları", "dağılım gösteren seramik parçaları")
S(p, "FIND", "seramik parçaları (C5b1-C5b2)", "period", "ETÇ-Demir Çağı arası", "ETÇ-Demir Çağı arasında dağılım gösteren seramik parçaları")
S(p, "FIND", "seramik parçaları (C5b1-C5b2)", "was found in", "her iki açma (C5b1, C5b2)", "Her iki açmada da derinleştikçe ele geçen malzeme")
S(p, "BUILT", "duvarlar (C5b1-C5b2)", "kind", "basit duvarlar", "basit (iki sıra genişliğinde")
S(p, "DATE", "duvarlar (C5b1-C5b2)", "is dated to", "Demir Çağı", "Kuzey Yamaç’ta Demir Çağı’na tarihlenen basit")
S(p, "MEASURE", "duvarlar (C5b1-C5b2)", "measures (width)", "iki sıra", "iki sıra genişliğinde ve birkaç sıra yüksekliğinde")
S(p, "MEASURE", "duvarlar (C5b1-C5b2)", "measures (height)", "birkaç sıra", "iki sıra genişliğinde ve birkaç sıra yüksekliğinde")
S(p, "BUILT", "duvarlar (C5b1-C5b2)", "is made of", "orta boy taşlar", "orta boy taşlardan oluşan duvarlar tespit edilmiştir")
S(p, "BUILT", "duvarlar (C5b1-C5b2)", "gives clear plan", "belirgin bir plan", "Bu duvarlar belirgin bir plan vermediği için", neg=True)
S(p, "WORK", "duvarlar (C5b1-C5b2)", "were photographed by", "kazı ekibi", "kazı ekibi tarafından fotoğraflanarak kaldırılmıştır")
S(p, "WORK", "duvarlar (C5b1-C5b2)", "were removed", "kaldırılmıştır", "fotoğraflanarak kaldırılmıştır")
S(p, "PLACE", "C4c10 açması", "position", "bu açma grubunun (C5b1-C5b2) batısında", "bu açma grubunun batısında kalan C4c10 açmasının")
S(p, "INTERP", "duvarların benzerleri", "were found and removed in", "önceki sezonlarda yapılan kazı çalışmaları",
  "önceki sezonlarda yapılan kazı çalışmalarında da tespit edildiği ve kaldırıldığı anlaşılmaktadır",
  hedge="anlaşılmaktadır")
S(p, "INTERP", "duvarların benzerleri", "is based on", "C4c10 açmasının kesiti", "C4c10 açmasının kesitine bakıldığında")
S(p, "BUILT", "geniş çöp çukurları", "is particular to", "Kuzey Yamaç açmaları",
  "Her iki açmada da Kuzey Yamaç açmalarına özgü olan geniş")

# ---------------------------------------------------------------- page 284
p = 284
S(p, "BUILT", "çöp çukurları (C5b1-C5b2)", "count excavated", "iki", "çöp çukurlarından ikisi kazılmış olup")
S(p, "MEASURE", "çöp çukurları (C5b1-C5b2, iki adet)", "size compared with other pits", "daha küçük",
  "alandaki diğer çöp çukurlarına kıyasla daha küçüktür")
S(p, "BUILT", "çöp çukurları (C5b1-C5b2, iki adet)", "floor", "kireç sıvalı", "tabanlarının kireç sıvalı olduğu dikkat çekmiştir")
S(p, "FIND", "kırık seramik parçaları (C5b1-C5b2 çöp çukurları)", "kind", "kırık seramik parçaları", "kırık seramik parçaları ve hayvan kemikleri")
S(p, "FIND", "kırık seramik parçaları (C5b1-C5b2 çöp çukurları)", "was found in", "çöp çukurları", "bunlar da kırık seramik parçaları")
S(p, "FIND", "hayvan kemikleri (C5b1-C5b2 çöp çukurları)", "kind", "hayvan kemikleri", "kırık seramik parçaları ve hayvan kemikleri")
S(p, "FIND", "hayvan kemikleri (C5b1-C5b2 çöp çukurları)", "was found in", "çöp çukurları", "hayvan kemikleri, kül dolgu içermektedir")
S(p, "BUILT", "çöp çukurları (C5b1-C5b2, iki adet)", "fill", "kül dolgu", "kül dolgu içermektedir")
S(p, "BUILT", "alandaki tüm çöp çukurları", "contain the same", "kırık seramik parçaları, hayvan kemikleri, kül dolgu", "Alandaki tüm çöp çukurları gibi")
S(p, "FIND", "at figürinleri (C5b1-C5b2)", "kind", "at figürinleri", "at figürinleri, heykelcikler, ağırşaklar")
S(p, "FIND", "at figürinleri (C5b1-C5b2)", "was found in", "C5b1 ve C5b2 açmaları", "C5b1 ve C5b2 açmalarının kazısı sırasında")
S(p, "FIND", "heykelcikler (C5b1-C5b2)", "kind", "heykelcikler", "at figürinleri, heykelcikler, ağırşaklar")
S(p, "FIND", "heykelcikler (C5b1-C5b2)", "was found in", "C5b1 ve C5b2 açmaları", "C5b1 ve C5b2 açmalarının kazısı sırasında")
S(p, "FIND", "ağırşaklar (C5b1-C5b2)", "kind", "ağırşaklar", "heykelcikler, ağırşaklar ve diğer küçük buluntulardan")
S(p, "FIND", "ağırşaklar (C5b1-C5b2)", "was found in", "C5b1 ve C5b2 açmaları", "C5b1 ve C5b2 açmalarının kazısı sırasında")
S(p, "FIND", "diğer küçük buluntular (C5b1-C5b2)", "kind", "diğer küçük buluntular", "diğer küçük buluntulardan örnekler ele geçirilmiştir")
S(p, "FIND", "diğer küçük buluntular (C5b1-C5b2)", "was found in", "C5b1 ve C5b2 açmaları", "C5b1 ve C5b2 açmalarının kazısı sırasında")
S(p, "INTERP", "C5b1-C5b2 küçük buluntuları", "is similar to", "Kuzey Yamaç’taki önceki kazılardan bilinenler",
  "Kuzey Yamaç’taki önceki kazılardan bildiğimiz")
S(p, "FIND", "heykelcik başı parçası", "kind", "küçük bir heykelciğin baş tarafına ait parça",
  "küçük bir heykelciğin baş tarafına ait olan parça")
S(p, "FIND", "heykelcik başı parçası", "period", "Helenistik/Roma Dönemi",
  "Helenistik/Roma Dönemi’ne tarihlenebilecek olan", hedge="tarihlenebilecek")
S(p, "FIND", "heykelcik başı parçası", "was found in", "C5b1 ve C5b2 açmaları", "Bunlar arasında Helenistik/Roma")
S(p, "FIND", "heykelcik başı parçası", "position inside place", "kazılan dolgu içi", "kazılan dolgu içinden ele geçirilmiştir")
S(p, "BUILT", "oval çöp çukuru (C5b2)", "is located in", "C5b2 açması", "C5b2 açmasının kazısı sırasında")
S(p, "BUILT", "oval çöp çukuru (C5b2)", "position", "açmanın doğu sınırına yakın", "açmanın doğu sınırına yakın")
S(p, "BUILT", "oval çöp çukuru (C5b2)", "shape", "oval form", "oval formda ve yaklaşık olarak")
S(p, "MEASURE", "oval çöp çukuru (C5b2)", "measures (depth)", "yaklaşık olarak 1.5 metre",
  "yaklaşık olarak 1.5 metre derinlikte bir çöp çukuru tespit edilmiştir", hedge="yaklaşık olarak")
S(p, "FIGURE", "oval çöp çukuru (C5b2)", "is shown in figure", "Resim: 6", "çöp çukuru tespit edilmiştir (Resim: 6)")
S(p, "BUILT", "ikinci çöp çukuru (C5b2)", "position", "oval çöp çukuruna bitişik", "buna bitişik ve çok daha küçük")
S(p, "MEASURE", "ikinci çöp çukuru (C5b2)", "size", "çok daha küçük", "buna bitişik ve çok daha küçük")
S(p, "BUILT", "ikinci çöp çukuru (C5b2)", "has definite shape", "belirgin bir form", "belirgin bir forma sahip olmayan", neg=True)
S(p, "MEASURE", "ikinci çöp çukuru (C5b2)", "depth", "çok sığ", "çok sığ ikinci bir çöp çukurunun da varlığı tespit edilmiştir")
S(p, "FIND", "kemik parçaları (C5b2 çöp çukurları)", "kind", "kemik parçası", "çok sayıda kemik ve seramik parçası")
S(p, "FIND", "kemik parçaları (C5b2 çöp çukurları)", "count", "çok sayıda", "çok sayıda kemik ve seramik parçası")
S(p, "FIND", "kemik parçaları (C5b2 çöp çukurları)", "was found in", "her iki çöp çukuru (C5b2)", "Her iki çöp çukurundan çok sayıda kemik")
S(p, "FIND", "seramik parçaları (C5b2 çöp çukurları)", "kind", "seramik parçası", "çok sayıda kemik ve seramik parçası")
S(p, "FIND", "seramik parçaları (C5b2 çöp çukurları)", "count", "çok sayıda", "çok sayıda kemik ve seramik parçası")
S(p, "FIND", "seramik parçaları (C5b2 çöp çukurları)", "was found in", "her iki çöp çukuru (C5b2)", "Her iki çöp çukurundan çok sayıda kemik")
S(p, "BUILT", "oval çöp çukuru (C5b2)", "fill", "kalın kül dolgu", "kalın ve birkaç farklı seviyede kül dolgunun")
S(p, "BUILT", "kül dolgu (oval çöp çukuru, C5b2)", "levels", "birkaç farklı seviyede", "birkaç farklı seviyede kül dolgunun")
S(p, "BUILT", "kül dolgu (oval çöp çukuru, C5b2)", "way of filling", "homojen olmayarak", "homojen olmayarak dolduğu tespit edilmiştir")
S(p, "PLACE", "C5b1 ve C5b2 açmaları (2024 sezonu sonu)", "level below Höyük surface", "yaklaşık 2.4 metre",
  "Höyük yüzeyinden yaklaşık 2.4 metre", hedge="yaklaşık")
S(p, "WORK", "C5b1 ve C5b2 açmaları (2024)", "count of locus excavated", "toplam 5 Locus", "toplam 5 Locus kazılmıştır")
S(p, "PLACE", "C4b10 açması", "is among", "Kuzey Yamaç’ta en derin açmalar", "C4b10 açması Kuzey Yamaç’ta en derin açmalardan olup")
S(p, "WORK", "C4b10 açması (2024 kazısı)", "duration", "yaklaşık sekiz gün",
  "yaklaşık sekiz gün süren bir kazı çalışmasına sahne olmuştur", hedge="yaklaşık")
S(p, "PLACE", "C4b10 açması", "opening elevation relative to 1055.31 m", "iki metre derinlik",
  "Açılış kotları yüzeydeki 1055.31 metre kotuna kıyasla iki metre derinlik göstermektedir")
S(p, "BUILT", "çöp çukuru (C4b10)", "position", "C4b9 açmasıyla olan sınırında", "C4b9 açmasıyla olan sınırında")
S(p, "PLACE", "C4b9 açması", "position", "C4b10 açmasının batısında", "batısındaki C4b9 açmasıyla")
S(p, "BUILT", "çöp çukuru (C4b10)", "size", "geniş", "geniş ve dairesel formda bir çöp çukuru")
S(p, "BUILT", "çöp çukuru (C4b10)", "shape", "dairesel form", "geniş ve dairesel formda bir çöp çukuru")
S(p, "WORK", "çöp çukuru (C4b10)", "was excavated in", "açmanın son kazıldığı sezon", "Açmanın son kazıldığı sezonda",
  hedge="anlaşılmaktadır")
S(p, "WORK", "C4b10 açması (2024 kazıları)", "started from locus", "Locus 60", "2024 kazıları bu açmada Locus 60’dan başlatılmıştır")
S(p, "WORK", "C4b10 açması (2024 kazıları)", "step (first)", "açmanın çöp çukurunun taban seviyesine indirilmesi",
  "Önce açmanın çöp çukurunun taban seviyesine indirilmesi")
S(p, "WORK", "C4b10 açması (2024 kazıları)", "step (then)", "tüm açma yüzeyinde kazı çalışması", "sonra da tüm açma yüzeyinde kazı çalışması yapılması")
S(p, "WORK", "C4b10 açması (2024 kazıları)", "deepened by", "yaklaşık 40 santimetre", "yaklaşık 40 santimetre derinleşilmiştir",
  hedge="yaklaşık")
S(p, "PLACE", "C4b10 açması (açma merkezi)", "closing elevation", "1052.803 metre", "kapanış kotu 1052.803 metre olup")
S(p, "PLACE", "C4b10 açması", "depth reached below Höyük surface", "2.5 metre", "Höyük yüzeyinden 2.5 metre inilmiştir")
S(p, "FIGURE", "C4b10 açması", "is shown in figure", "Resim: 8", "(Resim: 8)")
S(p, "FIND", "seramik parçaları (C4b10)", "kind", "seramik parçaları", "çağlarına ait seramik parçalarının ele geçirildiği")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "ETÇ III", "ETÇ III, Orta ve Geç Tunç çağlarına ait")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "Orta Tunç çağı", "ETÇ III, Orta ve Geç Tunç çağlarına ait")
S(p, "FIND", "seramik parçaları (C4b10)", "period", "Geç Tunç çağı", "ETÇ III, Orta ve Geç Tunç çağlarına ait")
S(p, "FIND", "seramik parçaları (C4b10)", "was found in", "C4b10 açması", "Bu açmanın kazısı sırasında")
S(p, "FIND", "ETÇ III, Orta ve Geç Tunç çağı seramik parçaları", "were found before in nearby trenches", "civardaki açmalar",
  "daha önce civardaki açmalarda tespit edilmeyen", neg=True)
S(p, "FIND", "tezgâh ağırlığı", "kind", "tezgâh ağırlığı", "küçük bir tezgâh ağırlığı")
S(p, "FIND", "tezgâh ağırlığı", "size", "küçük", "küçük bir tezgâh ağırlığı")
S(p, "FIND", "tezgâh ağırlığı", "was found in", "bu alan (C4b10)", "Yine bu alanda yüzeyde bulunan")
S(p, "FIND", "tezgâh ağırlığı", "position inside place", "yüzeyde", "yüzeyde bulunan küçük bir tezgâh ağırlığı")
S(p, "FIND", "tezgâh ağırlığı", "was recorded as", "envanterlik", "envanterlik olarak kaydedilmiştir")
S(p, "WORK", "C4c10 açması", "is", "Kuzey Yamaç’ta 2024 sezonunda kazısı yapılan son açma",
  "Kuzey Yamaç’ta 2024 sezonunda kazısı yapılan son açma C4c10’dur")
S(p, "WORK", "C4c10 açması (2024)", "duration", "sadece iki gün", "Sadece iki gün çalışılan bu açmada")
S(p, "WORK", "C4c10 açması (2024)", "step", "açma yüzeyinde biriken taşlar toplanmış ve açma dışına çıkarılmıştır",
  "açma yüzeyinde biriken taşlar toplanmış ve açma dışına çıkarılmıştır")
S(p, "BUILT", "taşlar (C4c10 açma yüzeyi)", "came from", "kenarlardan ve kesitten düşerek", "kenarlardan ve kesitten düşerek")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "removal was begun", "kaldırılmasına başlanmıştır",
  "Demir Devri duvarların kaldırılmasına başlanmıştır")
S(p, "DATE", "duvarlar (C4c10)", "is dated to", "Demir Devri", "Demir Devri duvarların")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were exposed in", "açmadaki son kazı sezonu", "açmadaki son kazı sezonunda açığa")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were photographed", "fotoğraflanarak", "fotoğraflanarak çizimi yapılan")
S(p, "WORK", "Demir Devri duvarlar (C4c10)", "were drawn", "çizimi yapılan", "fotoğraflanarak çizimi yapılan")
S(p, "BUILT", "dolgu (C4c10)", "consistency", "oldukça sert", "oldukça sert bir dolgu")
S(p, "WORK", "dolgu (C4c10)", "excavated depth", "yaklaşık 20 santimetre", "oldukça sert bir dolgu yaklaşık 20 santimetre kazılmıştır",
  hedge="yaklaşık")
S(p, "BUILT", "dolgu (C4c10)", "lies below", "Demir Devri duvarlar", "Duvarlar kaldırıldıktan sonra yapılan kazı çalışmasında")
S(p, "WORK", "bu açmalardaki kazı çalışmaları", "will continue in", "2025 sezonu", "kazı çalışmaları 2025 sezonunda devam edecek")
S(p, "WORK", "bu açmalardaki kazı çalışmaları", "aim", "bu alanın da diğer açmaların kotuna indirilmesi",
  "alanın da diğer açmaların kotuna indirilmesi için çalışılacaktır")
S(p, "WORK", "Kuzey Yamaç açmaları", "excavated since", "1994", "Kuzey Yamaç açmalarında 1994 yılından beri yürütülen kazı çalışmalarının")
S(p, "WORK", "ERT yöntemi", "was applied at", "Höyük geneli", "Höyük genelinde uygulanan ERT yönteminin")
S(p, "BUILT", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "kind", "Tunç Çağı sonrası katmanı", "bir Tunç Çağı sonrası")
S(p, "MEASURE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "measures (thickness)", "yaklaşık 4-5 metre",
  "yaklaşık 4-5 metre kalınlığında bir Tunç Çağı sonrası", hedge="yaklaşık")
S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", "Demir Devri", "(Demir Devri, Arkaik, Klasik, Helenistik/Roma, Bizans)")
S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", "Arkaik", "(Demir Devri, Arkaik, Klasik, Helenistik/Roma, Bizans)")
S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", "Klasik", "(Demir Devri, Arkaik, Klasik, Helenistik/Roma, Bizans)")
S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", "Helenistik/Roma", "(Demir Devri, Arkaik, Klasik, Helenistik/Roma, Bizans)")
S(p, "DATE", "Tunç Çağı sonrası katmanı (Kuzey Yamaç)", "includes period", "Bizans", "(Demir Devri, Arkaik, Klasik, Helenistik/Roma, Bizans)")
S(p, "MEASURE", "Kuzey Yamaç kazı alanı", "measures", "yaklaşık 20x30 metre", "(yaklaşık 20x30 metre alanda)", hedge="yaklaşık")
S(p, "BUILT", "kalın dolgu (Kuzey Yamaç)", "[unclear] stratigraphy with sound architectural plans found", "sağlam mimari planlar veren, somut maddi kültür kalıntısı sağlayan stratigrafi",
  "somut maddi kültür kalıntısı sağlayan stratigrafiye rastlanmamıştır", neg=True)

# ---------------------------------------------------------------- page 285
p = 285
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "kırık seramik parçaları", "tamamen kırık seramik parçaları, figürin parçaları")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "figürin parçaları", "tamamen kırık seramik parçaları, figürin parçaları")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "consists of", "diğer küçük buluntular", "diğer küçük buluntulardan oluşan")
S(p, "BUILT", "kalın ‘dolgu’ (Kuzey Yamaç)", "is destroyed by", "çöp çukurları",
  "sıklıkla çöp çukurları tarafından tahrip edilmiş bir stratigrafik karaktere sahiptir", hedge="sıklıkla")
S(p, "INTERP", "Kuzey Yamaç (Tunç Çağları tabakalarına ulaşıncaya kadar)", "chance of finding sound architecture and material culture", "oldukça zayıf",
  "sağlam mimari ve maddi kültür kalıntısı bulma ihtimali oldukça zayıftır")
S(p, "DATE", "yapı katları (C4a8, yaklaşık 1049 metre kot)", "is dated to", "ETÇ", "erişilen yapı katlarının ETÇ’ye tarihlendiği")
S(p, "DESCR", "ETÇ yapı katları (C4a8)", "is judged", "mimari ve küçük buluntu açısından oldukça sağlam bulgular sunduğu",
  "bu katların mimari ve küçük buluntu açısından oldukça sağlam bulgular sunduğu")
S(p, "INTERP", "karışık dolgu (Kuzey Yamaç)", "will not end until", "tüm açmalarda 1049 metre kota erişilinceye kadar",
  "1049 metre kota erişilinceye kadar bu karışık ve sağlam mimari plan/buluntu vermeyen dolgunun sonlanmayacağı açıktır",
  hedge="açıktır")
S(p, "STRUCT", "başlık", "heading reads", "4.2 MERKEZİ KİLİSE (Geleceğe Miras Projesi ödeneğiyle)",
  "4.2 MERKEZİ KİLİSE (Geleceğe Miras Projesi ödeneğiyle)")
S(p, "ADMIN", "Merkezi Kilise kazısı", "was funded by", "Geleceğe Miras Projesi ödeneği", "(Geleceğe Miras Projesi ödeneğiyle)")
S(p, "ADMIN", "Geleceğe Miras Projesi", "belongs to", "Kültür Varlıkları ve Müzeler Genel Müdürlüğü",
  "Kültür Varlıkları ve Müzeler Genel Müdürlüğünün Geleceğe Miras Projesi kapsamında")
S(p, "WORK", "Merkezi Kilise kazısı (2024)", "name of the work", "Merkezi Kilise 1. Etap 333 m2 Alan İçerisinde El İle Kazı",
  "“Merkezi Kilise 1. Etap 333 m2 Alan İçerisinde El İle Kazı”")
S(p, "WORK", "Merkezi Kilise kazısı (2024)", "method", "el ile kazı", "El İle Kazı")
S(p, "WORK", "Merkezi Kilise açmaları", "count", "yedi adet", "yedi adet 5x5 metre açmada")
S(p, "MEASURE", "Merkezi Kilise açmaları", "measures", "5x5 metre", "yedi adet 5x5 metre açmada")
S(p, "FIGURE", "Merkezi Kilise kazısı (2024)", "is shown in table", "Tablo: 1", "(Tablo: 1, Resim: 9)")
S(p, "FIGURE", "Merkezi Kilise kazısı (2024)", "is shown in figure", "Resim: 9", "(Tablo: 1, Resim: 9)")
S(p, "WORK", "Merkezi Kilise kazıları", "aim", "Merkezi Kilise (Manastır) yapısının çevresini genişleterek restitüsyon ve restorasyon projelerine yeterli zemini ve alanı sağlamak",
  "restitüsyon ve restorasyon projelerine yeterli zemini ve alanı sağlamaktır")
S(p, "LAB", "restitüsyon ve restorasyon projeleri (Merkezi Kilise)", "planned for", "ileriki yıllar", "ileriki yıllarda yapılacak")

# table header cells
hdrq = "Açma Açılış tarihi Açılış kotu Kapanış tarihi Kapanış kotu Kazılan m3"
for h in ["Açma", "Açılış tarihi", "Açılış kotu", "Kapanış tarihi", "Kapanış kotu", "Kazılan m3"]:
    S(p, "STRUCT", "Tablo 1", "column heading", h, h)
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
    a = r[0]
    S(p, "WORK", a + " açması", "is a trench excavated at Merkezi Kilise in 2024 (table row)", a, a + " " + r[1])
    if a == "E5c5":
        S(p, "WORK", a + " açması", "[unclear] opening date (earlier than the stated start of the work, 29.08.2024)", r[1], " ".join(r[:2]))
    else:
        S(p, "WORK", a + " açması", "opening date", r[1], " ".join(r[:2]))
    S(p, "PLACE", a + " açması", "opening elevation", r[2], " ".join(r[:3]))
    S(p, "WORK", a + " açması", "closing date", r[3], " ".join(r[:4]))
    S(p, "PLACE", a + " açması", "closing elevation", r[4], " ".join(r[:5]))
    S(p, "WORK", a + " açması", "excavated volume (m3)", r[5], " ".join(r))
S(p, "STRUCT", "Tablo 1", "row label", "TOPLAM", "TOPLAM")
S(p, "WORK", "Merkezi Kilise açmaları (TOPLAM)", "opening date", "29.08.2024", "TOPLAM 29.08.2024")
S(p, "WORK", "Merkezi Kilise açmaları (TOPLAM)", "closing date", "27.09.2024", "TOPLAM 29.08.2024 27.09.2024")
S(p, "WORK", "Merkezi Kilise açmaları (TOPLAM)", "excavated volume (m3)", "120.78", "TOPLAM 29.08.2024 27.09.2024 120.78")
S(p, "FIGURE", "Tablo 1", "caption", "Merkezi Kilise’de 2024 sezonunda kazı yapılan açmalar, açılış-kapanış tarihleri, açılış-kapanış kotları ve toplam hafriyat miktarı (m3).",
  "Tablo 1: Merkezi Kilise’de 2024 sezonunda kazı yapılan açmalar, açılış-kapanış tarihleri, açılış-kapanış kotları ve toplam hafriyat miktarı (m3).")
S(p, "ADMIN", "Merkezi Kilise çalışmasına ait ayrıntılı rapor", "was submitted to", "T.C. Antalya Valiliği, İl Kültür ve Turizm Müdürlüğü",
  "ayrıntılı rapor T.C. Antalya Valiliği, İl Kültür ve Turizm Müdürlüğüne sunulduğundan")
S(p, "DOC", "Merkezi Kilise çalışması", "is reported in detail here", "detaylı bir şekilde", "burada detaylı bir şekilde aktarılmayacaktır", neg=True)
S(p, "DESCR", "farklı mekanların duvarlarının sağlam ele geçirilmesi", "is judged", "1. Etap kazılarında elde edilen en önemli bulgu",
  "1. Etap kazılarında elde edilen en önemli")
S(p, "BUILT", "farklı mekanların duvarları", "belongs to", "Manastır yapısı", "bu yapıya ait olan farklı mekanların duvarlarının")
S(p, "BUILT", "farklı mekanların duvarları", "was found in", "Manastır yapısının güney sınırı boyunca açılan tüm açmalar",
  "Manastır yapısının güney sınırı boyunca açılan tüm açmalarda")
S(p, "BUILT", "farklı mekanların duvarları", "condition", "sağlam", "duvarlarının sağlam olarak ele geçirilmesidir")
S(p, "BUILT", MK, "building material", "ikincil malzeme (spolia)", "sıklıkla kullanılan ikincil malzeme (spolia)", hedge="sıklıkla")
S(p, "BUILT", "Manastır yapısını çevreleyen mekanlar", "building material", "ikincil malzeme (spolia)",
  "ikincil malzeme (spolia) Manastır yapısını çevreleyen mekanlarda da gözlemlenmiştir")
S(p, "FIGURE", "ikincil malzeme (spolia)", "is shown in figure", "Resim: 10", "da gözlemlenmiştir (Resim: 10)")

# ---------------------------------------------------------------- page 286
p = 286
S(p, "BUILT", "büyük sarnıç", "is part of", "Manastır yapısı", "Manastır yapısının parçası olan büyük sarnıç")
S(p, "BUILT", "büyük sarnıç", "kind", "sarnıç", "büyük sarnıç ve onu çevreleyen")
S(p, "BUILT", "sarnıcı çevreleyen yapılar", "were exposed", "ortaya çıkarıldığı", "onu çevreleyen yapıların da ortaya çıkarıldığı kazılarda")
S(p, "BUILT", "yol (Merkezi Kilise)", "kind", "yol", "bir yol da bulunmuştur")
S(p, "BUILT", "yol (Merkezi Kilise)", "has", "taban döşemesi", "taban döşemesi olan bir yol")
S(p, "FIGURE", "yol (Merkezi Kilise)", "is shown in figure", "Resim: 11", "bir yol da bulunmuştur (Resim: 11)")
S(p, "BUILT", "Manastır yapısını çevreleyen yapılar", "[unclear] plans", "çok evreli planlar",
  "çok Manastır yapısını çevreleyen yapıların çok evreli planlarıyla karşılaşılmıştır")
S(p, "PLACE", "çok evreli yapılar", "position", "bu alanın kuzeyi, Kilise’nin apsis yapısına doğru",
  "alanın kuzeyine, Kilise’nin apsis yapısına doğru")
S(p, "BUILT", "Kilise", "has", "apsis yapısı", "Kilise’nin apsis yapısına")
S(p, "WORK", "GMP bünyesinde yürütülen kazılar", "last day", "27.09.2024", "kazıların son günü olan 27.09.2024")
S(p, "FIGURE", "Merkezi Kilise’de kazı yapılan alanların görünümü", "is shown in figure", "Resim 12",
  "Merkezi Kilise’de kazı yapılan alanların görünümü Resim 12’de verilmiştir")
S(p, "FIND", "işli mimari parçalar (Merkezi Kilise)", "kind", "işli mimari parçalar", "ele geçen işli mimari parçalar")
S(p, "FIND", "işli mimari parçalar (Merkezi Kilise)", "was found in", "Merkezi Kilise kazıları", "Merkezi Kilise kazılarında ele geçen")
S(p, "FIND", "işli mimari parçalar (Merkezi Kilise)", "was placed in", "Höyük üzerindeki taş havuzu",
  "ya Höyük üzerindeki taş havuzuna konmuş", hedge="ya ... ya da")
S(p, "FIND", "işli mimari parçalar (Merkezi Kilise)", "was brought to", "kazı deposu", "ya da kazı deposuna getirtilmiştir",
  hedge="ya ... ya da")
S(p, "FIND", "sikkeler (Merkezi Kilise)", "kind", "sikke", "bakır sikkeler")
S(p, "FIND", "sikkeler (Merkezi Kilise)", "material", "bakır", "bakır sikkeler")
S(p, "FIND", "sikkeler (Merkezi Kilise)", "condition", "oldukça korozyona uğramış", "oldukça korozyona uğramış bakır sikkeler")
S(p, "FIND", "sikkeler (Merkezi Kilise)", "was found in", "Merkezi Kilise kazıları", "Kazılardan çıkan küçük buluntular")
S(p, "FIND", "takı (Merkezi Kilise)", "kind", "takı (bilezik?)", "takı (bilezik?)", hedge="bilezik?")
S(p, "FIND", "takı (Merkezi Kilise)", "[unclear] material (whether 'bakır' also covers takı)", "bakır",
  "bakır sikkeler ve takı (bilezik?)", hedge="[unclear]")
S(p, "FIND", "takı (Merkezi Kilise)", "was found in", "Merkezi Kilise kazıları", "Kazılardan çıkan küçük buluntular")
S(p, "FIND", "liturji (ayin) objeleri (Merkezi Kilise)", "kind", "liturji (ayin) objeleri", "liturji (ayin) objeleri")
S(p, "FIND", "liturji (ayin) objeleri (Merkezi Kilise)", "material", "demir", "demirden imal edilmiş liturji (ayin) objeleri")
S(p, "FIND", "liturji (ayin) objeleri (Merkezi Kilise)", "was found in", "Merkezi Kilise kazıları", "Kazılardan çıkan küçük buluntular")
S(p, "FIND", "boncuk (Merkezi Kilise)", "kind", "boncuk", "pişmiş topraktan boncuk")
S(p, "FIND", "boncuk (Merkezi Kilise)", "material", "pişmiş toprak", "pişmiş topraktan boncuk")
S(p, "FIND", "boncuk (Merkezi Kilise)", "was found in", "Merkezi Kilise kazıları", "Kazılardan çıkan küçük buluntular")
S(p, "FIND", "küçük buluntular (Merkezi Kilise)", "are classed as", "etütlük", "etütlük sayılacak buluntular vardır", hedge="sayılacak")
S(p, "STRUCT", "başlık", "heading reads", "5- KAMU YARARINA FAALİYETLER:", "5- KAMU YARARINA FAALİYETLER:")
S(p, "WORK", "Hacımusalar Höyük Kazısı", "includes", "disiplinler arası araştırmalar", "yürütülen disiplinler arası araştırmaların")
S(p, "WORK", "disiplinler arası araştırmalar", "aim", "güncel sorunların çözümüne katkı sağlamak",
  "güncel sorunların (iklim değişikliği")
for v, q in [("iklim değişikliği", "(iklim değişikliği,"),
             ("tarımsal üretimde verim kaybı", "tarımsal üretimde verim kaybı"),
             ("erozyon", "verim kaybı, erozyon"),
             ("ani ve şiddetli meteorolojik olaylar", "ani ve şiddetli meteorolojik olaylar, vb.)")]:
    S(p, "DESCR", "güncel sorunlar", "example", v, q)
S(p, "WORK", "disiplinler arası araştırmalar", "aim", "Elmalı Ovası’ndaki refahın artırılmasına katkı sağlamak",
  "Elmalı Ovası’ndaki refahın artırılmasına katkı sağlaması amacıyla")
S(p, "WORK", "etkinlikler", "are held", "her yıl", "her yıl ilçenin yöneticileri")
S(p, "WORK", "etkinlikler", "are held for", "ilçenin yöneticileri", "ilçenin yöneticileri, kamu görevlileri ve halkı için")
S(p, "WORK", "etkinlikler", "are held for", "kamu görevlileri", "ilçenin yöneticileri, kamu görevlileri ve halkı için")
S(p, "WORK", "etkinlikler", "are held for", "halk", "ilçenin yöneticileri, kamu görevlileri ve halkı için")
S(p, "WORK", "etkinlikler", "content presented", "çalışmalarımızdan kesitler", "etkinliklerde çalışmalarımızdan kesitler sunmaktayız")
S(p, "WORK", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "date", "12.10.2024", "12.10.2024 tarihinde")
S(p, "ADMIN", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "was organised by", "Elmalı Belediyesi",
  "Elmalı Belediyesi ve Elmalı Vakfı tarafından düzenlenen")
S(p, "ADMIN", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu", "was organised by", "Elmalı Vakfı",
  "Elmalı Belediyesi ve Elmalı Vakfı tarafından düzenlenen")
S(p, "WORK", "konuşma", "was given at", "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu",
  "Elmalı Bölgesel İklim Değişikliği ve Çevre Sorunları Sempozyumu’nda")
S(p, "WORK", "konuşma", "has title", "Elmalı Ovası’nın Geçmiş İklimi ve Kültür Tarihi", "“Elmalı Ovası’nın Geçmiş İklimi ve Kültür Tarihi”")
S(p, "WORK", "konuşma", "drew attention to", "bölgedeki arkeolojik kültürler", "hem bölgedeki arkeolojik kültürlere")
S(p, "WORK", "konuşma", "drew attention to", "geçmiş insanların yaşadıkları çevresel sorunlar",
  "geçmiş insanların yaşadıkları çevresel sorunlara dikkat çekilmiştir")

# ---------------------------------------------------------------- page 287
p = 287
S(p, "STRUCT", "başlık", "heading reads", "EKLER", "EKLER")
S(p, "FIGURE", "Resim 1", "caption", "Merkezi Kilise’nin kuzey ve batısındaki alanlarda 2022, 2023 ve 2024 sezonlarında gerçekleştirilen yer radarı çalışmalarının sonuçları.",
  "Resim 1: Merkezi Kilise’nin kuzey ve batısındaki alanlarda 2022, 2023 ve 2024 sezonlarında gerçekleştirilen yer radarı çalışmalarının sonuçları.")
S(p, "FIGURE", "Resim 2", "caption", "Hacımusalar Höyük’te gerçekleştirilen Elektrik Rezistivite (Özdirenç) Tomografi (ERT) çalışmasında taranan 10 profilin konumunu gösteren harita.",
  "Resim 2: Hacımusalar Höyük’te gerçekleştirilen Elektrik Rezistivite (Özdirenç) Tomografi (ERT) çalışmasında taranan 10 profilin konumunu gösteren harita.")
S(p, "FIGURE", "Resim 2", "kind of image", "harita", "10 profilin konumunu gösteren harita")

# ---------------------------------------------------------------- page 288
p = 288
S(p, "FIGURE", "Resim 3", "caption", "(a) Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline ait ölçüm haritaları, (b) topoğrafik düzeltmesi yapılmış olan hat haritası üzerinde işaretlenen arkeolojik (1,4,5,6) ve jeolojik (2,3,7) katmanlar.",
  "Resim 3: (a) Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline ait ölçüm haritaları, (b) topoğrafik düzeltmesi yapılmış olan hat haritası üzerinde işaretlenen")
S(p, "FIGURE", "birinci ERT profili", "is shown in figure", "Resim 2", "Resim 2’de gösterilen 240 metre uzunluktaki birinci ERT profiline")
S(p, "MEASURE", "birinci ERT profili", "measures (length)", "240 metre", "240 metre uzunluktaki birinci ERT profiline")
S(p, "WORK", "hat haritası (birinci ERT profili)", "was processed by", "topoğrafik düzeltme", "topoğrafik düzeltmesi yapılmış olan hat haritası")
S(p, "BUILT", "arkeolojik katmanlar (birinci ERT profili)", "layer numbers", "1,4,5,6", "arkeolojik (1,4,5,6)")
S(p, "BUILT", "jeolojik katmanlar (birinci ERT profili)", "layer numbers", "2,3,7", "jeolojik (2,3,7) katmanlar")
S(p, "FIGURE", "Resim 4", "caption", "Önceki kazı sezonlarında kısmen kazılan, her biri farklı seviyelerde bırakılan açmalar. 2024 kazı sezonunda kazısı yapılan açmalar C4b10, C4c10, C5b1, C5b2 olmuştur. Bu fotoğraf aynı zamanda 2024 sezonu sonunda Kuzey Yamaç açmalarının kapanış durumunu göstermektedir.",
  "Resim 4: Önceki kazı sezonlarında kısmen kazılan, her biri farklı seviyelerde bırakılan açmalar.")
S(p, "WORK", "Kuzey Yamaç açmaları", "were excavated in earlier seasons", "kısmen", "Önceki kazı sezonlarında kısmen kazılan")
S(p, "PLACE", "Kuzey Yamaç açmaları", "were left at", "her biri farklı seviyelerde", "her biri farklı seviyelerde bırakılan açmalar")
for a in ["C4b10", "C4c10", "C5b1", "C5b2"]:
    S(p, "WORK", a + " açması", "was excavated in", "2024 kazı sezonu",
      "2024 kazı sezonunda kazısı yapılan açmalar C4b10, C4c10, C5b1, C5b2 olmuştur")
S(p, "FIGURE", "Resim 4", "kind of image", "fotoğraf", "Bu fotoğraf aynı zamanda")
S(p, "FIGURE", "Resim 4", "shows", "2024 sezonu sonunda Kuzey Yamaç açmalarının kapanış durumu",
  "2024 sezonu sonunda Kuzey Yamaç açmalarının kapanış durumunu göstermektedir")

# ---------------------------------------------------------------- page 289
p = 289
S(p, "FIGURE", "Resim 5", "caption", "C4a6 açmasında yüzeyin 1 metre altında tespit edilen in situ kerpiç blok (35x35x12 cm).",
  "Resim 5: C4a6 açmasında yüzeyin 1 metre altında tespit edilen in situ kerpiç blok (35x35x12 cm).")
S(p, "MEASURE", "kerpiç blok", "[unclear] measures (caption; text on page 283 gives 35x3x12 cm)", "35x35x12 cm", "kerpiç blok (35x35x12 cm)")

# ---------------------------------------------------------------- page 290
p = 290
S(p, "FIGURE", "Resim 6", "caption", "C4a6-C4a7-C4b7 açmalarının İHA görüntüsü. C4a6’daki 2x1 m sondajda bulunan kerpiç bloğu korumak üzere naylon örtü vardır. [...] Üçüncü çöp çukuru açmanın güneydoğu köşesinde birkaç santimetre aşağıda çıkacaktır.",
  "Resim 6: C4a6-C4a7-C4b7 açmalarının İHA görüntüsü.")
S(p, "FIGURE", "Resim 6", "kind of image", "İHA görüntüsü", "açmalarının İHA görüntüsü")
S(p, "LAB", "kerpiç blok", "is protected by", "naylon örtü", "kerpiç bloğu korumak üzere naylon örtü vardır")
S(p, "BUILT", "eşik (C4a7-C4b7)", "separates", "C4a7 açmasını C4b7 açmasından", "C4a7 açmasını C4b7 açmasından ayıran eşiğin")
S(p, "BUILT", "çöp çukuru (C4a7, kuzey yarısı)", "position", "C4a7 açmasını C4b7 açmasından ayıran eşiğin hemen altında",
  "ayıran eşiğin hemen altında naylon örtü altında")
S(p, "BUILT", "çöp çukuru (C4a7, kuzey yarısı)", "shape", "dairesel form", "dairesel formda bir çöp çukurunun kuzey yarısı")
S(p, "LAB", "çöp çukuru (C4a7, kuzey yarısı)", "is covered by", "naylon örtü", "naylon örtü altında dairesel formda bir çöp çukurunun")
S(p, "BUILT", "diğer çöp çukuru (C4a7)", "position", "açmanın ortasında", "açmanın ortasında ise dairesel formda diğer bir çöp çukuru")
S(p, "BUILT", "diğer çöp çukuru (C4a7)", "shape", "dairesel form", "dairesel formda diğer bir çöp çukuru görülmektedir")
S(p, "BUILT", "üçüncü çöp çukuru (C4a7)", "position", "açmanın güneydoğu köşesinde", "Üçüncü çöp çukuru açmanın güneydoğu köşesinde")
S(p, "BUILT", "üçüncü çöp çukuru (C4a7)", "will appear at depth", "birkaç santimetre aşağıda", "birkaç santimetre aşağıda çıkacaktır")
S(p, "FIGURE", "Resim 7", "caption", "C4b10 açmasının 2024 kazı sezonu sonundaki görünümü. Fotoğrafın sol alt köşesine (batıya) doğru C4b9 açması yer almaktadır; bu Kuzey Yamaç’taki en derin açmadır.",
  "Resim 7: C4b10 açmasının 2024 kazı sezonu sonundaki görünümü.")
S(p, "FIGURE", "Resim 7", "kind of image", "fotoğraf", "Fotoğrafın sol alt köşesine (batıya) doğru")
S(p, "FIGURE", "C4b9 açması", "position in Resim 7", "fotoğrafın sol alt köşesine (batıya) doğru",
  "Fotoğrafın sol alt köşesine (batıya) doğru C4b9 açması yer almaktadır")
S(p, "PLACE", "C4b9 açması", "is", "Kuzey Yamaç’taki en derin açma", "bu Kuzey Yamaç’taki en derin açmadır")

# ---------------------------------------------------------------- page 291
p = 291
S(p, "FIGURE", "Resim 8", "caption", "Merkezi Kilise’nin karelajlarını gösteren harita. Bu İHA görüntüsü 2024 kazıları başlamadan önce alınmış olup Merkezi Kilise’nin güney sınırı boyunca (kabaca A4 ve A3 noktaları arasında) kazı yapılan açmaları göstermektedir. Kazılan açmalar kırmızı okun üst kısmındadır.",
  "Resim 8: Merkezi Kilise’nin karelajlarını gösteren harita.")
S(p, "FIGURE", "Resim 8", "kind of image", "harita / İHA görüntüsü", "Bu İHA görüntüsü")
S(p, "FIGURE", "Resim 8", "was taken", "2024 kazıları başlamadan önce", "Bu İHA görüntüsü 2024 kazıları başlamadan önce alınmış")
S(p, "PLACE", "kazı yapılan açmalar (Merkezi Kilise)", "position", "Merkezi Kilise’nin güney sınırı boyunca",
  "Merkezi Kilise’nin güney sınırı boyunca (kabaca")
S(p, "PLACE", "kazı yapılan açmalar (Merkezi Kilise)", "position", "A4 ve A3 noktaları arasında",
  "(kabaca A4 ve A3 noktaları arasında)", hedge="kabaca")
S(p, "FIGURE", "kazılan açmalar", "position in Resim 8", "kırmızı okun üst kısmında", "Kazılan açmalar kırmızı okun üst kısmındadır")
S(p, "FIGURE", "Resim 9", "caption", "E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi; tüm yapı malzemesi ikincil kullanımdır.",
  "Resim 9: E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği ve dikmesi; tüm yapı malzemesi ikincil kullanımdır.")
S(p, "BUILT", "kapı eşiği", "is located in", "E4d10 açması", "E4d10 açmasında kazı sırasında ortaya çıkarılan kapı eşiği")
S(p, "BUILT", "kapı dikmesi", "is located in", "E4d10 açması", "ortaya çıkarılan kapı eşiği ve dikmesi")
S(p, "BUILT", "kapı eşiği ve dikmesi (E4d10)", "building material", "tüm yapı malzemesi ikincil kullanım", "tüm yapı malzemesi ikincil kullanımdır")

# ---------------------------------------------------------------- page 292
p = 292
S(p, "FIGURE", "Resim 10", "caption", "E5c4 açmasında sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi ve üzerindeki duvar örgüsünü gösteren fotoğraf.",
  "Resim 10: E5c4 açmasında sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi ve üzerindeki duvar örgüsünü gösteren fotoğraf.")
S(p, "BUILT", "sarnıç", "is located in", "E5c4 açması", "E5c4 açmasında sarnıcın")
S(p, "BUILT", "taban döşemesi (E5c4)", "position", "sarnıcın hemen solunda (kuzeydoğusunda)", "sarnıcın hemen solunda (kuzeydoğusunda) taban döşemesi")
S(p, "BUILT", "duvar örgüsü (E5c4)", "lies above", "taban döşemesi", "taban döşemesi ve üzerindeki duvar örgüsünü")
S(p, "FIGURE", "Resim 11", "caption", "E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının birden fazla evresine ait duvarları gösteren fotoğraf.",
  "Resim 11: E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının birden fazla evresine ait duvarları gösteren fotoğraf.")
S(p, "BUILT", "yapı (E5b6)", "is located in", "E5b6 açması", "E5b6 açmasında Merkezi Kilise yapısının çevresinde bulunan yapının")
S(p, "BUILT", "yapı (E5b6)", "position", "Merkezi Kilise yapısının çevresinde", "Merkezi Kilise yapısının çevresinde bulunan yapının")
S(p, "BUILT", "duvarlar (E5b6)", "belong to phases", "yapının birden fazla evresi", "birden fazla evresine ait duvarları")

# ---------------------------------------------------------------- page 293
p = 293
S(p, "FIGURE", "Resim 12", "caption", "Merkezi Kilise’nin güney sınırı boyunca kazılan yedi 5x5 metre boyutlarındaki açmanın kapanış günündeki durumunu gösteren İHA fotoğrafı. Kazı yapılan açmalar kırmızı okun üst kısmındadır.",
  "Resim 12: Merkezi Kilise’nin güney sınırı boyunca kazılan yedi 5x5 metre boyutlarındaki açmanın kapanış günündeki durumunu gösteren İHA fotoğrafı.")
S(p, "FIGURE", "Resim 12", "kind of image", "İHA fotoğrafı", "durumunu gösteren İHA fotoğrafı")
S(p, "FIGURE", "kazı yapılan açmalar", "position in Resim 12", "kırmızı okun üst kısmında", "Kazı yapılan açmalar kırmızı okun üst kısmındadır")

json.dump(ST, open("/media/tugce/ProgramsVS/tez/v2/blind/test2/readerB/statements.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(len(ST))
