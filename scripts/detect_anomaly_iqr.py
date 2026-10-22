"""
Hands-on 8: Deteksi Anomali - Metode 3: IQR
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Batas IQR: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]. Lebih tahan terhadap nilai ekstrim.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")


def iqr_bounds(series: pd.Series):
  q1 = series.quantile(0.25)
  q3 = series.quantile(0.75)
  iqr = q3 - q1
  lower = q1 - 1.5 * iqr
  upper = q3 + 1.5 * iqr
  return lower, upper


def main():
  df = pd.read_csv(DATA_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])

  temp_lower, temp_upper = iqr_bounds(df["temperature_c"])
  co2_lower, co2_upper = iqr_bounds(df["co2_ppm"])
  power_lower, power_upper = iqr_bounds(df["power_watt"])

  print("[INFO] Batas IQR:")
  print(f"  temperature_c: [{temp_lower:.2f}, {temp_upper:.2f}]")
  print(f"  co2_ppm      : [{co2_lower:.2f}, {co2_upper:.2f}]")
  print(f"  power_watt   : [{power_lower:.2f}, {power_upper:.2f}]")

  df["anomaly_iqr"] = (
      (df["temperature_c"] < temp_lower) | (df["temperature_c"] > temp_upper)
      | (df["co2_ppm"] < co2_lower) | (df["co2_ppm"] > co2_upper)
      | (df["power_watt"] < power_lower) | (df["power_watt"] > power_upper)
  )

  print("\n=== Deteksi anomali - IQR ===")
  flagged = df[df["anomaly_iqr"]]
  print(flagged[["timestamp", "temperature_c", "co2_ppm", "power_watt"]].to_string(index=False))
  print(f"\n[INFO] Titik anomali terdeteksi: {len(flagged)}")


if __name__ == "__main__":
  main()
