"""
Hands-on 15: Visualisasi Fitur Getaran per Jendela
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/processed/vibration_window_features.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH)
  warna = {"normal": "steelblue", "fault": "tomato"}
  colors = df["status_label"].map(warna)

  fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
  axes[0].scatter(df["window_start"], df["rms"], c=colors, s=10)
  axes[0].set_ylabel("RMS")
  axes[0].set_title("Fitur Getaran per Jendela (biru=normal, merah=fault)")
  axes[1].scatter(df["window_start"], df["peak_to_peak"], c=colors, s=10)
  axes[1].set_ylabel("Peak-to-peak")
  axes[2].scatter(df["window_start"], df["kurtosis"], c=colors, s=10)
  axes[2].set_ylabel("Kurtosis")
  axes[2].set_xlabel("Window start (sample)")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "vibration_window_features.png")
  plt.close()
  print("[SUKSES] outputs/figures/vibration_window_features.png")


if __name__ == "__main__":
  main()
