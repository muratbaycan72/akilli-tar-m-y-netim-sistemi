import time
import paho.mqtt.client as mqtt

# HiveMQ Ekranındaki URL'niz
CLUSTER_URL = "f9bcfd1d23fd4e1aaa45dbfc61b3c18d.s1.eu.hivemq.cloud"
# Access Management sekmesinde oluşturduğunuz bilgiler
USER = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Başarıyla HiveMQ Bulut Broker'a bağlandık!")
        # Test için bir konuya abone olalım
        client.subscribe("tarim/sensor/test")
    else:
        print(f"❌ Bağlantı hatası! Hata kodu: {rc}")

def on_message(client, userdata, msg):
    print(f"📩 Mesaj Geldi -> Konu: {msg.topic} | Veri: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Güvenlik Ayarları (HiveMQ Cloud TLS gerektirir)
client.username_pw_set(USER, PASSWORD)
client.tls_set() 

print("Bağlanılıyor...")
client.connect(CLUSTER_URL, 8883)

client.loop_start()

# 5 saniye sonra bir test verisi gönderelim
time.sleep(2)
print("🚀 Test verisi gönderiliyor...")
client.publish("tarim/sensor/test", '{"nem": 45, "sicaklik": 22}')

# Verinin geri gelmesini beklemek için programı açık tutalım
time.sleep(10)
client.loop_stop().  
