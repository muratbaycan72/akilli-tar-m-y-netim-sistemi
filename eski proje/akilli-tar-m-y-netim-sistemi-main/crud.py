import psycopg2
import psycopg2.extras
from datetime import datetime

# =========================================================
# Veritabanı Bağlantı Ayarları
# =========================================================
# Veritabanı ile etkileşim kurmak için gerekli yapılandırmaları içerir.
# Kendi local veya uzak sunucu bilgilerinize göre bu sözlüğü güncellemeyi unutmayın.
DB_CONFIG = {
    'dbname': 'akillitarim',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# ---------------------------------------------------------
# ÇİFTÇİLER (Ciftciler) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_ciftci(conn, ad, soyad, telefon, email, adres):
    """
    Veritabanına yeni bir çiftçi kaydı ekler. (CREATE)
    """
    try:
        # RealDictCursor ile verileri dizi yerine (dict) anahtar-değer sözlükleri olarak alırız.
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # SQL Injection tehlikesinden korunmak için %s ile parametreli sorgu kullanıyoruz.
            sql = """
                INSERT INTO Ciftciler (Ad, Soyad, Telefon, Email, Adres)
                VALUES (%s, %s, %s, %s, %s) RETURNING Ciftci_ID;
            """
            cur.execute(sql, (ad, soyad, telefon, email, adres))
            # RETURNING ifadesi sayesinde eklenen verinin otomatik oluşturulan ID'sini yakalarız.
            ciftci_id = cur.fetchone()['ciftci_id']
            conn.commit() # Değişikliği kalıcı olarak veritabanına işliyoruz.
            return ciftci_id
    except Exception as e:
        print(f"Hata (create_ciftci): {e}")
        conn.rollback() # İşlem esnasında hata çıkarsa (Örn: unique email hatası) rollback ile geri al.
        return None

def read_ciftciler(conn, ciftci_id=None):
    """
    Veritabanından çiftçi verilerini getirir. (READ)
    ciftci_id parametresi verilirse sadece o kişiyi, verilmezse tüm tabloyu döndürür.
    """
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if ciftci_id:
                cur.execute("SELECT * FROM Ciftciler WHERE Ciftci_ID = %s;", (ciftci_id,))
                return cur.fetchone() # Tek satır
            else:
                cur.execute("SELECT * FROM Ciftciler;")
                return cur.fetchall() # Tüm satırlar (liste içerisinde dict olarak)
    except Exception as e:
        print(f"Hata (read_ciftciler): {e}")
        return None

def update_ciftci(conn, ciftci_id, data):
    """
    Çiftçi tablosundaki belirli bir kaydı tamamen veya kısmen günceller. (UPDATE)
    data: Sadece değişecek alanları içeren python sözlüğü. (Örn: {"Adres": "Ankara"})
    """
    if not data:
        return False
    # Gelen dict'deki key'leri kullanarak dinamik olarak 'Ad = %s, Soyad = %s' metnini oluşturur.
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(ciftci_id) # WHERE şartı son parametre olmalı.
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Ciftciler SET {set_clause} WHERE Ciftci_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0 # Etkilenen satır 0'dan büyükse True döner
    except Exception as e:
        print(f"Hata (update_ciftci): {e}")
        conn.rollback()
        return False

def delete_ciftci(conn, ciftci_id):
    """
    Çiftçiyi ID üzerinden veritabanından siler. (DELETE)
    Not: Bu işlem veritabanı şemasında CASCADE ayarlı olduğu için bağlı tablolarını da etkileyebilir.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Ciftciler WHERE Ciftci_ID = %s;", (ciftci_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_ciftci): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# TARLALAR (Tarlalar) CRUD İŞLEMLERİ
# ---------------------------------------------------------
# Diğer tablolar da çiftçiler tablosuyla aynı yapıda CRUD operasyonlarını içerir.

def create_tarla(conn, ciftci_id, konum, alan, urun_turu):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Tarlalar (Ciftci_ID, Konum, Alan, Urun_Turu)
                VALUES (%s, %s, %s, %s) RETURNING Tarla_ID;
            """
            cur.execute(sql, (ciftci_id, konum, alan, urun_turu))
            tarla_id = cur.fetchone()['tarla_id']
            conn.commit()
            return tarla_id
    except Exception as e:
        print(f"Hata (create_tarla): {e}")
        conn.rollback()
        return None
        
def read_tarlalar(conn, tarla_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if tarla_id:
                cur.execute("SELECT * FROM Tarlalar WHERE Tarla_ID = %s;", (tarla_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Tarlalar;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_tarlalar): {e}")
        return None

def update_tarla(conn, tarla_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(tarla_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Tarlalar SET {set_clause} WHERE Tarla_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_tarla): {e}")
        conn.rollback()
        return False

def delete_tarla(conn, tarla_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Tarlalar WHERE Tarla_ID = %s;", (tarla_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_tarla): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# ÜRÜNLER (Urunler) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_urun(conn, tarla_id, urun_adi, ekim_tarihi, hasat_tarihi, miktar):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Urunler (Tarla_ID, Urun_Adi, Ekim_Tarihi, Hasat_Tarihi, Miktar)
                VALUES (%s, %s, %s, %s, %s) RETURNING Urun_ID;
            """
            cur.execute(sql, (tarla_id, urun_adi, ekim_tarihi, hasat_tarihi, miktar))
            urun_id = cur.fetchone()['urun_id']
            conn.commit()
            return urun_id
    except Exception as e:
        print(f"Hata (create_urun): {e}")
        conn.rollback()
        return None

def read_urunler(conn, urun_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if urun_id:
                cur.execute("SELECT * FROM Urunler WHERE Urun_ID = %s;", (urun_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Urunler;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_urunler): {e}")
        return None

def update_urun(conn, urun_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(urun_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Urunler SET {set_clause} WHERE Urun_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_urun): {e}")
        conn.rollback()
        return False

def delete_urun(conn, urun_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Urunler WHERE Urun_ID = %s;", (urun_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_urun): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# SENSÖRLER (Sensorler) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_sensor(conn, tarla_id, sensor_turu, kurulum_tarihi, durum='Aktif'):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Sensorler (Tarla_ID, Sensor_Turu, Kurulum_Tarihi, Durum)
                VALUES (%s, %s, %s, %s) RETURNING Sensor_ID;
            """
            cur.execute(sql, (tarla_id, sensor_turu, kurulum_tarihi, durum))
            sensor_id = cur.fetchone()['sensor_id']
            conn.commit()
            return sensor_id
    except Exception as e:
        print(f"Hata (create_sensor): {e}")
        conn.rollback()
        return None

def read_sensorler(conn, sensor_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if sensor_id:
                cur.execute("SELECT * FROM Sensorler WHERE Sensor_ID = %s;", (sensor_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Sensorler;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_sensorler): {e}")
        return None

def update_sensor(conn, sensor_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(sensor_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Sensorler SET {set_clause} WHERE Sensor_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_sensor): {e}")
        conn.rollback()
        return False

def delete_sensor(conn, sensor_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Sensorler WHERE Sensor_ID = %s;", (sensor_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_sensor): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# ÖLÇÜMLER (Olcumler) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_olcum(conn, sensor_id, tarih, deger):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Olcumler (Sensor_ID, Tarih, Deger)
                VALUES (%s, %s, %s) RETURNING Olcum_ID;
            """
            cur.execute(sql, (sensor_id, tarih, deger))
            olcum_id = cur.fetchone()['olcum_id']
            conn.commit()
            return olcum_id
    except Exception as e:
        print(f"Hata (create_olcum): {e}")
        conn.rollback()
        return None

def read_olcumler(conn, olcum_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if olcum_id:
                cur.execute("SELECT * FROM Olcumler WHERE Olcum_ID = %s;", (olcum_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Olcumler;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_olcumler): {e}")
        return None

def update_olcum(conn, olcum_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(olcum_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Olcumler SET {set_clause} WHERE Olcum_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_olcum): {e}")
        conn.rollback()
        return False

def delete_olcum(conn, olcum_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Olcumler WHERE Olcum_ID = %s;", (olcum_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_olcum): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# SULAMA (Sulama) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_sulama(conn, tarla_id, tarih, sure, su_miktari):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Sulama (Tarla_ID, Tarih, Sure, Su_Miktari)
                VALUES (%s, %s, %s, %s) RETURNING Sulama_ID;
            """
            cur.execute(sql, (tarla_id, tarih, sure, su_miktari))
            sulama_id = cur.fetchone()['sulama_id']
            conn.commit()
            return sulama_id
    except Exception as e:
        print(f"Hata (create_sulama): {e}")
        conn.rollback()
        return None

def read_sulamalar(conn, sulama_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if sulama_id:
                cur.execute("SELECT * FROM Sulama WHERE Sulama_ID = %s;", (sulama_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Sulama;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_sulamalar): {e}")
        return None

def update_sulama(conn, sulama_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(sulama_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Sulama SET {set_clause} WHERE Sulama_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_sulama): {e}")
        conn.rollback()
        return False

def delete_sulama(conn, sulama_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Sulama WHERE Sulama_ID = %s;", (sulama_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_sulama): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# GUBRELEME (Gubreleme) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_gubreleme(conn, tarla_id, tarih, gubre_turu, miktar):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Gubreleme (Tarla_ID, Tarih, Gubre_Turu, Miktar)
                VALUES (%s, %s, %s, %s) RETURNING Gubreleme_ID;
            """
            cur.execute(sql, (tarla_id, tarih, gubre_turu, miktar))
            gubreleme_id = cur.fetchone()['gubreleme_id']
            conn.commit()
            return gubreleme_id
    except Exception as e:
        print(f"Hata (create_gubreleme): {e}")
        conn.rollback()
        return None

def read_gubrelemeler(conn, gubreleme_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if gubreleme_id:
                cur.execute("SELECT * FROM Gubreleme WHERE Gubreleme_ID = %s;", (gubreleme_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Gubreleme;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_gubrelemeler): {e}")
        return None

def update_gubreleme(conn, gubreleme_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(gubreleme_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Gubreleme SET {set_clause} WHERE Gubreleme_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_gubreleme): {e}")
        conn.rollback()
        return False

def delete_gubreleme(conn, gubreleme_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Gubreleme WHERE Gubreleme_ID = %s;", (gubreleme_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_gubreleme): {e}")
        conn.rollback()
        return False

# ---------------------------------------------------------
# KULLANICILAR (Kullanicilar) CRUD İŞLEMLERİ
# ---------------------------------------------------------

def create_kullanici(conn, ad, soyad, rol, email, sifre_hash):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
                INSERT INTO Kullanicilar (Ad, Soyad, Rol, Email, Sifre_Hash)
                VALUES (%s, %s, %s, %s, %s) RETURNING Kullanici_ID;
            """
            cur.execute(sql, (ad, soyad, rol, email, sifre_hash))
            kullanici_id = cur.fetchone()['kullanici_id']
            conn.commit()
            return kullanici_id
    except Exception as e:
        print(f"Hata (create_kullanici): {e}")
        conn.rollback()
        return None

def read_kullanicilar(conn, kullanici_id=None):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if kullanici_id:
                cur.execute("SELECT * FROM Kullanicilar WHERE Kullanici_ID = %s;", (kullanici_id,))
                return cur.fetchone()
            else:
                cur.execute("SELECT * FROM Kullanicilar;")
                return cur.fetchall()
    except Exception as e:
        print(f"Hata (read_kullanicilar): {e}")
        return None

def update_kullanici(conn, kullanici_id, data):
    if not data:
        return False
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values())
    values.append(kullanici_id)
    try:
        with conn.cursor() as cur:
            sql = f"UPDATE Kullanicilar SET {set_clause} WHERE Kullanici_ID = %s;"
            cur.execute(sql, tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (update_kullanici): {e}")
        conn.rollback()
        return False

def delete_kullanici(conn, kullanici_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Kullanicilar WHERE Kullanici_ID = %s;", (kullanici_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Hata (delete_kullanici): {e}")
        conn.rollback()
        return False


# ---------------------------------------------------------
# TEST BLOĞU
# ---------------------------------------------------------
if __name__ == "__main__":
    print(f"{'='*50}\nCRUD Operasyonları Testi Başlatılıyor...\n{'='*50}")
    try:
        # Veritabanına bağlantı deneniyor
        print("Adım 1: Veritabanına bağlanılıyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Bağlantı başarılı.\n")
        
        # 1. Kullanıcı Oluşturma (CREATE)
        print("Adım 2: Örnek bir kullanıcı 'Kullanicilar' tablosuna ekleniyor...")
        k_id = create_kullanici(conn, "Omer", "Akhan", "Admin", "testomer@akillitarim.com", "hash_abc123")
        
        if k_id:
            print(f"✓ Kullanıcı başarıyla oluşturuldu, ID atandı: {k_id}\n")
            
            # 2. Kullanıcıyı Okuma (READ)
            print("Adım 3: Eklenen kullanıcı bilgisi veritabanından getiriliyor...")
            kullanici = read_kullanicilar(conn, k_id)
            print(f"  > Okunan Kayıt: {kullanici}\n")
            
            # 3. Kullanıcıyı Güncelleme (UPDATE)
            print("Adım 4: Kullanıcının Rol ve Ad bilgisi güncelleniyor...")
            update_basarili = update_kullanici(conn, k_id, {"Rol": "Süper Admin", "Ad": "Ömer Faruk"})
            if update_basarili:
                print(f"✓ Kullanıcı başarıyla güncellendi.")
                print(f"  > Yeni Kayıt: {read_kullanicilar(conn, k_id)}\n")
            
            # 4. Kullanıcıyı Silme (DELETE)
            print("Adım 5: İşlem tamamlandı, test kayıdı siliniyor...")
            silme_basarili = delete_kullanici(conn, k_id)
            if silme_basarili:
                print(f"✓ Kullanıcı veritabanından kalıcı olarak silindi.\n")
                
        # İşlem sonu bağlantıyı kapatıyoruz.
        conn.close()
        print(f"{'='*50}\nTüm testler başarıyla tamamlandı ve bağlantı kapatıldı.\n{'='*50}")
        
    except psycopg2.OperationalError as e:
        print(f"HATA: Veritabanına bağlanılamadı. \n->Lütfen PostgreSQL servisinizin açık olduğundan ve DB_CONFIG değişkenindeki bilgilerin (şifre, port vb.) doğruluğundan emin olun.")
    except psycopg2.errors.UndefinedTable:
         print(f"HATA: Tablolar bulunamadı.\n-> Lütfen önce PostgreSQL içerisinde 'schema.sql' dosyasını çalıştırarak tabloların oluşturulduğundan emin olun.")
    except Exception as e:
        print(f"Beklenmeyen Hata Oluştu: {e}")
