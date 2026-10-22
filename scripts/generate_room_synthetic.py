from pathlib import Path
import numpy as np
import pandas as pd
OUTPUT_PATH = Path("data/synthetic/room_daily_synthetic.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
# Waktu 1 hari, interval 10 menit
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    end="2026-01-01 23:50:00",
    freq="10min"
)
hours = timestamps.hour + timestamps.minute / 60.0
# Pola suhu harian: rendah malam, naik siang
temperature = 24 + 4 * np.sin((hours - 6) / 24 * 2 * np.pi)
temperature += np.random.normal(0, 0.3, len(timestamps))
# kelembaban berlawanan dengan suhu
humidity = 70 - 10 * np.sin((hours - 6) / 24 * 2 * np.pi)
humidity += np.random.normal(0, 1.5, len(timestamps))
df = pd.DataFrame({
    "timestamp": timestamps,
    "device_id": "room01",
    "temperature_c": np.round(temperature, 2),
    "humidity_pct": np.round(humidity, 2)
})
df.to_csv(OUTPUT_PATH, index=False)
print(f"Data sintetik disimpan ke: {OUTPUT_PATH}")
print(df.head())
