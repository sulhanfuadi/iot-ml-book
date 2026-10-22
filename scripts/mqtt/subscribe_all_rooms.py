import json
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/+/telemetry"
CLIENT_ID = "subscriber-all-lab1"
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Terhubung ke broker.")
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribe wildcard ke: {TOPIC}")
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"[{msg.topic}] {data}")
    except Exception as exc:
        print(f"Gagal memproses pesan: {exc}")
client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_forever()
