import paho.mqtt.client as mqtt
import time
import json
import random

# HiveMQ Bilgilerin (Buraları kendi bilgilerinle doldur)
URL = "f9bcfd1d23fd4e1aaa45dbfc61b3c18d.s1.eu.hivemq.cloud"
USER = "KULLANICI_ADIN"
PW = "SIFREN"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USER, PW)
client.tls_set()
client.connect(URL, 8883)

while True:
    data = {"toprak_nem": random.randint(30, 60), "sicaklik": 25}
    client.publish("tarim/sensor", json.dumps(data))
    print(f"Veri gönderildi: {data}")
    time.sleep(5)
