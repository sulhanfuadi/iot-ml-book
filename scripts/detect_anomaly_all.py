"""
Hands-on 8: Versi Gabungan - Aturan Domain + Z-Score + IQR
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Titik yang muncul di ketiga metode sekaligus layak diperiksa lebih serius.
Hasil lengkap disimpan ke data/processed/room_sensor_anomaly_flags.csv.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")
OUTPUT_PATH = Path("data/processed/room_sensor_anomaly_flags.csv")


def zscore(series: pd.Series) -> pd.Series:
  return (series - series.mean()) / series.std(ddof=0)


def iqr_bounds(series: pd.Series):
  q1 = series.quantile(0.25)
  q3 = series.quantile(0.75)
  iqr = q3 - q1
  return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def main():
  df = pd.read_csv(DATA_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])

  # Rule-based
  df["anomaly_rule"] = (
      (df["temperature_c"] > 35)
      | (df["co2_ppm"] > 1200)
      | (df["power_watt"] > 250)
  )

  # Z-score
  df["z_temp"] = zscore(df["temperature_c"])
  df["z_co2"] = zscore(df["co2_ppm"])
  df["z_power"] = zscore(df["power_watt"])
  df["anomaly_zscore"] = (
      (df["z_temp"].abs() > 3)
      | (df["z_co2"].abs() > 3)
      | (df["z_power"].abs() > 3)
  )

  # IQR
  temp_lower, temp_upper = iqr_bounds(df["temperature_c"])
  co2_lower, co2_upper = iqr_bounds(df["co2_ppm"])
  power_lower, power_upper = iqr_bounds(df["power_watt"])
  df["anomaly_iqr"] = (
      (df["temperature_c"] < temp_lower) | (df["temperature_c"] > temp_upper)
      | (df["co2_ppm"] < co2_lower) | (df["co2_ppm"] > co2_upper)
      | (df["power_watt"] < power_lower) | (df["power_watt"] > power_upper)
  )

  df["anomaly_all_methods"] = (
      df["anomaly_rule"] & df["anomaly_zscore"] & df["anomaly_iqr"]
  )

  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(OUTPUT_PATH, index=False)

  cols = [
      "timestamp", "temperature_c", "co2_ppm", "power_watt",
      "anomaly_rule", "anomaly_zscore", "anomaly_iqr", "anomaly_all_methods",
  ]
  flagged = df[df[["anomaly_rule", "anomaly_zscore", "anomaly_iqr"]].any(axis=1)]
  print("=== Titik yang terdeteksi minimal satu metode ===")
  print(flagged[cols].to_string(index=False))
  print(f"\n[INFO] rule: {df['anomaly_rule'].sum()} titik")
  print(f"[INFO] zscore: {df['anomaly_zscore'].sum()} titik")
  print(f"[INFO] iqr: {df['anomaly_iqr'].sum()} titik")
  print(f"[INFO] ketiga metode sekaligus: {df['anomaly_all_methods'].sum()} titik")
  print(f"[SUKSES] Hasil lengkap disimpan ke {OUTPUT_PATH}")


if __name__ == "__main__":
  main()
