"""
Hands-on 6: Visualisasi Eksploratif Pertama
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_week.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.set_index("timestamp")

  # Plot suhu
  plt.figure(figsize=(10, 5))
  plt.plot(df.index, df["temperature_c"])
  plt.title("Eksplorasi Awal - Suhu Ruangan")
  plt.xlabel("Waktu")
  plt.ylabel("Suhu (C)")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "explore_temperature.png")
  plt.close()
  print("[SUKSES] outputs/figures/explore_temperature.png")

  # Plot CO2
  plt.figure(figsize=(10, 5))
  plt.plot(df.index, df["co2_ppm"], color="darkgreen")
  plt.title("Eksplorasi Awal - CO2 Ruangan")
  plt.xlabel("Waktu")
  plt.ylabel("CO2 (ppm)")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "explore_co2.png")
  plt.close()
  print("[SUKSES] outputs/figures/explore_co2.png")

  # Plot kelembaban
  plt.figure(figsize=(10, 5))
  plt.plot(df.index, df["humidity_pct"], color="steelblue")
  plt.title("Eksplorasi Awal - Kelembaban Ruangan")
  plt.xlabel("Waktu")
  plt.ylabel("Kelembaban (%)")
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "explore_humidity.png")
  plt.close()
  print("[SUKSES] outputs/figures/explore_humidity.png")

  # Heatmap korelasi
  corr = df[["temperature_c", "humidity_pct", "co2_ppm", "power_watt"]].corr()
  plt.figure(figsize=(6, 5))
  plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
  plt.colorbar(label="Korelasi")
  plt.xticks(range(len(corr)), corr.columns, rotation=45, ha="right")
  plt.yticks(range(len(corr)), corr.columns)
  for i in range(len(corr)):
    for j in range(len(corr)):
      plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
  plt.title("Korelasi Antar Variabel Sensor")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "explore_correlation.png")
  plt.close()
  print("[SUKSES] outputs/figures/explore_correlation.png")


if __name__ == "__main__":
  main()
