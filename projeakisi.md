# Akıllı Tarım Yönetim Sistemi - Proje Akışı ve Haftalık İlerleme

Bu dosya, Algoritma Alimleri takımının haftalık proje ilerlemesini ve üyelerin görev dağılımlarını içermektedir.

## 1. Hafta (7-12 Mart)
Murat Baycan (Scrum Master / Yönetici): GitHub reposu oluşturuldu, Trello ve Discord iletişim kanalları kuruldu. Proje akış dokümanı eklendi.
Selahattin Ali Kılıç : Teknoloji araştırması ve seçimi üzerinde çalışıyor.
Ömer Akhan: Geliştirme ortamı kurulumu üzerinde çalışıyor.
Binnur Aslan: Proje analizi ve kapsam tanımı üzerinde çalışıyor.
Ülkü Tuana Kara: Gereksinim toplama ve belgeleme üzerinde çalışıyor. 

 
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
=======
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
 main

Binnur Aslan:

[UI/UX Wireframe Tasarımı](./uiuxwireframetasarimi.pdf)
