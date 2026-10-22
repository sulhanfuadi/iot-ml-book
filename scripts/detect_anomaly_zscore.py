"""
Hands-on 8: Deteksi Anomali - Metode 2: Z-Score
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Z-score mengukur jarak nilai dari rata-rata dalam satuan deviasi standar.
Ambang: |z| > 3.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")


def zscore(series: pd.Series) -> pd.Series:
  return (series - series.mean()) / series.std(ddof=0)


def main():
  df = pd.read_csv(DATA_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])

  df["z_temp"] = zscore(df["temperature_c"])
  df["z_co2"] = zscore(df["co2_ppm"])
  df["z_power"] = zscore(df["power_watt"])
  df["anomaly_zscore"] = (
      (df["z_temp"].abs() > 3)
      | (df["z_co2"].abs() > 3)
      | (df["z_power"].abs() > 3)
  )

  print("=== Deteksi anomali - Z-score (|z| > 3) ===")
  flagged = df[df["anomaly_zscore"]]
  print(flagged[[
      "timestamp", "temperature_c", "z_temp",
      "co2_ppm", "z_co2", "power_watt", "z_power",
  ]].to_string(index=False))
  print(f"\n[INFO] Titik anomali terdeteksi: {len(flagged)}")


if __name__ == "__main__":
  main()
