"""
Hands-on 8: Generator Dataset Sensor dengan Anomali
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Menghasilkan data/raw/room_sensor_anomaly.csv: satu hari data ruangan
interval 10 menit dengan beberapa titik anomali yang disuntikkan
(suhu/CO2/daya melonjak), sesuai pola contoh buku.
"""

from datetime import datetime, timedelta
from pathlib import Path
import math
import random

import pandas as pd

OUTPUT_PATH = Path("data/raw/room_sensor_anomaly.csv")
SEED = 8


def main():
  random.seed(SEED)
  rows = []
  t = datetime(2026, 1, 1, 0, 0, 0)
  for _ in range(144):  # 24 jam x 6 sampel per jam
    hour = t.hour + t.minute / 60.0
    temp = 26.0 + 3.0 * math.sin((hour - 9) / 24 * 2 * math.pi) + random.uniform(-0.3, 0.3)
    occupancy = max(0.0, math.sin((hour - 7) / 12 * math.pi) if 7 <= hour <= 19 else 0.0)
    co2 = 450 + 420 * occupancy + random.uniform(-15, 15)
    humidity = 62 - 8 * math.sin((hour - 9) / 24 * 2 * math.pi) + random.uniform(-1.5, 1.5)
    power = 90 + 65 * occupancy + random.uniform(-6, 6)
    rows.append({
        "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": "room01",
        "temperature_c": round(temp, 2),
        "humidity_pct": round(humidity, 2),
        "co2_ppm": int(co2),
        "power_watt": round(power, 2),
    })
    t += timedelta(minutes=10)

  df = pd.DataFrame(rows)

  # Suntikkan anomali: lonjakan gabungan, lonjakan CO2 saja, lonjakan daya saja.
  anomalies = {
      "2026-01-01 09:30:00": {"temperature_c": 45.0, "co2_ppm": 1500, "power_watt": 300.0},
      "2026-01-01 13:00:00": {"co2_ppm": 1600},
      "2026-01-01 15:20:00": {"power_watt": 320.0},
  }
  for ts, changes in anomalies.items():
    for col, val in changes.items():
      df.loc[df["timestamp"] == ts, col] = val

  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Dataset anomali tersimpan: {OUTPUT_PATH} ({len(df)} baris)")
  print(f"[INFO] Titik anomali disuntikkan pada: {list(anomalies.keys())}")


if __name__ == "__main__":
  main()
