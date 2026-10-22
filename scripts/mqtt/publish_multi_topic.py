"""
Hands-on 13: Versi Publish Multi-Topic (alert untuk warning/fault)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Semua baris dikirim ke iotlab/room01/telemetry; baris berlabel
warning/fault juga dikirim ke iotlab/room01/alert.
"""

import argparse
import json
from pathlib import Path
import sys
import time

import pandas as pd
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
DATA_PATH = Path("data/synthetic/room_classification_dataset.csv")
TELEMETRY_TOPIC = "iotlab/room01/telemetry"
ALERT_TOPIC = "iotlab/room01/alert"


def create_mqtt_client(client_id):
  try:
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
  except AttributeError:
    return mqtt.Client(client_id=client_id)


def main():
  parser = argparse.ArgumentParser(description="Publish multi-topic (Hands-on 13)")
  parser.add_argument("--broker", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  parser.add_argument("--limit", type=int, default=0)
  parser.add_argument("--interval", type=float, default=0.2)
  args = parser.parse_args()

  df = pd.read_csv(DATA_PATH)
  if args.limit > 0:
    df = df.head(args.limit)

  client = create_mqtt_client("multi-topic-publisher")
  try:
    client.connect(args.broker, args.port, keepalive=60)
  except Exception as e:
    print(f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}")
    sys.exit(1)

  client.loop_start()
  sent_telemetry = 0
  sent_alert = 0

  for _, row in df.iterrows():
    payload = {
        "timestamp": str(row["timestamp"]),
        "device_id": row["device_id"],
        "temperature_c": float(row["temperature_c"]),
        "humidity_pct": float(row["humidity_pct"]),
        "co2_ppm": int(row["co2_ppm"]),
        "power_watt": float(row["power_watt"]),
        "status_label": row["status_label"],
        "is_anomaly": int(row["is_anomaly"]),
    }
    payload_json = json.dumps(payload)

    client.publish(TELEMETRY_TOPIC, payload_json, qos=1)
    sent_telemetry += 1

    if row["status_label"] in ("warning", "fault"):
      client.publish(ALERT_TOPIC, payload_json, qos=1)
      sent_alert += 1
      print(f"[ALERT] {row['status_label']} -> {ALERT_TOPIC}")

    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(
      f"[SELESAI] {sent_telemetry} pesan ke {TELEMETRY_TOPIC}, "
      f"{sent_alert} pesan ke {ALERT_TOPIC}."
  )


if __name__ == "__main__":
  main()
