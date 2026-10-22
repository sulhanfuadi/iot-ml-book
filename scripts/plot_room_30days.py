"""
Hands-on 9: Visualisasi Cepat Dataset 30 Hari
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
  df = df.set_index("timestamp")

  fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
  axes[0].plot(df.index, df["temperature_c"], lw=0.6, color="tomato")
  axes[0].set_title("Suhu Ruangan 30 Hari (interval 10 menit)")
  axes[0].set_ylabel("Suhu (C)")
  axes[1].plot(df.index, df["humidity_pct"], lw=0.6, color="steelblue")
  axes[1].set_title("Kelembaban Ruangan 30 Hari")
  axes[1].set_ylabel("Kelembaban (%)")
  axes[1].set_xlabel("Waktu")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_30days.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_30days.png")

  # Rata-rata harian untuk melihat drift dan pola hari kerja/akhir pekan
  daily = df.resample("1D").mean(numeric_only=True)
  plt.figure(figsize=(10, 5))
  plt.plot(daily.index, daily["temperature_c"], marker="o", label="suhu rata-rata")
  plt.plot(daily.index, daily["humidity_pct"], marker="s", label="kelembaban rata-rata")
  plt.title("Rata-rata Harian - Suhu dan Kelembaban")
  plt.xlabel("Tanggal")
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_30days_daily.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_30days_daily.png")


if __name__ == "__main__":
  main()
