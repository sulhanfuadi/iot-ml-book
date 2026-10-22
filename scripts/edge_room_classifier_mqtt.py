"""
Hands-on 29 (Bab 11): Mini Proyek Klasifikasi Edge dengan MQTT (opsional)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Alur: simulator sensor -> model lokal -> status -> publish MQTT ke
iotlab/room01/prediction. Membutuhkan broker lokal (lihat scripts/mqtt/run_broker.py).
"""

import argparse
import json
import random
import time
from pathlib import Path

import joblib
import pandas as pd
import paho.mqtt.client as mqtt

MODEL_PATH = Path("models/room_status_rf.joblib")
TOPIC = "iotlab/room01/prediction"


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
      "power_ma_3": power,
  }
  return pd.DataFrame([row])


def main():
  parser = argparse.ArgumentParser(description="Mini proyek edge room classifier + MQTT")
  parser.add_argument("--steps", type=int, default=20, help="Jumlah langkah simulasi")
  parser.add_argument("--delay", type=float, default=0.05, help="Jeda antar-langkah (detik)")
  parser.add_argument("--host", default="localhost")
  parser.add_argument("--port", type=int, default=1883)
  args = parser.parse_args()

  model = joblib.load(MODEL_PATH)

  client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="edge-room-classifier")
  client.connect(args.host, args.port, 60)
  client.loop_start()

  rng = random.Random(42)

  print("=== Mini proyek edge room classifier + MQTT dimulai ===")
  for step in range(args.steps):
    temp = round(rng.uniform(24.0, 33.0), 2)
    hum = round(rng.uniform(40.0, 70.0), 2)
    co2 = rng.randint(450, 1500)
    power = round(rng.uniform(100.0, 300.0), 2)
    hour = (8 + step // 3) % 24
    dow = 2

    X = build_feature_row(temp, hum, co2, power, hour, dow)
    pred = model.predict(X)[0]

    payload = {
        "step": step,
        "device_id": "room01",
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "predicted_status": pred,
    }
    client.publish(TOPIC, json.dumps(payload))
    print(f"step={step} | publish {TOPIC} -> status={pred}")
    time.sleep(args.delay)

  client.loop_stop()
  client.disconnect()
  print("[SUKSES] Semua prediksi dipublish ke broker.")


if __name__ == "__main__":
  main()
