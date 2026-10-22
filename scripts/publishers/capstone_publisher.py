import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER = "localhost"
PORT = 1883
TOPIC = "capstone/iotnode01/telemetry"
client = mqtt.Client(client_id="capstone-publisher")
client.connect(BROKER, PORT, 60)
while True:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "iotnode01",
        "temperature_c": round(random.uniform(24.0, 34.0), 2),
        "humidity_pct": round(random.uniform(40.0, 75.0), 2),
        "power_watt": round(random.uniform(80.0, 260.0), 2),
        "current_amp": round(random.uniform(3.5, 9.5), 2)
    }
    # injeksi anomali kecil sesekali
    if random.random() < 0.08:
        payload["power_watt"] += random.uniform(80, 180)
        payload["current_amp"] += random.uniform(2, 5)
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published:", payload)
    time.sleep(2)
