"""
Hands-on 26 (Bab 10): Visualisasi Perbandingan Model Forecasting Suhu
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/figures/room_compare_mae.png, room_compare_rmse.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("outputs/reports/room_forecast_model_comparison.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  plt.figure(figsize=(10, 5))
  plt.bar(df["model"], df["mae"], color="steelblue")
  plt.title("Perbandingan MAE Forecasting Suhu")
  plt.xlabel("Model")
  plt.ylabel("MAE")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_compare_mae.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_compare_mae.png")

  plt.figure(figsize=(10, 5))
  plt.bar(df["model"], df["rmse"], color="seagreen")
  plt.title("Perbandingan RMSE Forecasting Suhu")
  plt.xlabel("Model")
  plt.ylabel("RMSE")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_compare_rmse.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_compare_rmse.png")


if __name__ == "__main__":
  main()
