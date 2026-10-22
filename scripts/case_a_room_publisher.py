import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER = "localhost"
TOPIC = "casea/room01/telemetry"
client = mqtt.Client(client_id="casea-room-pub")
client.connect(BROKER, 1883, 60)
while True:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "room01",
        "temperature_c": round(random.uniform(23.0, 33.0), 2),
        "humidity_pct": round(random.uniform(40.0, 72.0), 2),
        "co2_ppm": random.randint(450, 1500)
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published:", payload)
    time.sleep(2)
