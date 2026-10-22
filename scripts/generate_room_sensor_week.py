"""
Hands-on 6: Generator Dataset Sintetis Sensor Ruangan 1 Minggu
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Menghasilkan data/raw/room_sensor_week.csv: dataset sintetis realistis
interval 10 menit selama 7 hari dengan pola harian (siang lebih panas,
lebih ramai, dan daya lebih tinggi).
"""

from datetime import datetime, timedelta
from pathlib import Path
import math
import random

import pandas as pd

OUTPUT_PATH = Path("data/raw/room_sensor_week.csv")
DEVICE_ID = "room01"
START = datetime(2026, 1, 1, 0, 0, 0)
DAYS = 7
INTERVAL_MINUTES = 10
SEED = 42


def generate():
  random.seed(SEED)
  rows = []
  t = START
  for _ in range(int(DAYS * 24 * 60 / INTERVAL_MINUTES)):
    hour = t.hour + t.minute / 60.0
    # Pola harian: suhu puncak siang, CO2 dan daya mengikuti jam sibuk.
    temp = (
        26.0
        + 3.0 * math.sin((hour - 9) / 24 * 2 * math.pi)
        + random.uniform(-0.4, 0.4)
    )
    occupancy = max(
        0.0, math.sin((hour - 7) / 12 * math.pi) if 7 <= hour <= 19 else 0.0
    )
    co2 = 450 + 450 * occupancy + random.uniform(-20, 20)
    humidity = 62 - 8 * math.sin((hour - 9) / 24 * 2 * math.pi) + random.uniform(-2, 2)
    power = 90 + 70 * occupancy + random.uniform(-8, 8)
    rows.append({
        "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": DEVICE_ID,
        "temperature_c": round(temp, 2),
        "humidity_pct": round(humidity, 2),
        "co2_ppm": int(co2),
        "power_watt": round(power, 2),
    })
    t += timedelta(minutes=INTERVAL_MINUTES)
  return pd.DataFrame(rows)


def main():
  df = generate()
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Dataset tersimpan: {OUTPUT_PATH} ({df.shape[0]} baris)")
  print(df.head(4).to_string(index=False))


if __name__ == "__main__":
  main()
