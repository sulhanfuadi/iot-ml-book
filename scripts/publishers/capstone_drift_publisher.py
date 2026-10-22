import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER = "localhost"
TOPIC = "capstone/iotnode01/telemetry"
client = mqtt.Client(client_id="capstone-drift-publisher")
client.connect(BROKER, 1883, 60)
base_temp = 26.0
base_power = 130.0
for i in range(500):
    # drift perlahan
    temp = base_temp + (i * 0.01) + random.uniform(-0.5, 0.5)
    power = base_power + (i * 0.08) + random.uniform(-10, 10)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "iotnode01",
        "temperature_c": round(temp, 2),
        "humidity_pct": round(random.uniform(45.0, 65.0), 2),
        "power_watt": round(power, 2),
        "current_amp": round(random.uniform(4.0, 7.5), 2)
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published drift payload:", payload)
    time.sleep(0.1)
