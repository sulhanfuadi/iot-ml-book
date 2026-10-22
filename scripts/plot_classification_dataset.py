"""
Hands-on 12: Visualisasi Dataset Klasifikasi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/synthetic/room_classification_dataset.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH)

  warna = {"normal": "steelblue", "warning": "orange", "fault": "red"}

  fig, axes = plt.subplots(1, 2, figsize=(13, 5))
  for label, g in df.groupby("status_label"):
    axes[0].scatter(g["temperature_c"], g["co2_ppm"], s=6, alpha=0.5,
                    c=warna[label], label=label)
  axes[0].set_xlabel("Suhu (C)")
  axes[0].set_ylabel("CO2 (ppm)")
  axes[0].set_title("Suhu vs CO2 per Label")
  axes[0].legend()

  for label, g in df.groupby("status_label"):
    axes[1].scatter(g["temperature_c"], g["power_watt"], s=6, alpha=0.5,
                    c=warna[label], label=label)
  axes[1].set_xlabel("Suhu (C)")
  axes[1].set_ylabel("Daya (watt)")
  axes[1].set_title("Suhu vs Daya per Label")
  axes[1].legend()

  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_classification_scatter.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_classification_scatter.png")


if __name__ == "__main__":
  main()
