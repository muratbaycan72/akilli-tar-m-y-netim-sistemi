import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"Yeni Veri Alındı: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
# Bağlantı ayarları yukardakiyle aynı olacak...
client.connect(URL, 8883)
client.subscribe("tarim/sensor")
client.loop_forever()
