from pathlib import Path
import json
import time
import random
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
MODEL_PATH = Path("models/room_status_rf.joblib")
TOPIC = "iotlab/room01/prediction"
model = joblib.load(MODEL_PATH)
client = mqtt.Client(client_id="edge-room-classifier")
client.connect("localhost", 1883, 60)
def build_feature_row(temp, hum, co2, power, hour, dow):
    row = {
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "hour": hour,
            "day_of_week": dow,
        "is_weekend": int(dow >= 5),
        "temp_lag_1": temp,
        "co2_lag_1": co2,
        "power_lag_1": power,
        "temp_ma_3": temp,
        "co2_ma_3": co2,
        "power_ma_3": power
    }
    return pd.DataFrame([row])
for step in range(20):
    temp = round(random.uniform(24.0, 33.0), 2)
    hum = round(random.uniform(40.0, 70.0), 2)
    co2 = random.randint(450, 1500)
    power = round(random.uniform(100.0, 300.0), 2)
    hour = (8 + step // 3) % 24
    dow = 2
    X = build_feature_row(temp, hum, co2, power, hour, dow)
    pred = model.predict(X)[0]
    payload = {
        "step": step,
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "predicted_status": pred
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published:", payload)
    time.sleep(0.5)
client.disconnect()
