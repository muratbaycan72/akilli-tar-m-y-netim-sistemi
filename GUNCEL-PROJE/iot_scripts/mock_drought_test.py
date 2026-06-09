import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

# MQTT Broker Ayarları (Docker Compose kullanıyorsan genelde localhost ve 1883 portudur)
BROKER = "localhost" 
PORT = 1883
TOPIC = "tarim/sensor/tarla_1"

# MQTT İstemcisini Başlat
# paho-mqtt 2.0+ sürümü için callback sürümünü belirtiyoruz
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Mock_Drought_Publisher")

try:
    client.connect(BROKER, PORT, 60)
    print("🌱 Broker'a bağlanıldı. Test başlatılıyor...\n")
except Exception as e:
    print(f"Bağlantı hatası: {e}")
    exit()

try:
    for i in range(1, 6):
        # İlk 3 adım: Toprak nemi %60-%70 arası (Normal)
        if i <= 3:
            soil_moisture = round(random.uniform(60.0, 70.0), 2)
            status_msg = "🟢 NORMAL"
        # Son 2 adım: Toprak nemi %10-%15 arası (Kuraklık / Alarm)
        else:
            soil_moisture = round(random.uniform(10.0, 15.0), 2)
            status_msg = "🔴 KURAKLIK DÜŞÜŞÜ"

        # Sensör Veri Paketi (Payload)
        payload = {
            "sensor_id": "sensor_zemin_01",
            "soil_moisture": soil_moisture,
            "temperature": round(random.uniform(28.0, 32.0), 2), # Sıcaklık yüksek
            "air_humidity": round(random.uniform(30.0, 40.0), 2),
            "timestamp": datetime.now().isoformat()
        }

        # Veriyi JSON formatına çevir ve MQTT üzerinden yayınla (publish)
        client.publish(TOPIC, json.dumps(payload))
        print(f"{status_msg} -> Yayınlandı: {payload}")
        
        time.sleep(3) # Veri akışını net görmek için 3 saniye bekle

except KeyboardInterrupt:
    print("\nTest manuel olarak durduruldu.")

client.disconnect()
print("\n✅ Kuraklık testi tamamlandı.")