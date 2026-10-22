import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER = "localhost"
TOPIC = "capstone/iotnode01/telemetry"
client = mqtt.Client(client_id="capstone-bad-publisher")
client.connect(BROKER, 1883, 60)
samples = [
    {"timestamp": datetime.now().isoformat(timespec="seconds"), "device_id": "iotnode01"},
    {"timestamp": "bad_time", "device_id": "iotnode01", "temperature_c": "abc", "humidity_pct": 50, "power_watt": 100, "current_amp": 5},
    {"timestamp": datetime.now().isoformat(timespec="seconds"), "device_id": "iotnode01", "temperature_c": -99, "humidity_pct": 999, "power_watt": 10000, "current_amp": -3},
]
for payload in samples:
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published bad payload:", payload)
    time.sleep(1)
