import json
from collections import deque
from pathlib import Path
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
# MQTT
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"
# Model
MODEL_PATH = Path("models/room_status_rf.joblib")
# InfluxDB
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "GANTI_DENGAN_TOKEN_ANDA"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"
# Buffer sederhana untuk lag / moving average
temp_buffer = deque(maxlen=3)
co2_buffer = deque(maxlen=3)
power_buffer = deque(maxlen=3)
model = joblib.load(MODEL_PATH)
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
def safe_mean(values):
    return sum(values) / len(values) if len(values) > 0 else None
def build_features(data):
    temp = float(data["temperature_c"])
    hum = float(data["humidity_pct"])
    co2 = float(data["co2_ppm"])
    power = float(data["power_watt"])
    # update buffer
    temp_buffer.append(temp)
    co2_buffer.append(co2)
    power_buffer.append(power)
    feature_row = {
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "hour": pd.to_datetime(data["timestamp"]).hour,
        "day_of_week": pd.to_datetime(data["timestamp"]).dayofweek,
        "is_weekend": int(pd.to_datetime(data["timestamp"]).dayofweek >= 5),
        "temp_lag_1": temp_buffer[-2] if len(temp_buffer) >= 2 else temp,
        "co2_lag_1": co2_buffer[-2] if len(co2_buffer) >= 2 else co2,
        "power_lag_1": power_buffer[-2] if len(power_buffer) >= 2 else power,
        "temp_ma_3": safe_mean(temp_buffer),
        "co2_ma_3": safe_mean(co2_buffer),
        "power_ma_3": safe_mean(power_buffer),
    }
    return pd.DataFrame([feature_row])
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Subscriber terhubung ke broker.")
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribe ke: {TOPIC}")
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        # Validasi dasar
        required_fields = [
            "timestamp", "device_id", "temperature_c",
            "humidity_pct", "co2_ppm", "power_watt"
        ]
        for field in required_fields:
            if field not in payload:
                print(f"Field hilang: {field}")
                return
        # Preprocessing + fitur
        X = build_features(payload)
        # Prediksi
        pred_status = model.predict(X)[0]
        print(
            f"[{payload['timestamp']}] "
            f"T={payload['temperature_c']} H={payload['humidity_pct']} "
            f"CO2={payload['co2_ppm']} P={payload['power_watt']} "
            f"-> status={pred_status}"
        )
        # Simpan ke InfluxDB
        point = (
            Point("room_pipeline")
            .tag("device_id", payload["device_id"])
            .field("temperature_c", float(payload["temperature_c"]))
            .field("humidity_pct", float(payload["humidity_pct"]))
            .field("co2_ppm", float(payload["co2_ppm"]))
            .field("power_watt", float(payload["power_watt"]))
            .field("pred_status_code", 0 if pred_status == "normal" else (1 if pred_status == "warning" else 2)).tag("pred_status", str(pred_status)).time(payload["timestamp"], WritePrecision.S)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    except Exception as exc:
        print("Error processing message:", exc)
client = mqtt.Client(client_id="subscriber-room-pipeline")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_forever()
