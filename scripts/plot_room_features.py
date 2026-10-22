"""
Hands-on 14: Visualisasi Fitur Time-Series
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/processed/room_30days_features.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"]).set_index("timestamp")

  # Suhu mentah vs moving average
  window = df.loc["2026-01-05":"2026-01-07"]
  plt.figure(figsize=(12, 5))
  plt.plot(window.index, window["temperature_c"], lw=0.8, label="suhu mentah", alpha=0.6)
  plt.plot(window.index, window["temp_ma_3"], lw=1.5, label="MA-3 (30 menit)")
  plt.plot(window.index, window["temp_ma_6"], lw=1.5, label="MA-6 (1 jam)")
  plt.title("Suhu Mentah vs Moving Average (5-7 Jan 2026)")
  plt.ylabel("Suhu (C)")
  plt.legend()
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "features_moving_average.png")
  plt.close()
  print("[SUKSES] outputs/figures/features_moving_average.png")

  # Laju perubahan suhu
  plt.figure(figsize=(12, 4))
  plt.plot(window.index, window["temp_diff_1"], lw=0.8, color="darkorange")
  plt.title("Difference Suhu (temp_diff_1) - Laju Perubahan per 10 Menit")
  plt.ylabel("Delta suhu (C)")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "features_diff.png")
  plt.close()
  print("[SUKSES] outputs/figures/features_diff.png")

  # Comfort index
  plt.figure(figsize=(12, 4))
  plt.plot(df.index, df["comfort_index_simple"], lw=0.6, color="seagreen")
  plt.title("Comfort Index Sederhana 30 Hari")
  plt.ylabel("comfort_index_simple")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "features_comfort_index.png")
  plt.close()
  print("[SUKSES] outputs/figures/features_comfort_index.png")


if __name__ == "__main__":
  main()
