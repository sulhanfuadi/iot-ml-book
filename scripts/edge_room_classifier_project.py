"""
Hands-on 29 (Bab 11): Mini Proyek Klasifikasi Edge (tanpa MQTT)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Alur: simulator sensor -> model lokal -> status klasifikasi -> log CSV.
Meniru deployment di Raspberry Pi / emulator Linux.
Output: outputs/reports/edge_room_predictions.csv
"""

import argparse
import random
import time
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path("outputs/models/room_status_rf.joblib")
OUTPUT_LOG = Path("outputs/reports/edge_room_predictions.csv")


def build_feature_row(temp, hum, co2, power, hour, dow):
  # Pada implementasi nyata, lag/rolling dipertahankan dari buffer lokal
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
  parser = argparse.ArgumentParser(description="Mini proyek edge room classifier")
  parser.add_argument("--steps", type=int, default=30, help="Jumlah langkah simulasi")
  parser.add_argument("--delay", type=float, default=0.05, help="Jeda antar-langkah (detik)")
  args = parser.parse_args()

  OUTPUT_LOG.parent.mkdir(parents=True, exist_ok=True)
  model = joblib.load(MODEL_PATH)

  rng = random.Random(42)
  records = []

  print("=== Mini proyek edge room classifier dimulai ===")
  for step in range(args.steps):
    temp = round(rng.uniform(24.0, 33.0), 2)
    hum = round(rng.uniform(40.0, 70.0), 2)
    co2 = rng.randint(450, 1500)
    power = round(rng.uniform(100.0, 300.0), 2)
    hour = (8 + step // 3) % 24
    dow = 2  # misal Rabu

    X = build_feature_row(temp, hum, co2, power, hour, dow)
    pred = model.predict(X)[0]

    print(f"step={step} | T={temp} H={hum} CO2={co2} P={power} -> status={pred}")

    records.append({
        "step": step,
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "predicted_status": pred,
    })
    time.sleep(args.delay)

  pd.DataFrame(records).to_csv(OUTPUT_LOG, index=False)
  print("[SUKSES] Log hasil inferensi disimpan ke:", OUTPUT_LOG)


if __name__ == "__main__":
  main()
