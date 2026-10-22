"""
Hands-on 35 (Studi Kasus A): Subscriber + Klasifikasi Kenyamanan
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Storage default: CSV lokal (outputs/reports/case_a_room_predictions.csv).
Storage InfluxDB + dashboard Grafana sesuai buku: aktifkan dengan --influx.
"""

import argparse
import json
from collections import deque
from pathlib import Path

import joblib
import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "casea/room01/telemetry"
MODEL_PATH = Path("models/case_a_room_rf.joblib")
CSV_PATH = Path("outputs/reports/case_a_room_predictions.csv")

INFLUX_URL = "http://localhost:8086"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"

temp_buffer = deque(maxlen=3)
co2_buffer = deque(maxlen=3)
records = []


def safe_mean(values):
  return sum(values) / len(values) if len(values) > 0 else None


def valid_payload(payload):
  try:
    return (
        10.0 <= float(payload["temperature_c"]) <= 45.0
        and 0.0 <= float(payload["humidity_pct"]) <= 100.0
        and float(payload["co2_ppm"]) > 0
    )
  except (KeyError, TypeError, ValueError):
    return False


def build_features(payload):
  ts = pd.to_datetime(payload["timestamp"])
  temp = float(payload["temperature_c"])
  hum = float(payload["humidity_pct"])
  co2 = float(payload["co2_ppm"])

  temp_buffer.append(temp)
  co2_buffer.append(co2)

  return pd.DataFrame([{
      "temperature_c": temp,
      "humidity_pct": hum,
      "co2_ppm": co2,
      "hour": ts.hour,
      "is_weekend": int(ts.dayofweek >= 5),
      "temp_lag_1": temp_buffer[-2] if len(temp_buffer) >= 2 else temp,
      "co2_lag_1": co2_buffer[-2] if len(co2_buffer) >= 2 else co2,
      "temp_ma_3": safe_mean(temp_buffer),
      "co2_ma_3": safe_mean(co2_buffer),
  }])


def main():
  parser = argparse.ArgumentParser(description="Subscriber studi kasus A")
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
    client_db = InfluxDBClient(url=INFLUX_URL, token=args.influx_token, org=INFLUX_ORG)
    write_api = client_db.write_api(write_options=SYNCHRONOUS)

  state = {"count": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC, qos=1)
    print("[INFO] Subscribe ke", TOPIC)

  def on_message(client, userdata, msg):
    try:
      payload = json.loads(msg.payload.decode("utf-8"))
      if not valid_payload(payload):
        print("[PERINGATAN] Payload tidak valid, dilewati:", payload)
        return
      X = build_features(payload)
      pred = model.predict(X)[0]
      print(f"[{payload['timestamp']}] -> status={pred}")

      if write_api is not None:
        from influxdb_client import Point, WritePrecision
        point = (
            Point("case_a_room")
            .tag("device_id", payload["device_id"])
            .tag("pred_status", str(pred))
            .field("temperature_c", float(payload["temperature_c"]))
            .field("humidity_pct", float(payload["humidity_pct"]))
            .field("co2_ppm", float(payload["co2_ppm"]))
            .time(payload["timestamp"], WritePrecision.S)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
      else:
        records.append({**payload, "predicted_status": pred})

      state["count"] += 1
      if args.max_messages and state["count"] >= args.max_messages:
        client.disconnect()
    except Exception as exc:
      print("[ERROR] Gagal memproses pesan:", exc)

  client = mqtt.Client(client_id="casea-room-sub")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(BROKER, 1883, 60)
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
    print(f"[SUKSES] {len(records)} prediksi disimpan ke {CSV_PATH}")


if __name__ == "__main__":
  main()
