from pathlib import Path
import numpy as np
import pandas as pd
OUTPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
# Reproducible
rng = np.random.default_rng(42)
# 30 hari, interval 10 menit
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    end="2026-01-30 23:50:00",
    freq="10min"
)
hours = timestamps.hour + timestamps.minute / 60.0
day_of_week = timestamps.dayofweek # 0=Senin ... 6=Minggu
# Pola suhu harian
daily_temp_cycle = 3.5 * np.sin((hours - 6) / 24 * 2 * np.pi)
# Sedikit beda antara hari kerja dan akhir pekan
workday_boost = np.where(day_of_week < 5, 0.8, 0.2)
# Drift kecil antar-hari, misalnya efek cuaca/lingkungan
slow_drift = np.linspace(0, 1.0, len(timestamps))
# Noise
temp_noise = rng.normal(0, 0.35, len(timestamps))
temperature = 24.0 + daily_temp_cycle + workday_boost + slow_drift + temp_noise
# kelembaban cenderung berlawanan arah dengan suhu
humidity_noise = rng.normal(0, 1.8, len(timestamps))
humidity = 68.0 - 0.9 * daily_temp_cycle - 0.3 * workday_boost - 0.2 * slow_drift + humidity_noise
# Batasi rentang agar realistis
humidity = np.clip(humidity, 35, 85)
df = pd.DataFrame({
    "timestamp": timestamps,
    "device_id": "room01",
    "temperature_c": np.round(temperature, 2),
    "humidity_pct": np.round(humidity, 2)
})
df.to_csv(OUTPUT_PATH, index=False)
print(f"Dataset disimpan ke: {OUTPUT_PATH}")
print(df.head())
print(df.tail())
print(df.describe())
