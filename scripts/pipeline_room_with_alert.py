"""
Hands-on 31 (Bab 12): Pipeline dengan Alert Sederhana
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Subscriber pipeline + alert: alert diterbitkan ke topik iotlab/room01/alert bila
model memprediksi FAULT atau suhu > 32 C dan CO2 > 1200 ppm bersamaan.

Storage default: CSV lokal (outputs/reports/pipeline_room_alerts.csv).
Storage InfluxDB sesuai buku: aktifkan dengan --influx.
"""

import argparse
import json
from collections import deque
from pathlib import Path

import joblib
import pandas as pd
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_INPUT = "iotlab/room01/telemetry"
TOPIC_ALERT = "iotlab/room01/alert"

MODEL_PATH = Path("outputs/models/room_status_rf.joblib")
CSV_PATH = Path("outputs/reports/pipeline_room_alerts.csv")

INFLUX_URL = "http://localhost:8086"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"

temp_buffer = deque(maxlen=3)
co2_buffer = deque(maxlen=3)
power_buffer = deque(maxlen=3)

alerts = []


def safe_mean(values):
  return sum(values) / len(values) if len(values) > 0 else None


def build_features(data):
  temp = float(data["temperature_c"])
  hum = float(data["humidity_pct"])
  co2 = float(data["co2_ppm"])
  power = float(data["power_watt"])

  temp_buffer.append(temp)
  co2_buffer.append(co2)
  power_buffer.append(power)

  ts = pd.to_datetime(data["timestamp"])
  return pd.DataFrame([{
      "temperature_c": temp,
      "humidity_pct": hum,
      "co2_ppm": co2,
      "power_watt": power,
      "hour": ts.hour,
      "day_of_week": ts.dayofweek,
      "is_weekend": int(ts.dayofweek >= 5),
      "temp_lag_1": temp_buffer[-2] if len(temp_buffer) >= 2 else temp,
      "co2_lag_1": co2_buffer[-2] if len(co2_buffer) >= 2 else co2,
      "power_lag_1": power_buffer[-2] if len(power_buffer) >= 2 else power,
      "temp_ma_3": safe_mean(temp_buffer),
      "co2_ma_3": safe_mean(co2_buffer),
      "power_ma_3": safe_mean(power_buffer),
  }])


def should_alert(payload, pred_status):
  # Aturan sederhana yang mudah dipahami
  if pred_status == "fault":
    return True, "Model memprediksi FAULT"
  if float(payload["temperature_c"]) > 32.0 and float(payload["co2_ppm"]) > 1200:
    return True, "Suhu dan CO2 sama-sama tinggi"
  return False, ""


def main():
  parser = argparse.ArgumentParser(description="Subscriber pipeline dengan alert")
  parser.add_argument("--max-messages", type=int, default=10,
                      help="Berhenti setelah N pesan (0 = terus-menerus)")
  parser.add_argument("--timeout", type=int, default=60)
  parser.add_argument("--influx", action="store_true",
                      help="Simpan ke InfluxDB (butuh server InfluxDB 2)")
  parser.add_argument("--influx-token", default="GANTI_DENGAN_TOKEN_ANDA")
  parser.add_argument("--host", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  args = parser.parse_args()

  model = joblib.load(MODEL_PATH)
  CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

  write_api = None
  if args.influx:
    from influxdb_client import InfluxDBClient
    from influxdb_client.client.write_api import SYNCHRONOUS
    influx_client = InfluxDBClient(url=INFLUX_URL, token=args.influx_token, org=INFLUX_ORG)
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    print("[INFO] Storage: InfluxDB", INFLUX_URL)
  else:
    print("[INFO] Storage alert: CSV lokal", CSV_PATH)

  state = {"count": 0, "alerts": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Subscriber+Alert terhubung ke broker.")
    client.subscribe(TOPIC_INPUT, qos=1)
    print(f"[INFO] Subscribe ke: {TOPIC_INPUT}")

  def on_message(client, userdata, msg):
    try:
      payload = json.loads(msg.payload.decode("utf-8"))
      X = build_features(payload)
      pred_status = model.predict(X)[0]
      print(f"[{payload['timestamp']}] -> status={pred_status}")

      if write_api is not None:
        from influxdb_client import Point, WritePrecision
        point = (
            Point("room_pipeline")
            .tag("device_id", payload["device_id"])
            .field("temperature_c", float(payload["temperature_c"]))
            .field("humidity_pct", float(payload["humidity_pct"]))
            .field("co2_ppm", float(payload["co2_ppm"]))
            .field("power_watt", float(payload["power_watt"]))
            .field("pred_status_code",
                   0 if pred_status == "normal" else (1 if pred_status == "warning" else 2))
            .tag("pred_status", str(pred_status))
            .time(payload["timestamp"], WritePrecision.S)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

      # Alert sederhana
      is_alert, alert_reason = should_alert(payload, pred_status)
      if is_alert:
        alert_payload = {
            "timestamp": payload["timestamp"],
            "device_id": payload["device_id"],
            "pred_status": pred_status,
            "alert_reason": alert_reason,
            "temperature_c": payload["temperature_c"],
            "humidity_pct": payload["humidity_pct"],
            "co2_ppm": payload["co2_ppm"],
            "power_watt": payload["power_watt"],
        }
        client.publish(TOPIC_ALERT, json.dumps(alert_payload), qos=1)
        print("[PERINGATAN] ALERT:", json.dumps(alert_payload))
        state["alerts"] += 1

        if write_api is not None:
          alert_point = (
              Point("room_alerts")
              .tag("device_id", payload["device_id"])
              .tag("pred_status", str(pred_status))
              .tag("alert_reason", alert_reason)
              .field("temperature_c", float(payload["temperature_c"]))
              .field("humidity_pct", float(payload["humidity_pct"]))
              .field("co2_ppm", float(payload["co2_ppm"]))
              .field("power_watt", float(payload["power_watt"]))
              .field("alert_flag", 1)
              .time(payload["timestamp"], WritePrecision.S)
          )
          write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=alert_point)
        else:
          alerts.append(alert_payload)

      state["count"] += 1
      if args.max_messages and state["count"] >= args.max_messages:
        client.disconnect()
    except Exception as exc:
      print("[ERROR] Gagal memproses pesan:", exc)

  client = mqtt.Client(client_id="subscriber-room-alert")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(args.host, args.port, keepalive=60)
  client.loop_start()

  import time
  start = time.time()
  while time.time() - start < args.timeout:
    if args.max_messages and state["count"] >= args.max_messages:
      break
    time.sleep(0.2)

  client.loop_stop()
  client.disconnect()

  if write_api is None:
    pd.DataFrame(alerts).to_csv(CSV_PATH, index=False)
    print(f"[SUKSES] {len(alerts)} alert disimpan ke {CSV_PATH}")
  print(f"[SUKSES] {state['count']} pesan diproses, {state['alerts']} alert.")


if __name__ == "__main__":
  main()
