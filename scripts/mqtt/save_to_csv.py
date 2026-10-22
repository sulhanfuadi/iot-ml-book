import csv
import json
from pathlib import Path
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
OUTPUT_FILE = Path("data/raw/mqtt_room01.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
HEADER = [
    "device_id",
    "temperature_c",
    "humidity_pct",
    "co2_ppm",
    "power_watt",
    "timestamp"
]
if not OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Terhubung ke broker.")
    client.subscribe(TOPIC, qos=1)
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        row = [
            data.get("device_id"),
            data.get("temperature_c"),
            data.get("humidity_pct"),
            data.get("co2_ppm"),
            data.get("power_watt"),
            data.get("timestamp"),
        ]
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print(f"Data disimpan ke CSV: {row}")
    except Exception as exc:
        print(f"Gagal menyimpan ke CSV: {exc}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_forever()
