import json
from pathlib import Path
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
BROKER = "localhost"
PORT = 1883
TOPIC_INPUT = "capstone/iotnode01/telemetry"
TOPIC_ALERT = "capstone/iotnode01/alert"
MODEL_PATH = Path("data/models/capstone_iforest.joblib")
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "GANTI_DENGAN_TOKEN_ANDA"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"
feature_cols = ["temperature_c", "humidity_pct", "power_watt", "current_amp"]
model = joblib.load(MODEL_PATH)
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
def validate_payload(payload):
    required = ["timestamp", "device_id", "temperature_c", "humidity_pct", "power_watt", "current_amp"]
    for field in required:
        if field not in payload:
            raise ValueError(f"Field hilang: {field}")
def build_features(payload):
    return pd.DataFrame([{
        "temperature_c": float(payload["temperature_c"]),
        "humidity_pct": float(payload["humidity_pct"]),
        "power_watt": float(payload["power_watt"]),
        "current_amp": float(payload["current_amp"]),
    }])
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC_INPUT, qos=1)
    print("Subscribed to", TOPIC_INPUT)
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        validate_payload(payload)
        X = build_features(payload)
        threshold_alert = int(
            X["power_watt"].iloc[0] > 280 or
            X["current_amp"].iloc[0] > 10.0
        )
        pred = model.predict(X[feature_cols])[0]
        anomaly_flag = 1 if pred == -1 else 0
        is_alert = threshold_alert == 1 or anomaly_flag == 1
        reason = []
        if threshold_alert:
            reason.append("threshold")
        if anomaly_flag:
            reason.append("iforest")
        reason_text = ",".join(reason) if reason else "none"
        # simpan data monitoring biasa
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
        if is_alert:
            alert_payload = {
                "timestamp": payload["timestamp"],
                "device_id": payload["device_id"],
                "temperature_c": payload["temperature_c"],
                "humidity_pct": payload["humidity_pct"],
                "power_watt": payload["power_watt"],
                "current_amp": payload["current_amp"],
                "reason": reason_text
            }
            client.publish(TOPIC_ALERT, json.dumps(alert_payload), qos=1)
            print("ALERT:", alert_payload)
            alert_point = (
                Point("capstone_alerts")
                .tag("device_id", payload["device_id"])
                .tag("reason", reason_text)
                .field("temperature_c", float(payload["temperature_c"]))
                .field("humidity_pct", float(payload["humidity_pct"]))
                .field("power_watt", float(payload["power_watt"]))
                .field("current_amp", float(payload["current_amp"]))
                .field("alert_flag", 1)
                .time(payload["timestamp"], WritePrecision.S)
            )
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=alert_point)
    except Exception as exc:
        print("Error:", exc)
client = mqtt.Client(client_id="capstone-subscriber-alert")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
