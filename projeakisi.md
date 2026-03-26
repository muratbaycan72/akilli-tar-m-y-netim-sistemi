# Akıllı Tarım Yönetim Sistemi - Proje Akışı ve Haftalık İlerleme

Bu dosya, Algoritma Alimleri takımının haftalık proje ilerlemesini ve üyelerin görev dağılımlarını içermektedir.

## 1. Hafta (7-12 Mart)
Murat Baycan (Scrum Master / Yönetici): GitHub reposu oluşturuldu, Trello ve Discord iletişim kanalları kuruldu. Proje akış dokümanı eklendi.
Selahattin Ali Kılıç : Teknoloji araştırması ve seçimi üzerinde çalışıyor.
Ömer Akhan: Geliştirme ortamı kurulumu üzerinde çalışıyor.
Binnur Aslan: Proje analizi ve kapsam tanımı üzerinde çalışıyor.
Ülkü Tuana Kara: Gereksinim toplama ve belgeleme üzerinde çalışıyor. 


 
Murat Baycan :
# 🚀 Algoritma Alimleri Sprint Planı

## 🎯 Hedef
Geliştirme ortamımızın (Python) kurulumunun ardından, projemizde kullanacağımız temel veri yapıları ve algoritmaların analizini yapmak ve pratik uygulamalarla temeli sağlamlaştırmak.

## 📚 Odaklanılacak Konular
Bu hafta ağırlıklı olarak şu 4 temel konuya odaklanıyoruz:
1. **Diziler (Python Lists):** Veri saklama ve indeksleme mantığı.
2. **Bağlı Listeler (Linked Lists):** OOP ile `Node` sınıfı oluşturma ve dinamik veri yönetimi.
3. **Arama Algoritmaları:** Linear Search ve Binary Search.
4. **Sıralama Algoritmaları:** Bubble Sort ve Insertion Sort. 

## 📖 Öğrenme Kaynakları
- Fırat Üniversitesi ders notları ve slaytları.
- *Grokking Algorithms* (Aditya Bhargava) - İlgili bölümler.
- LeetCode ve HackerRank (Python 3 çözümleri).

## 🛠️ Pratik Uygulama Örnekleri
- [ ] **Örnek 1:** Fenerbahçe maç istatistiklerini tutan bir liste oluşturup, yazacağımız özel bir *Bubble Sort* fonksiyonu ile sıralamak.
- [ ] **Örnek 2:** Proje görevlerimizi ekleyip silebileceğimiz, sıfırdan yazılmış bir `LinkedList` yapısı kurgulamak.
- [ ] **Örnek 3:** İstatistik listesi üzerinde *Binary Search* ile belirli bir veriyi bulma fonksiyonu yazmak.



*Not: Lütfen kodları yazarken Python standartlarına (PEP 8) uymaya özen gösterelim ve commit mesajlarımızı açıklayıcı yazalım.*

Ülkü Tuanna Kara : 
Proje konusu ve kapsamı:
Günümüzde tarım sektöründe su kaynaklarının verimli kullanılması, ürün veriminin artırılması ve çevresel etkilerin azaltılması büyük önem taşımaktadır. Akıllı Tarım Yönetim Sistemi, sensör verileri ve makine öğrenmesi teknolojilerini kullanarak tarımsal üretim süreçlerini daha verimli, sürdürülebilir ve otomatik hale getirmeyi amaçlayan bir yazılım sistemidir. Bu proje,  bahsedilen problemlere teknolojik çözümler sunmayı hedeflemektedir. 
Sistem, tarım alanına yerleştirilen sensörler aracılığıyla toprak nemi, sıcaklık, hava durumu ve diğer çevresel verileri sürekli olarak toplar. Toplanan bu veriler bir sunucuya iletilerek veritabanında saklanır ve makine öğrenmesi algoritmaları kullanılarak analiz edilir. Analiz sonuçlarına göre sistem, sulama, gübreleme ve ilaçlama gibi tarımsal işlemler için öneriler üretir veya otomatik kontrol mekanizmaları aracılığıyla bu işlemleri gerçekleştirebilir.
Kullanıcılar, geliştirilecek olan bu web tabanlı arayüz sayesinde tarım alanlarındaki sensör verilerini takip edebilir. Takip edilen bu analiz sonuçlarını görüntüleyebilir ve gerekli durumlarda müdahale edilebilir. Bu sayede çiftçiler tarım süreçlerini daha bilinçli şekilde yönetebilir ve kaynak kullanımını optimize edebilirler.
Sonuç olarak Akıllı Tarım Yönetim Sistemi, tarımsal üretimde dijital dönüşümü destekleyen, veri odaklı karar verme süreçlerini geliştiren ve üretim verimliliğini artırmayı hedefleyen yenilikçi bir çözüm sunmaktadır.
Sistem amaçları: 
Sistemin temel amaçlarından biri elde edilen verileri analiz ederek tarımsal üretim süreçlerini daha verimli hale getirmektir.
Tarımda su, gübre ve ilaç gibi kaynakların gereksiz kullanımını önlemek.
Bu sistem sensör verilerini kullanarak bazı tarımsal işlemleri otomatik hale getirmeyi hedefler.
Makine öğrenmesi algoritmaları kullanılarak geçmiş veriler analiz edilir ve gelecekte oluşabilecek durumlar hakkında tahminler yapılır. Bu sayede olası riskler önceden tespit edilebilinir. 



Fonksiyonel Gereksinimler :
Sensör verisi toplama: Sistem, tarım alanında bulunan sensörlerden toprak nemi verisini toplayabilmelidir. Sistem, sensörlerden sıcaklık ve nem gibi çevresel verileri alabilmelidir. Sistem, sensörlerden gelen verileri belirli zaman aralıklarında otomatik olarak almalıdır.
Veri Saklama : Sistem, sensörlerden gelen tüm verileri veritabanında saklamalıdır. Sistem, geçmiş sensör verilerini saklayarak daha sonra analiz edilmesini sağlamalıdır.
Veri Analizi: Sistem, toplanan sensör verilerini analiz edebilmelidir. Sistem, makine öğrenmesi algoritmaları kullanarak tarımsal süreçler hakkında tahminler oluşturmalıdır.
Sulama Öneri Sistemi :  Sistem, toprak nem seviyesine göre sulama önerisi oluşturmalıdır. Sistem, gerektiğinde sulama işlemini otomatik olarak başlatabilmelidir (sistem donanımı destekliyorsa).
Kullanıcı Yönetimi: Sistem kullanıcıların kayıt olmasını sağlamalıdır. Sistem kullanıcıların giriş yapmasını sağlamalıdır. Sistem kullanıcı bilgilerini güvenli şekilde saklamalıdır.
Web Arayüzü: Sistem, kullanıcıların sensör verilerini web arayüzü üzerinden görüntülemesine izin vermelidir. Sistem, kullanıcıların geçmiş sensör verilerini grafik veya rapor olarak görüntülemesini sağlamalıdır.
Mobil Uygulama: Sistem, kullanıcıların mobil uygulama üzerinden sensör verilerini görüntülemesini sağlamalıdır. Sistem, kullanıcıya gerekli durumlarda bildirim göndermelidir.
Bildirim Sistemi :  Sistem, toprak nemi kritik seviyeye düştüğünde kullanıcıya bildirim göndermelidir. Sistem, sistem tarafından oluşturulan önerileri kullanıcıya iletmelidir.




Teknik Gereksinimler :
Sunucu Tarafı Gereksinimler: Sistemin arka planında çalışan ve sensör verilerini işleyen sunucu tarafı yazılımı Python programlama dili kullanılarak geliştirilecektir. Python, veri analizi ve makine öğrenmesi uygulamaları için güçlü kütüphanelere sahip olduğu için tercih edilmektedir.
Makine Öğrenmesi Gereksinimleri: Sistem, sensörlerden elde edilen verileri analiz etmek ve tarımsal tahminler oluşturmak amacıyla makine öğrenmesi algoritmaları kullanacaktır. Bu amaçla TensorFlow kütüphanesi kullanılacaktır.
TensorFlow ile geliştirilecek modeller şu amaçlarla kullanılabilir:
-Toprak nemi analizleri
-Sulama önerisi oluşturma
-Bitki sağlığı tahmini
-Verim tahmini
Sensör Veri İletişim Gereksinimleri: Tarım alanına yerleştirilen sensörlerden elde edilen verilerin sisteme iletilmesi için MQTT (Message Queuing Telemetry Transport) protokolü kullanılacaktır.
Veritabanı Gereksinimleri: Sistem, sensör verilerini, kullanıcı bilgilerini ve analiz sonuçlarını saklamak için PostgreSQL veritabanını kullanacaktır. PostgreSQL veritabanı şu verileri saklayacaktır:
-Sensör verileri
-Kullanıcı hesapları
-Sistem tarafından üretilen analiz sonuçları
-Geçmiş veri kayıtları
Web Arayüzü Gereksinimleri:  Kullanıcıların sistemdeki verileri görüntüleyebilmesi ve yönetebilmesi için React tabanlı bir web arayüzü geliştirilecektir.
Web arayüzü sayesinde kullanıcılar:
-Sensör verilerini görüntüleyebilir
-Analiz sonuçlarını inceleyebilir
-Sistem önerilerini takip edebilir.


Mobil Uygulama Gereksinimleri:  Sisteme mobil cihazlardan erişim sağlamak için React Native kullanılarak bir mobil uygulama geliştirilecektir. Mobil uygulama kullanıcıların:
-Sensör verilerini görüntülemesine
-Bildirim almasına
-Tarım süreçlerini takip etmesine olanak sağlar.
Geliştirme Ortamı Gereksinimleri:  Projenin geliştirilmesi için aşağıdaki araçlar kullanılacaktır:
-Visual Studio Code → Kod geliştirme ortamı
-Python → Backend geliştirme
-Node.js → Frontend geliştirme için gerekli ortam
-PostgreSQL → Veritabanı yönetimi

Performans Gereksinimleri : 
Veri İşleme Hızı:  Sistem, sensörlerden gelen verileri en fazla 5 saniye içinde işleyebilmelidir. Sistem, sensörlerden gelen verileri gerçek zamanlıya yakın bir şekilde analiz edebilmelidir.
Sistem Kapasitesi: Sistem aynı anda en az 1000 sensörden gelen veriyi işleyebilmelidir. Sistem aynı anda birden fazla kullanıcının web veya mobil uygulama üzerinden sisteme erişmesini desteklemelidir.
Sistem Yanıt Süresi: Sensör verileri sistemde düzenli aralıklarla güncellenmeli ve kullanıcı arayüzüne yansıtılmalıdır.
Sistem Güvenilirliği: Sistem kesintisiz çalışabilmeli ve veri kaybını önleyecek mekanizmalara sahip olmalıdır. Sistem arızası durumunda veriler güvenli şekilde korunmalıdır.
Ölçeklenebilirlik: Sistem ileride sensör sayısı arttığında veya kullanıcı sayısı yükseldiğinde performans kaybı yaşamadan çalışabilecek şekilde tasarlanmalıdır.

Güvenlik Gereksinimleri: 
Kullanıcı Kimlik Doğrulama: Sisteme erişen kullanıcılar giriş yapmadan sistem özelliklerini kullanamamalıdır. Kullanıcılar sisteme kullanıcı adı ve şifre ile giriş yapmalıdır. Kullanıcıların hesap bilgileri güvenli şekilde saklanmalıdır.
Yetkilendirme: Sistem farklı kullanıcı rollerini desteklemelidir. Kullanıcılar yalnızca kendi yetkileri dahilindeki işlemleri gerçekleştirebilmelidir.
Veri Güvenliği: Kullanıcı şifreleri veritabanında şifrelenmiş (hashlenmiş) olarak saklanmalıdır. Hassas veriler güvenli şekilde depolanmalıdır. Sistem veri kaybını önlemek için düzenli veri yedekleme mekanizmasına sahip olmalıdır.
Güvenli Veri İletişimi: Sensörlerden gelen veriler güvenli bir iletişim protokolü üzerinden gönderilmelidir. Web ve mobil uygulama ile sunucu arasındaki veri iletişimi HTTPS kullanılarak yapılmalıdır.
API Güvenliği: Sistem API’lerine erişim kimlik doğrulama tokenları ile korunmalıdır. Yetkisiz kullanıcıların API erişimi engellenmelidir.
Sistem Koruması: Sistem yetkisiz erişim girişimlerini tespit edebilmelidir. Sistem saldırılara karşı temel güvenlik önlemlerine sahip olmalıdır.

Gereksinim Önceliklendirmesi
Yüksek Öncelikli Gereksinimler
Bu gereksinimler sistemin temel çalışmasını sağlayan ve mutlaka gerçekleştirilmesi gereken özelliklerdir. Sistem bu özellikler olmadan çalışamaz.
-Sensörlerden veri toplama sistemi
-Sensör verilerinin veritabanında saklanması
-Sensör verilerinin analiz edilmesi
-Toprak nemine göre sulama önerisi oluşturulması
-Kullanıcı kayıt ve giriş sistemi
-Web arayüzü üzerinden sensör verilerinin görüntülenmesi
-Sensör verilerinin düzenli olarak güncellenmesi
Orta Öncelikli Gereksinimler
Bu gereksinimler sistemin kullanımını geliştiren ve kullanıcı deneyimini artıran özelliklerdir. Ancak sistem temel işlevlerini bu özellikler olmadan da gerçekleştirebilir.
-Mobil uygulama üzerinden sensör verilerinin görüntülenmesi
-Kullanıcılara bildirim gönderme sistemi
-Sensör verilerinin grafik ve rapor olarak gösterilmesi
-Makine öğrenmesi ile tahmin analizlerinin yapılması
Düşük Öncelikli Gereksinimler
Bu gereksinimler sistemin gelişmiş özelliklerini içerir ve projenin ilerleyen aşamalarında geliştirilebilir.
-Gelişmiş veri analiz raporları
-Uzun vadeli tarım verim tahminleri
-Kullanıcıların farklı tarım alanlarını karşılaştırabilmesi
-Gelişmiş veri görselleştirme araçları
 
Binnur Aslan: 

AKILLI TARIM YÖNETİM SİSTEMİ (ATYS)

1.	Projenin Amacı ve Genel Hedefleri 
Akıllı Tarım Yönetim Sistemi (ATYS), tarımsal süreçleri IoT (Nesnelerin İnterneti) tabanlı sensör verileri ve makine öğrenimi algoritmalarıyla optimize etmeyi amaçlayan entegre bir yazılım çözümüdür.
•	Temel Hedef: Toprak nemi, hava durumu ve bitki sağlığı verilerini anlık olarak analiz ederek sulama, gübreleme ve ilaçlama süreçlerinde karar destek mekanizmaları sunmak ve bu işlemleri otomatize etmektir.
•	İş Hedefleri: Su, gübre ve enerji gibi kaynakların israfını önlemek, insan hatasını minimize etmek ve toplam tarımsal verimliliği artırmak.

2.	Paydaş Analizi ve Beklentiler 
Yazılım süreçlerinde gereksinimlerin doğru belirlenmesi için temel paydaş beklentileri şu şekilde analiz edilmiştir:
•	Son Kullanıcılar (Çiftçiler ve Tarım İşletmecileri): Teknik bilgi gerektirmeyen, sade ve anlaşılır bir kullanıcı arayüzü (Mobil ve Web). Kritik durumlarda (don tehlikesi, aşırı kuraklık, hastalık riski) anlık bildirimler ve uyarılar alabilme.
•	Ziraat Uzmanları / Danışmanlar: Sahadan toplanan tarihsel verilerin (nem, sıcaklık rejimleri) detaylı olarak raporlanabilmesi. Makine öğrenimi tahminlerinin ziraat bilimiyle tutarlı ve yüksek doğruluk oranına sahip olması.
•	Sistem Yöneticileri: Sensörlerden gelen sürekli veri akışının kopmadan işlenmesi, sistemin ölçeklenebilir ve güvenli olması.

3.	Proje Kapsamı (In-Scope) 
Proje dahilinde geliştirilecek ve teslim edilecek fonksiyonel süreçler şunlardır:
•	Sensör Veri Toplama ve İşleme Modülü: Sahadaki IoT cihazlarından (toprak nemi, hava durumu sensörleri) gelen verilerin MQTT protokolü kullanılarak toplanması, Python ile işlenip temizlenmesi ve PostgreSQL veritabanında yapılandırılmış olarak depolanması.
•	Makine Öğrenimi Tabanlı Tahmin Algoritmaları: TensorFlow altyapısı kullanılarak, geçmiş veriler ve anlık sensör okumaları üzerinden "Optimum Sulama Zamanı", "Hastalık/Zararlı Riski Tahmini" gibi çıktılar üreten modellerin entegrasyonu.
•	Kullanıcı Arayüzleri: Kullanıcıların sistemin anlık durumunu izleyebileceği, raporlar alabileceği ve gerektiğinde sistemi manuel olarak yönetebileceği React tabanlı bir Web Paneli ve eşzamanlı çalışan bir Mobil Uygulama geliştirilmesi.


4.	Proje Sınırları ve Kapsam Dışı Unsurlar (Out-of-Scope) 
"Scope Creep" (kapsam kayması) riskini önlemek adına aşağıdaki unsurlar projenin sınırları dışında bırakılmıştır:
•	Donanım Üretimi ve Montajı: Fiziksel sensörlerin, sulama motorlarının, vanaların veya kablolama altyapısının üretimi ve tarlaya fiziksel montajı. (Proje geliştirme sürecinde sensör verileri simüle edilecek veya hazır API/geliştirme kartları kullanılacaktır).
•	Otonom Tarım Araçları: Traktör veya tarım dronları gibi otonom donanımların kontrol yazılımları bu projeye dahil değildir.
•	Kimyasal Analizler: Gübre veya tarımsal ilaçların laboratuvar düzeyindeki kimyasal analizleri yazılımın kapsamında değildir; sistem sadece sensör okumalarına dayalı tahminsel öneriler sunar.

5.	Teslim Edilecekler ve Teknoloji Yığını 
Proje sonunda aşağıdaki teslimatlar belirtilen teknoloji yığını ile sağlanacaktır:
•	Backend & Veri Akışı: Python, MQTT
•	Veritabanı: PostgreSQL
•	Yapay Zeka & Analiz: TensorFlow
•	Frontend & Arayüzler: React (Web), Cross-platform Mobil Uygulama

6.	Ölçülebilir Başarı Kriterleri (KPI'lar) 
Sistemin başarısını ve gereksinimleri karşılayıp karşılamadığını somut verilerle değerlendirebilmek için aşağıdaki hedefler belirlenmiştir:
•	Performans ve Yanıt Süresi: Sensörlerden toplanan verilerin işlenip kullanıcı arayüzüne (Web/Mobil) yansıma süresinin maksimum 2 saniye olması.
•	Model Doğruluğu (Accuracy): TensorFlow ile geliştirilen makine öğrenimi modelinin, bitki hastalığı veya kuraklık riski tahminlerinde %85 ve üzeri doğruluk oranına ulaşması.
•	Sistem Erişilebilirliği (Uptime): Bulut tabanlı sunucuların (PostgreSQL ve Backend) ve API'lerin %99.9 oranında kesintisiz hizmet vermesi.
•	Kaynak Optimizasyonu Hedefi: Geliştirilen karar destek sisteminin, simülasyon ortamında geleneksel yöntemlere kıyasla su ve enerji tüketimini en az %20 oranında azaltabileceğinin teorik olarak kanıtlanması.



7.	Olası Proje Riskleri, Kısıtlar ve Çözüm Stratejileri 
Yazılımın geliştirilme ve canlıya alınma süreçlerinde karşılaşılabilecek teknik riskler ve bunlara karşı geliştirilen hafifletme (mitigation) planları şunlardır:
•	İnternet Bağlantısı Kopuklukları (Risk): Kırsal alanlarda IoT cihazlarının ağ bağlantısını kaybetmesi veri kaybına veya karar mekanizmasının aksamasına yol açabilir.
•	Çözüm Stratejisi: Sensör düğümlerine (node) yerel önbellekleme (local caching) mekanizması eklenerek, bağlantı koptuğunda verilerin geçici olarak tutulması ve bağlantı sağlandığında MQTT üzerinden geriye dönük aktarılması.
•	Sensör Donanım Arızaları (Risk): Yanlış kalibrasyon veya fiziksel hasar nedeniyle sisteme hatalı veri akışı (örneğin yağmurlu havada toprağın %0 nemli görünmesi).
•	Çözüm Stratejisi: Yazılım tarafında anomali tespiti (anomaly detection) algoritmaları kurularak, mantık dışı değerler okunduğunda sistemin otomatik sulamayı durdurması ve kullanıcıya "Sensör Arızası Şüphesi" bildirimi göndermesi.
•	Veri Gizliliği ve Güvenliği (Kısıt): Toplanan tarımsal verilerin ve sisteme kayıtlı kullanıcı bilgilerinin yetkisiz erişime karşı korunması zorunluluğu.
•	Çözüm Stratejisi: Veritabanı (PostgreSQL) bağlantılarında ve API haberleşmelerinde uçtan uca şifreleme kullanılması, kullanıcı yetkilendirme adımlarının (Role-Based Access Control) eksiksiz uygulanması.

Selahattin Ali Kılıç:
1. Projenin Amacı 
Akıllı tarım sistemleri sensörlerden elde edilen çevresel verileri analiz ederek tarımsal üretim 
süreçlerini daha verimli hale getirmeyi amaçlayan sistemlerdir. Bu projede amaç; toprak 
nemi, hava durumu ve bitki sağlığı gibi verileri analiz ederek sulama, gübreleme ve hastalık 
yönetimi gibi süreçleri optimize eden bir sistem tasarlamaktır. Sensörlerden elde edilen veriler 
analiz edilerek çiftçilere doğru zamanda doğru müdahaleyi yapabilmeleri için öneriler 
sunulacaktır. 
2. Sistem İçin Gerekli Teknolojiler 
Akıllı tarım sistemi geliştirirken farklı yazılım ve donanım teknolojilerinin birlikte 
kullanılması gerekmektedir. Bu sistemde sensörlerden veri toplanması, verilerin işlenmesi, 
analiz edilmesi ve kullanıcıya sunulması için çeşitli teknolojilere ihtiyaç duyulmaktadır. 
Bu proje kapsamında aşağıdaki teknoloji alanları kullanılacaktır: 
 Backend geliştirme 
 Sensör veri iletişimi 
 Makine öğrenmesi 
 Veritabanı yönetimi 
 Kullanıcı arayüzü 
3. Teknoloji Analizi 
Backend – Python 
Python veri analizi ve makine öğrenmesi alanlarında oldukça yaygın kullanılan bir 
programlama dilidir. Geniş kütüphane desteği sayesinde sensör verilerinin işlenmesi ve 
sistemin backend tarafının geliştirilmesi için uygun bir seçenektir. 
Makine Öğrenmesi – TensorFlow 
TensorFlow yapay zeka ve makine öğrenmesi uygulamaları geliştirmek için kullanılan güçlü 
bir kütüphanedir. Sensörlerden elde edilen veriler kullanılarak sulama tahmini, bitki stres 
analizi ve verim tahmini gibi modeller oluşturulabilir. 
Sensör Veri İletişimi – MQTT 
MQTT, IoT sistemleri için geliştirilmiş hafif bir iletişim protokolüdür. Sensörlerden gelen 
verilerin düşük bant genişliği kullanarak hızlı ve güvenilir bir şekilde sisteme aktarılmasını 
sağlar. 
Veritabanı – PostgreSQL 
PostgreSQL güçlü ve güvenilir bir açık kaynak veritabanı sistemidir. Sensörlerden elde edilen 
verilerin saklanması, yönetilmesi ve analiz edilmesi için uygun bir altyapı sunar.
Web Arayüzü – React 
React modern web uygulamaları geliştirmek için kullanılan popüler bir JavaScript 
kütüphanesidir. Kullanıcıların sensör verilerini grafikler, bildirimler ve analiz sonuçları 
şeklinde görüntüleyebileceği bir arayüz geliştirmek için kullanılabilir. 
4. Sektör Görüşü (Uzman Görüşü) 
Akıllı tarım alanında çalışan bir sektör uzmanından alınan bilgilere göre akıllı tarım 
sistemlerinde çevresel verileri toplamak amacıyla çeşitli sensörler kullanılmaktadır. Bunlar 
arasında toprak nem ve sıcaklık sensörleri, EC ve pH sensörleri, iklim sensörleri (hava 
sıcaklığı, nem, yağış miktarı ve rüzgar hızı gibi parametreleri ölçen sensörler) ve NDVI 
sensörleri bulunmaktadır. Son dönemlerde hastalık ve zararlı popülasyonlarını tespit etmek 
amacıyla yapay zeka destekli sensörler de kullanılmaya başlanmıştır. 
Sensörlerden elde edilen veriler genellikle mobil uygulamalar veya bilgisayar sistemleri 
üzerinden çiftçiler ve mühendisler tarafından anlık olarak takip edilmektedir. Bu sistemlerin 
temel amacı iklim değişikliği, kuraklık ve aşırı hava olaylarına karşı verim ve kaliteyi 
korumaktır. Ayrıca su, gübre ve pestisit kullanımını optimize ederek maliyetlerin azaltılması 
ve doğal kaynakların korunması hedeflenmektedir. 
Yapay zekâ tarım sektöründe özellikle hastalık ve zararlı tahmini, sulama optimizasyonu, 
bitki stres analizi, verim tahmini ve hasat sonrası süreçlerde kullanılmaktadır. Bununla birlikte 
akıllı tarım teknolojilerinin yaygınlaşmasının önündeki en önemli zorluklardan biri 
geliştiriciler ile çiftçiler arasındaki teknoloji bilgi farkıdır. Ayrıca arazi koşullarındaki altyapı 
eksiklikleri, enerji sorunları ve donanımın arazi şartlarına uyumu da önemli zorluklar arasında 
yer almaktadır. 
Bu bilgiler akıllı tarım alanında faaliyet gösteren bir şirkette çalışan sektör uzmanı ile yapılan 
görüşmeden elde edilmiştir. 
5. Önerilen Teknoloji Yığını 
Yapılan araştırmalar sonucunda bu proje için aşağıdaki teknoloji yığınının kullanılması 
önerilmektedir: 
 Backend → Python 
 Makine Öğrenmesi → TensorFlow 
 Sensör Veri İletişimi → MQTT 
 Veritabanı → PostgreSQL 
 Web Arayüzü → React 
Bu teknoloji yığını sensör verilerinin toplanması, analiz edilmesi ve kullanıcıya sunulması için 
ölçeklenebilir ve sürdürülebilir bir altyapı sağlayacaktır.

Selahattin-Ali-Kılıç

Teknoloji Seçimi Detaylı Analizi ve Uygulama Planı

Maliyet Analizi: Projede değerlendirilen Python, TensorFlow, MQTT, PostgreSQL ve React teknolojilerinin tamamı açık kaynaklıdır. Bu nedenle lisans maliyeti oluşturmamaktadır. Yazılım tarafında ek lisans gideri gerektirmemesi, proje bütçesi açısından önemli bir avantaj sağlamaktadır. Altyapı maliyeti daha çok sensör, sunucu ve ağ bileşenlerinden oluşacak olsa da teknoloji seçimi açısından düşük maliyetli bir yapı ortaya çıkmaktadır.

Performans Analizi: MQTT, düşük bant genişliği kullanarak sensör verilerinin hızlı ve düşük gecikmeli şekilde iletilmesini sağlamaktadır. Python, backend tarafında veri işleme ve sistem mantığının yürütülmesi için yeterli performans sunmaktadır. TensorFlow, sensör verileri üzerinden tahmin ve analiz işlemlerinin gerçekleştirilmesinde güçlü bir yapı sağlamaktadır. PostgreSQL, verilerin güvenilir biçimde saklanması ve sorgulanması için uygun performansa sahiptir. React ise kullanıcı arayüzünde dinamik veri gösterimi açısından yeterli ve verimli bir çözüm sunmaktadır.

Uyumluluk Analizi: Seçilen teknolojiler birbirleriyle yüksek uyumluluk göstermektedir. Python backend sistemi TensorFlow ile doğrudan entegre çalışabilmektedir. MQTT üzerinden alınan sensör verileri Python tarafından işlenip PostgreSQL veritabanına kaydedilebilmektedir. React arayüzü ise backend tarafından sunulan API servisleri ile iletişim kurarak verileri kullanıcıya aktarabilmektedir. Bu durum sistemin katmanları arasında düzenli ve sürdürülebilir bir entegrasyon sağlamaktadır.

Teknoloji Seçimi: Yapılan maliyet, performans ve uyumluluk analizleri sonucunda proje için en uygun teknoloji yığını; backend için Python, makine öğrenmesi için TensorFlow, sensör veri iletişimi için MQTT, veritabanı için PostgreSQL ve kullanıcı arayüzü için React olarak belirlenmiştir.

Uygulama Planı: Sistem içerisinde sensörlerden elde edilen veriler öncelikle MQTT protokolü ile backend katmanına iletilecektir. Python tabanlı backend yapısı bu verileri alacak, işleyecek ve gerekli doğrulama adımlarından geçirecektir. Ardından veriler PostgreSQL veritabanında saklanacaktır. Biriken veriler TensorFlow kullanılarak analiz edilecek ve sulama önerisi, bitki stres analizi, hastalık riski ve verim tahmini gibi çıktılar üretilecektir. Son aşamada tüm veriler ve analiz sonuçları React tabanlı web arayüzü üzerinden kullanıcıya grafikler, bildirimler ve durum ekranları şeklinde sunulacaktır.



Ömer Akhan:
 Akıllı Tarım Yönetim Sistemi projesinin geliştirme sürecine başlanabilmesi için gerekli olan geliştirme ortamı hazırlanmıştır.

Öncelikle proje gereksinimleri doğrultusunda kullanılacak teknolojiler belirlenmiş ve kurulmuştur. Bu kapsamda Python ve TensorFlow makine öğrenimi geliştirmeleri için, PostgreSQL veritabanı işlemleri için, MQTT veri iletişimi için ve React ile Node.js web arayüzü geliştirme süreci için kurulmuştur.

Kurulumların ardından proje için temel klasör yapısı oluşturulmuş, backend ve frontend bileşenleri ayrıştırılmış ve gerekli bağımlılıklar yüklenmiştir. Ayrıca proje yapılandırmaları tamamlanarak sistem çalışmaya hazır hale getirilmiştir.

Versiyon kontrolü için Git kullanılarak proje deposu başlatılmış, .gitignore dosyası oluşturulmuş ve ilk commit işlemi gerçekleştirilmiştir.

Sonuç olarak, projenin geliştirilmesine başlanabilecek şekilde tüm teknik altyapı eksiksiz olarak hazırlanmıştır.## 📝 Yapılan Çalışmalar (Ortam Kurulumu)

Bu görev kapsamında, Akıllı Tarım Yönetim Sistemi projesinin geliştirme sürecine başlanabilmesi için gerekli olan geliştirme ortamı hazırlanmıştır.

Öncelikle proje gereksinimleri doğrultusunda kullanılacak teknolojiler belirlenmiş ve kurulmuştur. Bu kapsamda Python ve TensorFlow makine öğrenimi geliştirmeleri için, PostgreSQL veritabanı işlemleri için, MQTT veri iletişimi için ve React ile Node.js web arayüzü geliştirme süreci için kurulmuştur.

Kurulumların ardından proje için temel klasör yapısı oluşturulmuş, backend ve frontend bileşenleri ayrıştırılmış ve gerekli bağımlılıklar yüklenmiştir. Ayrıca proje yapılandırmaları tamamlanarak sistem çalışmaya hazır hale getirilmiştir.

Versiyon kontrolü için Git kullanılarak proje deposu başlatılmış, .gitignore dosyası oluşturulmuş ve ilk commit işlemi gerçekleştirilmiştir.

Sonuç olarak, projenin geliştirilmesine başlanabilecek şekilde tüm teknik altyapı eksiksiz olarak hazırlanmıştır.
 

