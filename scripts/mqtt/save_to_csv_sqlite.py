import csv
import json
import sqlite3
from pathlib import Path
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
CSV_PATH = Path("data/raw/mqtt_room01_combined.csv")
DB_PATH = Path("data/raw/iot_sensor_combined.db")
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
if not CSV_PATH.exists():
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "device_id", "temperature_c", "humidity_pct",
            "co2_ppm", "power_watt", "timestamp"
        ])
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS room_telemetry (
id INTEGER PRIMARY KEY AUTOINCREMENT,
device_id TEXT,
temperature_c REAL,
humidity_pct REAL,
co2_ppm INTEGER,
power_watt REAL,
timestamp TEXT
)
""")
conn.commit()
def on_connect(client, userdata, flags, reason_code, properties=None):
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
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        cursor.execute("""
INSERT INTO room_telemetry (
device_id, temperature_c, humidity_pct, co2_ppm,
power_watt, timestamp
) VALUES (?, ?, ?, ?, ?, ?)
""", tuple(row))
        conn.commit()
        print(f"Disimpan ke CSV dan SQLite: {row}")
    except Exception as exc:
        print(f"Error: {exc}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, 60)
try:
    client.loop_forever()
finally:
    conn.close()
