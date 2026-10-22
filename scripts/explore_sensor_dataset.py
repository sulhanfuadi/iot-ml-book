"""
Hands-on 6: Eksplorasi Dataset Sensor dengan pandas
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Eksplorasi awal dataset: struktur data, konversi timestamp,
time-series index, ringkasan operasional, dan korelasi antar variabel.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_week.csv")


def main():
  df = pd.read_csv(DATA_PATH)

  print("=== 5 baris pertama ===")
  print(df.head())

  print("\n=== Ukuran data ===")
  print(df.shape)

  print("\n=== Nama kolom ===")
  print(df.columns.tolist())

  print("\n=== Info dataset ===")
  print(df.info())

  print("\n=== Statistik numerik ===")
  print(df.describe(include="all"))

  # Konversi timestamp dan cek rentang waktu
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  print("\n=== Rentang waktu ===")
  print("Mulai :", df["timestamp"].min())
  print("Akhir :", df["timestamp"].max())

  print("\n=== Jumlah device ===")
  print(df["device_id"].nunique())
  print(df["device_id"].unique())

  # Jadikan time series
  df = df.sort_values("timestamp")
  df = df.set_index("timestamp")
  print("\n=== Data dengan index waktu ===")
  print(df.head())
  print("\n[INFO] Frekuensi data belum dipaksa, tapi index waktu sudah siap.")

  # Ringkasan operasional
  summary = {
      "temperature_min": df["temperature_c"].min(),
      "temperature_max": df["temperature_c"].max(),
      "temperature_mean": df["temperature_c"].mean(),
      "humidity_min": df["humidity_pct"].min(),
      "humidity_max": df["humidity_pct"].max(),
      "co2_max": df["co2_ppm"].max(),
      "power_mean": df["power_watt"].mean(),
  }
  print("\n=== Ringkasan operasional ===")
  for k, v in summary.items():
    print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

  # Korelasi awal
  corr = df[["temperature_c", "humidity_pct", "co2_ppm", "power_watt"]].corr()
  print("\n=== Korelasi antar variabel ===")
  print(corr)


if __name__ == "__main__":
  main()
