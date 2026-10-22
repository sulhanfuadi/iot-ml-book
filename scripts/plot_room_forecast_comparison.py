"""
Hands-on 24 (Bab 10): Visualisasi Perbandingan Forecasting Suhu Ruang
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/figures/room_forecast_compare.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path("data/processed/forecast_room")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  baseline = pd.read_csv(DATA_DIR / "baseline_predictions.csv")
  linear = pd.read_csv(DATA_DIR / "linear_predictions.csv")

  sample = baseline.copy()
  sample["pred_linear"] = linear["pred_linear"]

  plt.figure(figsize=(12, 5))
  plt.plot(sample.index, sample["actual"], label="Actual", linewidth=1.5)
  plt.plot(sample.index, sample["pred_last"], label="Last Value", alpha=0.7)
  plt.plot(sample.index, sample["pred_ma"], label="Moving Average", alpha=0.7)
  plt.plot(sample.index, sample["pred_linear"], label="Linear Regression", alpha=0.7)
  plt.title("Forecasting Suhu Ruang")
  plt.xlabel("Index waktu test")
  plt.ylabel("Temperature (C)")
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_forecast_compare.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_forecast_compare.png")


if __name__ == "__main__":
  main()
