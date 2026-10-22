import json
from pathlib import Path
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
BROKER = "localhost"
PORT = 1883
TOPIC = "capstone/iotnode01/telemetry"
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
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to broker.")
    client.subscribe(TOPIC, qos=1)
    print("Subscribed to", TOPIC)
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        validate_payload(payload)
        X = build_features(payload)
        # threshold baseline
        threshold_alert = int(
            X["power_watt"].iloc[0] > 280 or
            X["current_amp"].iloc[0] > 10.0
        )
        # Isolation Forest
        pred = model.predict(X[feature_cols])[0]         # 1 normal, -1 anomaly
        anomaly_flag = 1 if pred == -1 else 0
        print(
            f"[{payload['timestamp']}] "
            f"T={payload['temperature_c']} "
            f"H={payload['humidity_pct']} "
            f"P={payload['power_watt']} "
            f"I={payload['current_amp']} "
            f"-> anomaly={anomaly_flag}, threshold={threshold_alert}"
        )
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
    except Exception as exc:
        print("Error:", exc)
client = mqtt.Client(client_id="capstone-subscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
