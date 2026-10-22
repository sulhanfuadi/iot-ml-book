"""
Hands-on 13: Ekspor Dataset ke MQTT Simulator (Publisher dari CSV)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Membaca data/synthetic/room_classification_dataset.csv dan mempublikasikan
setiap baris sebagai payload JSON ke topik iotlab/room01/telemetry.
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
TOPIC = "iotlab/room01/telemetry"
CLIENT_ID = "csv-publisher-room01"
DATA_PATH = Path("data/synthetic/room_classification_dataset.csv")
PUBLISH_INTERVAL_SECONDS = 0.5  # percepat simulasi


def create_mqtt_client(client_id):
  try:
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
  except AttributeError:
    return mqtt.Client(client_id=client_id)


def main():
  parser = argparse.ArgumentParser(description="Publish CSV ke MQTT (Hands-on 13)")
  parser.add_argument("--broker", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  parser.add_argument("--topic", default=TOPIC)
  parser.add_argument(
      "--limit", type=int, default=0,
      help="Batasi jumlah baris yang dikirim (0 = semua)",
  )
  parser.add_argument(
      "--interval", type=float, default=PUBLISH_INTERVAL_SECONDS,
      help="Interval antar pesan dalam detik",
  )
  args = parser.parse_args()

  df = pd.read_csv(DATA_PATH)
  if args.limit > 0:
    df = df.head(args.limit)

  client = create_mqtt_client(CLIENT_ID)
  try:
    client.connect(args.broker, args.port, keepalive=60)
  except Exception as e:
    print(f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}")
    sys.exit(1)

  print(f"[INFO] Mengirim data dari {DATA_PATH} ke topic {args.topic}")
  client.loop_start()

  sent = 0
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
    result = client.publish(args.topic, payload_json, qos=1)
    if result.rc == 0:
      print(f"[PUBLISH] {payload_json}")
      sent += 1
    else:
      print(f"[GAGAL] {payload_json}")
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SELESAI] {sent} pesan terkirim ke {args.topic}.")


if __name__ == "__main__":
  main()
