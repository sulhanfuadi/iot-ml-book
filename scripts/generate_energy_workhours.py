"""
Hands-on 10: Generate Data Konsumsi Energi Berbasis Jam Kerja
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Aturan sintetis: malam rendah, pagi naik, jam kerja tinggi, makan siang
sangat tinggi, sore menurun, akhir pekan lebih rendah.
Output: data/synthetic/energy_30days.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/energy_30days.csv")


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  rng = np.random.default_rng(123)

  timestamps = pd.date_range(
      start="2026-01-01 00:00:00",
      end="2026-01-30 23:50:00",
      freq="10min",
  )

  records = []
  for ts in timestamps:
    hour = ts.hour
    minute = ts.minute
    dow = ts.dayofweek  # 0-4 kerja, 5-6 akhir pekan
    is_weekend = dow >= 5

    if is_weekend:
      if 0 <= hour < 7:
        base = 90
      elif 7 <= hour < 12:
        base = 130
      elif 12 <= hour < 18:
        base = 160
      else:
        base = 110
    else:
      if 0 <= hour < 6:
        base = 110
      elif 6 <= hour < 8:
        base = 170
      elif 8 <= hour < 12:
        base = 320
      elif 12 <= hour < 14:
        base = 430
      elif 14 <= hour < 18:
        base = 300
      elif 18 <= hour < 21:
        base = 180
      else:
        base = 130

    sub_cycle = 8 * np.sin((minute / 60.0) * 2 * np.pi)
    day_idx = (ts.date() - timestamps[0].date()).days
    drift = day_idx * 0.8
    noise = rng.normal(0, 12)
    power_watt = base + sub_cycle + drift + noise

    records.append({
        "timestamp": ts,
        "device_id": "energy-lab01",
        "power_watt": round(power_watt, 2),
    })

  df = pd.DataFrame(records)
  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Dataset energi disimpan ke: {OUTPUT_PATH} ({len(df)} baris)")
  print(df.head())
  print(df.describe())


if __name__ == "__main__":
  main()
