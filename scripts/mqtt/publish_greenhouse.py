import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/greenhouse/zone1/telemetry"
CLIENT_ID = "publisher-greenhouse-zone1"
client = mqtt.Client(client_id=CLIENT_ID)
def generate_data():
    return {
        "device_id": "greenhouse-zone1",
        "air_temp_c": round(random.uniform(25.0, 35.0), 2),
        "soil_moisture_pct": round(random.uniform(30.0, 80.0), 2),
        "light_lux": random.randint(8000, 30000),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
while True:
    payload = generate_data()
    payload_json = json.dumps(payload)
    client.publish(TOPIC, payload_json, qos=1)
    print(f"[GREENHOUSE] {payload_json}")
    time.sleep(10)
