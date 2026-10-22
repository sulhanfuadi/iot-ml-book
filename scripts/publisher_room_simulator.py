import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"
client = mqtt.Client(client_id="publisher-room-sim")
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
while True:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "room01",
        "temperature_c": round(random.uniform(24.0, 33.5), 2),
        "humidity_pct": round(random.uniform(40.0, 70.0), 2),
        "co2_ppm": random.randint(450, 1500),
        "power_watt": round(random.uniform(90.0, 300.0), 2)
    }
    payload_json = json.dumps(payload)
    result = client.publish(TOPIC, payload_json, qos=1)
    if result.rc == 0:
        print("Published:", payload_json)
    else:
        print("Publish gagal.")
    time.sleep(2)
