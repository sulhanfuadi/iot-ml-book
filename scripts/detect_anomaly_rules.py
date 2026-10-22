"""
Hands-on 8: Deteksi Anomali - Metode 1: Aturan Domain Sederhana
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Ambang operasional: suhu > 35 C, CO2 > 1200 ppm, daya > 250 watt.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")


def main():
  df = pd.read_csv(DATA_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])

  df["anomaly_rule"] = (
      (df["temperature_c"] > 35)
      | (df["co2_ppm"] > 1200)
      | (df["power_watt"] > 250)
  )

  print("=== Deteksi anomali - aturan domain ===")
  print(df[["timestamp", "temperature_c", "co2_ppm", "power_watt", "anomaly_rule"]].to_string(index=False))
  flagged = df[df["anomaly_rule"]]
  print(f"\n[INFO] Titik anomali terdeteksi: {len(flagged)}")
  print(flagged[["timestamp", "temperature_c", "co2_ppm", "power_watt"]].to_string(index=False))


if __name__ == "__main__":
  main()
