"""
Hands-on 38 (Bab 15): Latih Isolation Forest Baseline untuk Capstone
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Baseline perilaku normal sintetis (2000 sampel), contamination 5%.
Rentang baseline mengikuti rentang payload NORMAL publisher capstone
(temperature 24-34 C, humidity 40-75 %, power 80-260 W, current 3.5-9.5 A),
sesuai prinsip Bab 13: data training harus mewakili kondisi deployment.
Baseline normal sempit dari listing buku (mean 140 W, std 20 W) menandai
hampir setengah traffic normal sebagai anomali ("notifikasi harus cukup
berguna, bukan terlalu berisik" - Bab 15). Formula model tetap persis buku:
IsolationForest(n_estimators=200, contamination=0.05, random_state=42).

Output: outputs/models/capstone_iforest.joblib
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_DIR = Path("outputs/models")

FEATURE_COLS = ["temperature_c", "humidity_pct", "power_watt", "current_amp"]


def main():
  MODEL_DIR.mkdir(parents=True, exist_ok=True)

  # synthetic training baseline: rentang operasi normal deployment
  # (rentang yang sama dengan payload normal capstone_publisher.py)
  rng = np.random.default_rng(42)
  n = 2000
  df = pd.DataFrame({
      "temperature_c": rng.uniform(24.0, 34.0, n),
      "humidity_pct": rng.uniform(40.0, 75.0, n),
      "power_watt": rng.uniform(80.0, 260.0, n),
      "current_amp": rng.uniform(3.5, 9.5, n),
  })

  model = IsolationForest(
      n_estimators=200,
      contamination=0.05,
      random_state=42,
  )
  model.fit(df[FEATURE_COLS])

  joblib.dump(model, MODEL_DIR / "capstone_iforest.joblib")
  print("[SUKSES] Model disimpan ke:", MODEL_DIR / "capstone_iforest.joblib")


if __name__ == "__main__":
  main()
