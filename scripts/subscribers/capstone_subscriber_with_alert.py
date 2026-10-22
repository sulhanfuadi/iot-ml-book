"""
Hands-on 38 (Bab 15): Capstone Subscriber dengan Alert
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Seperti capstone_subscriber.py, plus alert ke topik capstone/iotnode01/alert
bila threshold terpicu atau Isolation Forest menandai anomali.
Alert disimpan ke outputs/reports/capstone_alerts.csv (atau InfluxDB dengan --influx).
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
TOPIC_ALERT = "capstone/iotnode01/alert"

MODEL_PATH = Path("data/models/capstone_iforest.joblib")
CSV_PATH = Path("outputs/reports/capstone_monitoring.csv")
ALERT_CSV_PATH = Path("outputs/reports/capstone_alerts.csv")

INFLUX_URL = "http://localhost:8086"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"

FEATURE_COLS = ["temperature_c", "humidity_pct", "power_watt", "current_amp"]

records = []
alerts = []


def validate_payload(payload):
  required = ["timestamp", "device_id", "temperature_c",
              "humidity_pct", "power_watt", "current_amp"]
  for field in required:
    if field not in payload:
      raise ValueError(f"Field hilang: {field}")
  float(payload["temperature_c"])
  float(payload["humidity_pct"])
  float(payload["power_watt"])
  float(payload["current_amp"])


def build_features(payload):
  return pd.DataFrame([{
      "temperature_c": float(payload["temperature_c"]),
      "humidity_pct": float(payload["humidity_pct"]),
      "power_watt": float(payload["power_watt"]),
      "current_amp": float(payload["current_amp"]),
  }])


def main():
  parser = argparse.ArgumentParser(description="Capstone subscriber dengan alert")
  parser.add_argument("--max-messages", type=int, default=15)
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

  state = {"count": 0, "alerts": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Connected to broker.")
    client.subscribe(TOPIC, qos=1)
    print("[INFO] Subscribed to", TOPIC)

  def on_message(client, userdata, msg):
    try:
      payload = json.loads(msg.payload.decode("utf-8"))
      validate_payload(payload)
      X = build_features(payload)

      threshold_alert = int(
          X["power_watt"].iloc[0] > 280 or X["current_amp"].iloc[0] > 10.0
      )
      pred = model.predict(X[FEATURE_COLS])[0]
      anomaly_flag = 1 if pred == -1 else 0

      print(
          f"[{payload['timestamp']}] "
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

      is_alert = threshold_alert == 1 or anomaly_flag == 1
      if is_alert:
        reasons = []
        if threshold_alert:
          reasons.append("threshold")
        if anomaly_flag:
          reasons.append("isolation_forest")
        alert_payload = {
            "timestamp": payload["timestamp"],
            "device_id": payload["device_id"],
            "alert_reason": "+".join(reasons),
            "temperature_c": payload["temperature_c"],
            "humidity_pct": payload["humidity_pct"],
            "power_watt": payload["power_watt"],
            "current_amp": payload["current_amp"],
        }
        client.publish(TOPIC_ALERT, json.dumps(alert_payload), qos=1)
        print("[PERINGATAN] ALERT:", json.dumps(alert_payload))
        state["alerts"] += 1

        if write_api is not None:
          alert_point = (
              Point("capstone_alerts")
              .tag("device_id", payload["device_id"])
              .tag("alert_reason", alert_payload["alert_reason"])
              .field("power_watt", float(payload["power_watt"]))
              .field("current_amp", float(payload["current_amp"]))
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
      print("[ERROR]", exc)

  client = mqtt.Client(client_id="capstone-subscriber-alert")
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

  if write_api is None:
    if records:
      pd.DataFrame(records).to_csv(CSV_PATH, index=False)
    pd.DataFrame(alerts).to_csv(ALERT_CSV_PATH, index=False)
    print(f"[SUKSES] {len(records)} hasil ke {CSV_PATH}, "
          f"{len(alerts)} alert ke {ALERT_CSV_PATH}")


if __name__ == "__main__":
  main()
