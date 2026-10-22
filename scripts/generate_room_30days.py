"""
Hands-on 9: Generate Data Suhu-Kelembaban Ruangan 30 Hari
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Dataset sintetis 30 hari interval 10 menit dengan pola harian,
perbedaan hari kerja/akhir pekan, drift perlahan, dan noise.
Output: data/synthetic/room_30days.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/room_30days.csv")


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  rng = np.random.default_rng(42)

  timestamps = pd.date_range(
      start="2026-01-01 00:00:00",
      end="2026-01-30 23:50:00",
      freq="10min",
  )
  hours = timestamps.hour + timestamps.minute / 60.0
  day_of_week = timestamps.dayofweek  # 0=Senin ... 6=Minggu

  daily_temp_cycle = 3.5 * np.sin((hours - 6) / 24 * 2 * np.pi)
  workday_boost = np.where(day_of_week < 5, 0.8, 0.2)
  slow_drift = np.linspace(0, 1.0, len(timestamps))
  temp_noise = rng.normal(0, 0.35, len(timestamps))
  temperature = 24.0 + daily_temp_cycle + workday_boost + slow_drift + temp_noise

  humidity_noise = rng.normal(0, 1.8, len(timestamps))
  humidity = (
      68.0 - 0.9 * daily_temp_cycle - 0.3 * workday_boost - 0.2 * slow_drift
      + humidity_noise
  )
  humidity = np.clip(humidity, 35, 85)

  df = pd.DataFrame({
      "timestamp": timestamps,
      "device_id": "room01",
      "temperature_c": np.round(temperature, 2),
      "humidity_pct": np.round(humidity, 2),
  })
  df.to_csv(OUTPUT_PATH, index=False)

  print(f"[SUKSES] Dataset disimpan ke: {OUTPUT_PATH} ({len(df)} baris)")
  print(df.head())
  print(df.tail())
  print(df.describe())


if __name__ == "__main__":
  main()
