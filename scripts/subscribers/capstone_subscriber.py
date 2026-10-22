"""
Hands-on 38 (Bab 15): Capstone Subscriber - Validasi, Inferensi, Storage
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Menerima telemetry, memvalidasi payload, menjalankan threshold baseline
(power > 280 W atau arus > 10 A) dan Isolation Forest, lalu menyimpan hasil.

Storage default: CSV lokal (outputs/reports/capstone_monitoring.csv).
Storage InfluxDB + Grafana sesuai buku: aktifkan dengan --influx.
"""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "capstone/iotnode01/telemetry"

MODEL_PATH = Path("outputs/models/capstone_iforest.joblib")
CSV_PATH = Path("outputs/reports/capstone_monitoring.csv")

INFLUX_URL = "http://localhost:8086"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"

FEATURE_COLS = ["temperature_c", "humidity_pct", "power_watt", "current_amp"]

records = []


def validate_payload(payload):
  required = ["timestamp", "device_id", "temperature_c",
              "humidity_pct", "power_watt", "current_amp"]
  for field in required:
    if field not in payload:
      raise ValueError(f"Field hilang: {field}")
  # validasi ringan
  float(payload["temperature_c"])
  float(payload["humidity_pct"])
  float(payload["power_watt"])
  float(payload["current_amp"])


def build_features(payload):
  row = pd.DataFrame([{
      "temperature_c": float(payload["temperature_c"]),
      "humidity_pct": float(payload["humidity_pct"]),
      "power_watt": float(payload["power_watt"]),
      "current_amp": float(payload["current_amp"]),
  }])
  return row


def main():
  parser = argparse.ArgumentParser(description="Capstone subscriber")
  parser.add_argument("--max-messages", type=int, default=10)
  parser.add_argument("--timeout", type=int, default=60)
  parser.add_argument("--influx", action="store_true")
  parser.add_argument("--influx-token", default="GANTI_DENGAN_TOKEN_ANDA")
  args = parser.parse_args()

  model = joblib.load(MODEL_PATH)
  CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

  write_api = None
  if args.influx:
    from influxdb_client import InfluxDBClient
    from influxdb_client.client.write_api import SYNCHRONOUS
    influx_client = InfluxDBClient(url=INFLUX_URL, token=args.influx_token, org=INFLUX_ORG)
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

  state = {"count": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Connected to broker.")
    client.subscribe(TOPIC, qos=1)
    print("[INFO] Subscribed to", TOPIC)

  def on_message(client, userdata, msg):
    try:
      payload = json.loads(msg.payload.decode("utf-8"))
      validate_payload(payload)
      X = build_features(payload)

      # threshold baseline
      threshold_alert = int(
          X["power_watt"].iloc[0] > 280 or X["current_amp"].iloc[0] > 10.0
      )

      # Isolation Forest
      pred = model.predict(X[FEATURE_COLS])[0]  # 1 normal, -1 anomaly
      anomaly_flag = 1 if pred == -1 else 0

      print(
          f"[{payload['timestamp']}] "
          f"T={payload['temperature_c']} "
          f"H={payload['humidity_pct']} "
          f"P={payload['power_watt']} "
          f"I={payload['current_amp']} "
          f"-> anomaly={anomaly_flag}, threshold={threshold_alert}"
      )

      if write_api is not None:
        from influxdb_client import Point, WritePrecision
        point = (
            Point("capstone_device_monitoring")
            .tag("device_id", payload["device_id"])
            .field("temperature_c", float(payload["temperature_c"]))
            .field("humidity_pct", float(payload["humidity_pct"]))
            .field("power_watt", float(payload["power_watt"]))
            .field("current_amp", float(payload["current_amp"]))
            .field("iforest_anomaly", anomaly_flag)
            .field("threshold_alert", threshold_alert)
            .time(payload["timestamp"], WritePrecision.S)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
      else:
        records.append({
            **payload,
            "iforest_anomaly": anomaly_flag,
            "threshold_alert": threshold_alert,
        })

      state["count"] += 1
      if args.max_messages and state["count"] >= args.max_messages:
        client.disconnect()
    except Exception as exc:
      print("[ERROR]", exc)

  client = mqtt.Client(client_id="capstone-subscriber")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(BROKER, PORT, 60)
  client.loop_start()

  import time
  start = time.time()
  while time.time() - start < args.timeout:
    if args.max_messages and state["count"] >= args.max_messages:
      break
    time.sleep(0.2)

  client.loop_stop()
  client.disconnect()

  if write_api is None and records:
    pd.DataFrame(records).to_csv(CSV_PATH, index=False)
    print(f"[SUKSES] {len(records)} hasil disimpan ke {CSV_PATH}")


if __name__ == "__main__":
  main()
