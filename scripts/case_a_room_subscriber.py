import json
from collections import deque
from pathlib import Path
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
BROKER = "localhost"
TOPIC = "casea/room01/telemetry"
MODEL_PATH = Path("models/case_a_room_rf.joblib")
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "GANTI_DENGAN_TOKEN_ANDA"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"
temp_buffer = deque(maxlen=3)
co2_buffer = deque(maxlen=3)
model = joblib.load(MODEL_PATH)
client_db = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_db.write_api(write_options=SYNCHRONOUS)
def safe_mean(values):
    return sum(values) / len(values) if len(values) > 0 else None
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
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC, qos=1)
    print("Subscribe ke", TOPIC)
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    X = build_features(payload)
    pred = model.predict(X)[0]
    print(f"[{payload['timestamp']}] -> status={pred}")
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
client = mqtt.Client(client_id="casea-room-sub")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
