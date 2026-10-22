"""
Hands-on 12: Dataset Sintetis untuk Klasifikasi dan Anomaly Detection
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Dataset smart room monitoring 15 hari @ 10 menit dengan label
normal / warning / fault dan kolom biner is_anomaly.
Output: data/synthetic/room_classification_dataset.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/room_classification_dataset.csv")


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  rng = np.random.default_rng(2026)

  timestamps = pd.date_range(
      start="2026-01-01 00:00:00",
      end="2026-01-15 23:50:00",
      freq="10min",
  )
  hours = timestamps.hour + timestamps.minute / 60.0
  dow = timestamps.dayofweek

  daily_temp = 24 + 3.5 * np.sin((hours - 6) / 24 * 2 * np.pi)
  workday_effect = np.where(dow < 5, 1.0, 0.3)
  temperature = daily_temp + workday_effect + rng.normal(0, 0.4, len(timestamps))
  humidity = 67 - 0.8 * (daily_temp - 24) + rng.normal(0, 1.8, len(timestamps))
  co2 = 500 + (temperature - 24) * 70 + rng.normal(0, 30, len(timestamps))
  power = (
      120 + (temperature - 24) * 12 + workday_effect * 18
      + rng.normal(0, 8, len(timestamps))
  )

  df = pd.DataFrame({
      "timestamp": timestamps,
      "device_id": "room01",
      "temperature_c": np.round(temperature, 2),
      "humidity_pct": np.round(humidity, 2),
      "co2_ppm": np.round(co2, 0),
      "power_watt": np.round(power, 2),
  })

  # Injeksi warning: salah satu/beberapa nilai mendekati batas
  warning_idx = rng.choice(df.index, size=80, replace=False)
  df.loc[warning_idx, "temperature_c"] += rng.uniform(2.0, 4.0, len(warning_idx))
  df.loc[warning_idx, "co2_ppm"] += rng.uniform(120, 280, len(warning_idx))
  df.loc[warning_idx, "power_watt"] += rng.uniform(20, 50, len(warning_idx))

  # Injeksi fault: lonjakan besar / kombinasi buruk
  remaining_idx = list(set(df.index) - set(warning_idx))
  fault_idx = rng.choice(remaining_idx, size=30, replace=False)
  df.loc[fault_idx, "temperature_c"] += rng.uniform(6.0, 10.0, len(fault_idx))
  df.loc[fault_idx, "co2_ppm"] += rng.uniform(500, 1000, len(fault_idx))
  df.loc[fault_idx, "power_watt"] += rng.uniform(80, 180, len(fault_idx))

  # Label
  df["status_label"] = "normal"
  df.loc[warning_idx, "status_label"] = "warning"
  df.loc[fault_idx, "status_label"] = "fault"
  df["is_anomaly"] = df["status_label"].apply(lambda x: 0 if x == "normal" else 1)

  df["co2_ppm"] = df["co2_ppm"].clip(lower=350).round().astype(int)
  df["temperature_c"] = df["temperature_c"].round(2)
  df["humidity_pct"] = df["humidity_pct"].round(2)
  df["power_watt"] = df["power_watt"].round(2)

  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Dataset disimpan ke: {OUTPUT_PATH} ({len(df)} baris)")
  print("\n[INFO] Distribusi label:")
  print(df["status_label"].value_counts())
  print("\n[INFO] Distribusi is_anomaly:")
  print(df["is_anomaly"].value_counts())
  print(df.head())


if __name__ == "__main__":
  main()
