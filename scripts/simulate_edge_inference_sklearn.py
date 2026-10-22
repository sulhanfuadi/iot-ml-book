"""
Hands-on 28 (Bab 11): Simulasi Inferensi Lokal di Edge - scikit-learn
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Data sensor masuk satu per satu; model joblib yang sudah dilatih memberi prediksi
status lokal. Pola ini meniru gateway edge: model dimuat sekali, inferensi cepat.
"""

import argparse
import time
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path("models/room_status_rf.joblib")
DATA_PATH = Path("data/processed/classification_status/test.csv")

FEATURE_COLS = [
    "temperature_c", "humidity_pct", "co2_ppm", "power_watt",
    "hour", "day_of_week", "is_weekend",
    "temp_lag_1", "co2_lag_1", "power_lag_1",
    "temp_ma_3", "co2_ma_3", "power_ma_3",
]


def main():
  parser = argparse.ArgumentParser(description="Simulasi inferensi edge scikit-learn")
  parser.add_argument("--max-rows", type=int, default=30,
                      help="Jumlah baris simulasi (default 30)")
  parser.add_argument("--delay", type=float, default=0.05,
                      help="Jeda antar-sampel dalam detik (default 0.05)")
  args = parser.parse_args()

  model = joblib.load(MODEL_PATH)
  df = pd.read_csv(DATA_PATH).head(args.max_rows)

  print("=== Simulasi inferensi lokal di edge (scikit-learn) ===")
  for _, row in df.iterrows():
    x = row[FEATURE_COLS].to_frame().T
    pred = model.predict(x)[0]
    print(
        f"[{row['timestamp']}] "
        f"T={row['temperature_c']:.2f}C, "
        f"H={row['humidity_pct']:.2f}%, "
        f"CO2={row['co2_ppm']}, "
        f"P={row['power_watt']:.2f}W "
        f"-> status_pred={pred}"
    )
    time.sleep(args.delay)  # simulasi aliran data


if __name__ == "__main__":
  main()
