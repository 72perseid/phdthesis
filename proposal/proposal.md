# Arazi Verisini Kaynağında FAIR Kılmak: CIDOC CRM ile Uyumlu, Veri Modelcisi Gerektirmeyen Bir Kayıt Modeli

**Doktora tez önerisi taslağı, ikinci sürüm — görüşünüzü almak içindir**

Hazırlayan: Tuğçe Köseoğlu
Sunulan: Prof. Dr. Çiler Çilingiroğlu, Ege Üniversitesi, Arkeoloji Bölümü
Tarih: 20 Ekim 2026

Bu sürüm 29 Eylül tarihli ilk taslağın yerine geçer. Aradaki görüşmelerin ardından tezin sorusu, yöntemi ve veri kaynakları değişmiştir. Değişenleri belgenin sonunda ayrıca özetledim.

## 1. Şu anda ne üzerinde çalışıyorum

Türkiye'de bir kazının ya da yüzey araştırmasının ürettiği kayıt, onu üreten ekibin dışında kullanılamaz durumdadır. Kayıt kâğıt formlarda, Excel tablolarında, Word belgelerinde ve Bakanlığın envanter formlarında tutulur; her ekip kendi düzenini ve kendi terimlerini kullanır. Dışarıya yalnızca Kazı Sonuçları Toplantısı'ndaki damıtılmış rapor çıkar. Kayıt, ne başka bir araştırmacı tarafından bulunabilir, ne ona erişilebilir, ne başka bir kayıtla birleştirilebilir, ne de onu üretenler dışında biri tarafından yeniden kullanılabilir. Araştırma verisi için uluslararası ölçüt olan FAIR ilkelerinin dördü de karşılanmamaktadır.

Bu durumun gerekçeleri sorulduğunda, verilen yanıtlar arasında teknik olanlar vardır: standart yoktur, araç yoktur, ekipte bu işi yapacak kimse yoktur, zaman yoktur. Bu gerekçenin gerçek olup olmadığı hiç sınanmamıştır. Uluslararası standart, yani CIDOC CRM ve arkeoloji ekleri, yıllardır mevcuttur; üzerine kurulmuş açık kaynaklı araçlar da vardır. Türkiye'de hiçbir kazı ya da araştırma bunları kullanmamaktadır. Nedeni, bu araçların bir veri modelcisi, bir sunucu, İngilizce ve Türkiye'de var olmayan terim listeleri gerektirmesidir.

Üzerinde çalıştığım şey, bu teknik engeli ortadan kaldıran bir kayıt modelidir: arazide, telefonda ya da dizüstü bilgisayarda, çevrimdışı çalışan; kullanıcının listeden seçerek doldurduğu; arkada standarda uyan ve FAIR bir kayıt üreten; kurulması için modelci gerektirmeyen bir yapı. Tez, bu yapının gerçek arazi ekipleriyle ne ölçüde çalıştığını ve ürettiği kaydın ne ölçüde FAIR olduğunu ölçecektir.

Bu çalışmanın uzun vadeli hedefi bir TÜBİTAK 3005 başvurusudur. Belgenin büyük kısmı tezi anlatır; projeye ilişkin düşüncelerimi 10. bölümde özetledim.

## 2. İki temel kavram

### 2.1 CIDOC CRM nedir

CIDOC CRM, kültürel miras bilgisini tanımlamak için Uluslararası Müzeler Konseyi'nin (ICOM) belgeleme komitesi tarafından geliştirilen ve ISO standardı olan (ISO 21127) bir kavram modelidir. Bir yazılım ya da bir veritabanı değildir. Bir tür ortak dilbilgisidir: "kim, neyi, nerede, ne zaman, hangi olayda" sorularının nasıl ifade edileceğini belirler.

Modelin temel fikri, bilgiyi olaylar üzerinden kurmaktır. Bir Excel satırında "kandil, C3 açması, Roma Dönemi" yazar. CIDOC CRM aynı bilgiyi şöyle ifade eder: bir nesne vardır; bu nesne bir kazı etkinliği sırasında, belirli bir tabakada bulunmuştur; bir kişi bu nesneyi belirli bir gerekçeyle Roma Dönemi'ne tarihlemiştir. Fark şudur: ikinci ifadede tarihlemenin bir gözlem değil bir yorum olduğu, kimin yaptığı ve neye dayandığı da kayıtlıdır.

Çekirdek modelin arkeolojiye özgü ekleri vardır. CRMarchaeo kazıyı ve tabakalanmayı, CRMsci gözlemi, örnek almayı ve laboratuvar analizini, CRMgeo konumu ve koordinatı, CRMinf ise yorumu ve gerekçesini tanımlar. Yüzey araştırması için ayrı bir resmî ek yoktur; araştırma kayıtları gözlem ve örnek alma modülü üzerinden ifade edilir. Avrupa'daki arkeolojik veri altyapısı ARIADNE bu model üzerine kuruludur.

Modelin iki sınırı vardır. Birincisi, doğrudan kullanılamaz; uzmanlık ister ve aynı bilgiyi birkaç farklı biçimde ifade etmeye izin verir. İkincisi, sözcükleri vermez. Model bir buluntunun bir türü olduğunu söyler; türün "sikke" mi "coin" mi olduğunu, hangi listeden geldiğini söylemez. Sözcükler ayrı sözlüklerden gelir ve Türkçe arazi kayıtları için böyle bir sözlük yoktur.

### 2.2 FAIR ilkeleri nedir

FAIR, araştırma verisinin nasıl yönetilmesi gerektiğini tanımlayan ve 2016'da yayımlanan dört ilkenin baş harfleridir. Veri bulunabilir olmalıdır (Findable): kalıcı bir tanımlayıcısı ve tanımı olmalıdır. Erişilebilir olmalıdır (Accessible): ona nasıl ve hangi koşulla ulaşılacağı açık olmalıdır. Birlikte çalışabilir olmalıdır (Interoperable): ortak bir dil ve ortak sözlükler kullanmalıdır. Yeniden kullanılabilir olmalıdır (Reusable): lisansı, kaynağı ve nasıl üretildiği belli olmalıdır.

FAIR, açık veri ile aynı şey değildir. Bir veri seti ambargolu ya da erişime kapalı olabilir ve yine de FAIR olabilir; yeter ki var olduğu bilinsin ve erişim koşulu yazılı olsun. Bu ayrım bu tez için önemlidir. Araştırma başkanının yayın hakkı, Bakanlığın malzeme üzerindeki mülkiyeti ve buluntu yerlerinin korunması, verinin düzenli ve tanımlı tutulmasıyla çelişmez. Koordinatlar kapalı kalabilir; kaydın geri kalanı yine FAIR olabilir. "Olabildiğince açık, gerektiği kadar kapalı" ilkesi tezin varsayılan tutumudur.

Bu tezde dört ilkenin karşılığı şudur: standart ve sözlükler "birlikte çalışabilir" ve "yeniden kullanılabilir" ilkelerini karşılar; kalıcı tanımlayıcı, tanım ve lisans ise "bulunabilir" ve "erişilebilir" ilkelerini. Son ikisi ucuzdur, ancak en baştan tasarıma konması gerekir.

## 3. Tezin sorusu

**Sorun.** Türkiye'de arazi verisi FAIR değildir ve bunun teknik gerekçesi hiç sınanmamıştır.

**Soru.** Bir Türk arazi ekibi, veri modelcisi olmadan, doğrudan CIDOC CRM ile uyumlu ve FAIR bir yapıya kayıt tutabilir mi; kaydettiklerinin ne kadarı kayıt anında karşılaştırılabilir veriye dönüşür; ortaya çıkan kayıt hangi düzeyde FAIR'dir?

**Alt sorular ve her birinin kanıtı.**

| Alt soru | Kanıt |
|---|---|
| Yapı standarttan nasıl türetilir ve bu türetme başkası tarafından tekrarlanabilir mi | Yazılı bir yöntem ve her kararın gerekçesiyle tutulduğu bir karar günlüğü |
| Sözcükler nereden gelir | Arazi ekiplerinin kendi kayıtlarından ve dilinden derlenen, mümkün olduğunda uluslararası sözlüklerle eşlenen Türkçe listeler |
| Ekibe maliyeti nedir, okuyucuya getirisi nedir | Kayıt anında karşılaştırılabilir biçimde saklanan bilginin oranı; çıktının FAIR ölçütleriyle değerlendirilmesi; orada bulunmamış bir arkeoloğun kayıttan soruları yanıtlayabilmesi |

Tezin tartışma bölümünde savunulacak ikinci bir sav vardır: teknik engel bu düzeye indiğinde veri paylaşımının önünde ne kaldığı daha açık görülür. Bu savı tez kendi başına kanıtlamaz. İki araştırmanın başkanlarının, çalışma sonunda yapılandırılmış veriyi hangi koşullarla paylaşmaya karar verdikleri gözlenecek ve literatürdeki diğer engellerle (yayın önceliği, izin rejimi, güven, zaman) birlikte tartışılacaktır. Literatür, teknik engelin çoğu zaman asıl engel olmadığını söylemektedir; bu da bir bulgu olur.

## 4. Önerdiğim yöntem

### 4.1 Yapı standarttan türetilir

Arkeolog CIDOC CRM'i öğrenmek zorunda kalmamalıdır. Standart yapının içine yerleştirilir: kullanıcı bir form doldurur, her alanın standarttaki karşılığı önceden ve bir kez belirlenmiştir, standarda uygun çıktı kendiliğinden üretilir.

Yapı, standardın kendisinden türetilir; arazi kayıtları yalnızca sınama malzemesidir. Standart hangi şeyin bir nesne, hangisinin bir olay, hangisinin bir yer, hangisinin bir yorum olduğunu belirler; bunlar birbirinden ayrı kimliklerle tutulur. Standardın belirlemediği şeyler, yani hangi alanların zorunlu olduğu, bir torba seramiğin tek kayıt mı yirmi kayıt mı olduğu, hangi listenin hangi alana bağlandığı, insan kararıdır. Her böyle karar bir satır olarak günlüğe yazılır: karar, gerekçe, tarih, kişi. Bu günlük, yöntemin başkası tarafından tekrarlanabilmesinin güvencesidir.

Yapı modüllerden oluşur. Çekirdek modül her arazi çalışmasında bulunanları tutar: kişiler, yerler, dönemler, etkinlikler, nesneler, ölçümler. Üzerine yüzey araştırması, kazı ve tabakalanma, örnek ve analiz, yorum ve gerekçe, konum ve belgeleme modülleri gelir. Kullanılmayan modül boş kalır.

### 4.2 Sözcükler arazi pratiğinden gelir

Tezin asıl emeğinin burada olduğunu düşünüyorum. Standart yapıyı verir, sözcükleri vermez. Türkçe arazi terimleri için yerleşik bir sözlük yoktur; uluslararası sözlüklerde Türkçe karşılıklar yok denecek kadar azdır.

Listeler, ekiplerin fiilen kullandığı sözcüklerden derlenecektir: formlarındaki, tablolarındaki ve arazide bir buluntuyu tarif ederken söyledikleri her terim, neye işaret ettiğiyle birlikte. Her terim, varsa, uluslararası sözlükteki karşılığıyla eşlenir. Ekibin kendi terimi daima korunur; ekip kimseden izin almadan kendi terimini ya da kendi alanını ekleyebilir. Böyle eklemeler yalnızca o çalışma içinde karşılaştırılabilir kalır; birçok ekibin kullandığı bir ekleme sonradan ortak listeye alınır.

### 4.3 Kayıt aracı

Yapı ve listeler, arazide kullanılan bir araçta somutlaşır. Aracın özellikleri şunlardır: çevrimdışı çalışır, çünkü arazide bağlantı yoktur; telefonda ya da dizüstü bilgisayarda çalışır; kullanıcı listeden seçer, serbest metin yalnızca açıklama alanındadır; tekil buluntu için kart, toplu buluntu için tablo görünümü vardır, çünkü kimse iki yüz seramik parçasını tek tek anlatmaz; kurulumu modelci gerektirmez, çünkü yapı ve listeler hazır gelir; Bakanlığın envanter formlarını kayıttan kendiliğinden üretir.

Bu araç tezin savı değil, tezin ölçüm aletidir. İlk aşamada listeli bir elektronik tablo yeterlidir; uygulama ikinci arazi çalışmasına yetişmelidir.

### 4.4 Arkeolojik açıdan önemli üç karar

**Gözlem ile yorum ayrı tutulur.** "Bu birimde şu buluntu vardı" bir kayıttır. "Bu yerleşim Geç Roma Dönemi'ne aittir" bir yorumdur. Yapı, her yorumun kim tarafından, neye dayanarak ve ne kadar kesinlikle yapıldığını kaydeder. Çelişen iki yorum birlikte saklanır. "Muhtemelen" denilerek söylenen bir şey kesin bilgi olarak kaydedilmez. Formda bunun karşılığı, "ne gördüm" ile "ne düşünüyorum" alanlarının ayrı olmasıdır.

**Dönem bir ad değil, bir tanımdır.** "Neolitik" sözcüğü farklı bölgelerde ve farklı yazarlarda farklı yılları ifade eder. Her dönem, onu kimin tanımladığı, hangi bölge için geçerli olduğu ve hangi yılları kapsadığı ile birlikte saklanır.

**Yokluk da bir kayıttır.** Yürünmüş ve hiçbir şey bulunmamış bir birim ile hiç yürünmemiş bir birim aynı şey değildir. Yapı, "bakıldı, yoktu" bilgisini saklar; yoğunluk haritası için bu fark zorunludur.

## 5. Araştırma tasarımı

Tez iki yüzey araştırmasının verisiyle yürütülecektir. Bakanlığın envanter formu (Ek-21) yüzey araştırması ile kazı için tek formdur; bu nedenle tezin kapsamı "kazı verisi" değil "arazi verisi" olarak tanımlanmıştır.

**Birinci çalışma: tamamlanmış bir araştırma.** Onayınız olursa Karaburun yüzey araştırmasının kayıtlarını kullanmak istiyorum. Çalışma bitmiş olduğu için bu kayıtlar iki işe yarar. Birincisi, Türkçe listelerin ilk kaynağıdır: ekibin kullandığı her terim buradan derlenir. İkincisi, yapının tamamlanmış bir veri setine ne ölçüde uyduğunun sınamasıdır: kayıtların ne kadarı karşılaştırılabilir biçimde yerleşir, ne kadarı açıklama alanına düşer, nerede eksik liste, nerede eksik alan vardır. Ekibiniz çalışmayı tanıdığı için bu aşama yöntemi geliştirme aşamasıdır, bağımsız sınama değildir.

**İkinci çalışma: yeni bir araştırma.** Bağımsız sınama için başka bir başkanın yürüttüğü yeni bir yüzey araştırması gerekmektedir; Tokat Erbaa yüzey araştırması aday olarak görüşülmektedir. Burada kayıt, yapı ve listelerle, kayıt anında tutulacaktır. Mümkünse araziye kendim katılacağım. İlk sezonda yalnızca gözlem yapılır: ekip bugün nasıl kaydediyor, hangi form ve tablolarla, ve arazide söylenip de yazılmayan neler var. İkinci sezonda, ya da ekip kabul ederse ilk sezonda, kayıt yapı ile tutulur. Bu çalışma "modelci olmadan" savının sınandığı yerdir.

**Her iki çalışmada ölçülenler.** Karşılaştırılabilir biçimde saklanan bilginin oranı, tamamlanmış ve canlı kayıt için ayrı ayrı. Çıktının FAIR ölçütleriyle değerlendirilmesi; bunun için Avrupa altyapısının yayımladığı ölçütler kullanılacaktır. Devir sınaması: çalışmada bulunmamış bir arkeolog, önceden belirlenmiş bir soru listesini yalnızca kayıttan yanıtlamaya çalışır; önce ekibin kendi dosyalarından, sonra yapılandırılmış kayıttan. Son olarak, iki başkanın çalışma sonunda yapılandırılmış veriyi paylaşma kararı ve koşulları.

**Kazı modülü.** Yapıda kazı ve tabakalanma modülü vardır ve standarttan aynı yöntemle türetilmiştir; ancak elimde kazı kaydı olmadığı için bu modül tezde sınanmış bir sav olarak değil, tasarlanmış ve belgelenmiş bir parça olarak yer alacaktır. Bir açma kaydı bulunursa sınama eklenir. Bunu açıkça yazmayı, iddia etmemeye tercih ediyorum.

## 6. Hipotez

Sınanabilir kısım: standarttan türetilmiş bir yapı ve arazi pratiğinden derlenmiş listelerle, bir Türk arazi ekibinin kaydettiği bilginin büyük çoğunluğu kayıt anında karşılaştırılabilir ve FAIR biçimde tutulabilir, ekibe bir modelci ya da sunucu yükü getirmeden. Hedef oran olarak yüzde 95'i koyuyorum; bu bir hedeftir, ölçümden önce yazılmıştır ve ulaşılamazsa nerede ve neden ulaşılamadığı tezin bulgusu olur.

Tartışılacak kısım: teknik engel kalktığında paylaşımın önünde kalan engeller daha net görünür hâle gelir. Bu, iki başkanın kararı ve literatür üzerinden tartışılacaktır.

## 7. Ön deneme ve öğrettikleri

Bu tasarıma gelmeden önce, kendi başıma bir ön deneme yaptım: Kazı Sonuçları Toplantısı'ndaki birkaç bildiriyi standarda uygun bir yapıya aktarmayı ve kaybı ölçmeyi denedim. Bu deneme tezin parçası değildir ve sayıları tezde yer almayacaktır; yayımlanmış rapor damıtılmış bir metindir ve arazi kaydını temsil etmez.

Deneme üç şey öğretti ve üçü de tasarıma girdi. Yapı, standarttan yazılı bir yöntemle türetilebilir ve bu tekrarlanabilir. Kaybın büyük kısmı yapıdan değil sözcüklerden gelir: tablo ve alan mevcutken Türkçe terim listede yoktur. Ve serbest metinden yapıya aktarmak, listeden seçerek kaydetmekten çok daha fazla kaybettirir; bu da kaydı kaynağında tutmanın, sonradan aktarmaya göre neden doğru sıra olduğunu gösterir.

## 8. Tezin kapsamı dışında bırakılanlar

Bu sürümde üç şeyi bilinçli olarak tezin dışına çıkardım.

**Büyük dil modelleri.** İlk taslakta modeller yöntemin yarısıydı. Kayıt listeden seçerek tutulduğunda modele gerek kalmamaktadır; tezin çekirdeği modelsiz çalışır. Modellerin yeri, mevcut arşivlerin, yani yıllardır birikmiş Excel ve defterlerin, sonradan yapıya aktarılmasıdır. Bu, tezin değil sonraki adımın işidir ve 10. bölümdeki projede yer alır. Veri egemenliği kaygısı geçerliliğini korur ve orada ele alınır.

**Arşivlerin geriye dönük aktarımı.** Yukarıdaki nedenle, tezden sonra.

**Kazı modülünün sınanması.** Kazı kaydı elde edilene kadar, 5. bölümde açıklandığı gibi.

## 9. Tez taslağı

1. Giriş: Türkiye'de arazi verisi neden FAIR değil, teknik gerekçe ve araştırma soruları
2. Kavramlar: CIDOC CRM ve arkeoloji ekleri, FAIR, açık veri ile farkı, Bakanlık mevzuatı ve envanter formları
3. Önceki çalışmalar: Avrupa altyapısı ve mevcut araçlar, neden Türkiye'de kullanılmadıkları, Türkiye'deki envanter ve sözlük girişimleri
4. Yöntem: yapının standarttan türetilmesi ve karar günlüğü; listelerin derlenmesi; kayıt aracı; ölçütler
5. Birinci çalışma: tamamlanmış araştırma kaydının yapıya uyumu ve listelerin derlenmesi
6. İkinci çalışma: yeni araştırmada kayıt anında kayıt
7. Bulgular: kapsama oranları, FAIR değerlendirmesi, devir sınaması, paylaşım kararları
8. Tartışma: teknik engel kalkınca ne kalıyor
9. Sonuç ve sonraki adımlar

## 10. Tezi destekleyecek proje: TÜBİTAK 3005

### 10.1 Program ve modül

TÜBİTAK 3005 programı 10 Eylül 2026'da iki modül olarak yeniden açılmıştır. Her iki modülde de proje süresi en fazla 24 ay, destek üst sınırı burslar hariç 1.200.000 TL'dir ve başvuru yıl boyunca yapılabilmektedir. Modülün amacına uymayan öneriler bilimsel değerlendirmeye alınmadan iade edilmektedir.

Başvuruyu 3005-B, Teknolojik İlerlemelerin Toplumsal Etkileri Modülü'ne yapmayı öneriyorum. Bu modül, yüksek teknolojilerin toplumsal etkilerini mühendislik bilimleriyle eş güdüm içinde ele alan ve toplumsal fayda hedefleyen sosyal ve beşeri bilimler araştırmalarını desteklemektedir. 3005-A bir kamu kurumuyla doldurulmuş iş birliği formu istemektedir; 3005-B'de böyle bir koşul yoktur.

### 10.2 Projenin savı ve tezle iş bölümü

Tez, kaydı kaynağında FAIR kılan yapıyı iki araştırmada sınar. Proje, tezin bilinçli olarak dışında bıraktığı iki şeyi üstlenir: mevcut arşivlerin yapıya aktarılması ve bunun arkeologların çalışması üzerindeki etkisinin ölçülmesi.

Arşiv aktarımı, modülün istediği yüksek teknoloji bileşenidir. Yıllardır birikmiş Excel tabloları ve defterler elle aktarılamayacak kadar çoktur; büyük dil modelleri bu işi yapabilir. Ancak yayımlanmamış miras verisi yurt dışındaki şirket sunucularına gönderilemez. Proje, aynı işin araştırmacının kendi sunucusunda çalışan açık kaynaklı modellerle ne ölçüde yapılabildiğini, tezin listeleri ve yapısı hedef alınarak ölçer. Tezde elde edilen listeler bu aktarımın ön koşuludur; listeler olmadan aktarımın neden başarısız olduğunu ön denemede gördüm.

Toplumsal etki, modülün asıl sorusudur. Proje şunları ölçecektir: bir araştırmacı başka bir çalışmanın verisini anlamak için ne kadar zaman harcıyor ve yapı bu süreyi kısaltıyor mu; teknik eğitimi olmayan bir ekip, kurulumdan ilk sezona kaç saatte geçiyor; yapıyı kullanan ekipler veri paylaşımı konusunda ne diyor ve ne yapıyor. Son soru için gerekirse etik kurul onayıyla bir anket yapılır; bu, tezin değil projenin işidir.

| Tezde kalan | Projenin eklediği |
|---|---|
| Yapının standarttan türetilmesi ve karar günlüğü | Daha çok sayıda kazı ve araştırma ile sınama |
| İki araştırmadan derlenen Türkçe listeler | Listelerin ulusal bir sözlüğe genişletilmesi |
| Kayıt aracı ve iki arazi sınaması | Aracın ekiplere kurulumu, eğitim, sunucu ve donanım |
| FAIR değerlendirmesi ve devir sınaması | Mevcut arşivlerin yerel modellerle aktarımı ve bunun ölçümü |
| İki başkanın paylaşım kararı | Ekiplerle anket ve etkinin ölçümü |

Proje kabul edilmese de tez kendi başına savunulabilir olmalıdır; tablo bu ayrımı korumak için düzenlenmiştir.

### 10.3 Proje ekibi

Programın kurallarına göre proje yürütücüsünün doktora derecesine sahip ve kadrolu olması gerekmektedir; doktora öğrencileri yürütücü olamaz, bursiyer olarak yer alabilir. Bu nedenle projenin yürütücülüğünü sizin üstlenmenizi rica ediyorum. Ben projede doktora bursiyeri olarak yer alırım.

Mühendislik tarafında Ege Üniversitesi Bilgisayar Mühendisliği Bölümü Başkanı Prof. Dr. Murat Osman Ünalır ile ilerliyoruz. Çalışma alanları ontoloji mühendisliği, anlamsal ağ, birlikte çalışabilirlik ve makine öğrenmesidir. Kendisiyle yaptığımız görüşmeler bu sürümdeki değişikliklerin bir kısmının kaynağıdır: kaydı kaynağında tutan, model gerektirmeyen bir araç ve arşiv aktarımının sonraki adım olması onun önerisidir. Programın kuralına göre profesör unvanlı kişiler projede araştırmacı olarak görev alamamaktadır; bu nedenle Ünalır hoca danışman olarak yer alabilir, araştırmacı görevi için kendi grubundan bir öğretim üyesinin katılması uygun olur.

| Görev | Kişi |
|---|---|
| Proje yürütücüsü | Prof. Dr. Çiler Çilingiroğlu |
| Danışman | Prof. Dr. Murat Osman Ünalır, bilgisayar mühendisliği |
| Araştırmacı | Bilgisayar mühendisliğinden bir öğretim üyesi; belirlenecek |
| Doktora bursiyeri | Tuğçe Köseoğlu |
| Diğer bursiyerler | Kayıtları denetleyecek ve arşiv aktarımını karşılaştıracak arkeoloji öğrencileri |

[TODO: bütçe] [TODO: iş paketleri ve takvim] [TODO: araştırmacı adı]

## 11. İlk taslağa göre değişenler

Tezin sorusu, "kazı verisi için ortak bir yapı"dan "arazi verisini kaynağında FAIR kılmak ve teknik gerekçeyi sınamak"a dönüştü. Büyük dil modelleri tezin çekirdeğinden çıktı ve projeye taşındı. Kazı Sonuçları Toplantısı ön denemesi tezin dışına alındı; yalnızca öğrettikleri kaldı. Veri kaynağı, yayımlanmış raporlar yerine iki yüzey araştırması oldu; kapsam "kazı" yerine "arazi" olarak tanımlandı. Kazı modülünün sınanmamış olduğu açıkça yazıldı.

## 12. Size sorularım

1. **Karaburun kayıtları.** Bu kayıtları tezde kullanmama izin verir misiniz? Veri yalnızca kendi bilgisayarımda tutulacak, koordinatlar dâhil hiçbir şey onayınız olmadan yayımlanmayacaktır. Kayıtların hangi biçimde (Access, Excel, form) ve hangi kapsamda olduğunu öğrenmek istiyorum.
2. **İkinci araştırma.** Tokat Erbaa yüzey araştırması için başkanla temas kurmamda yardımcı olabilir misiniz, ya da daha uygun bulduğunuz bir araştırma var mı? Gerekli olan, başkanın yazılı izni ve neyin yayımlanabileceğine dair bir satırdır.
3. **Eş danışman.** Tezin yapı ve standart kısmı için Ünalır hocanın ikinci tez danışmanı olmasını uygun bulur musunuz?
