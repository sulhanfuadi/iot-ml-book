"""
Hands-on 38 (Bab 15): Latih Isolation Forest Baseline untuk Capstone
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Baseline perilaku normal sintetis (2000 sampel), contamination 5%.
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

  # synthetic training baseline
  rng = np.random.default_rng(42)
  n = 2000
  df = pd.DataFrame({
      "temperature_c": rng.normal(27.0, 1.5, n),
      "humidity_pct": rng.normal(55.0, 6.0, n),
      "power_watt": rng.normal(140.0, 20.0, n),
      "current_amp": rng.normal(5.5, 0.8, n),
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
