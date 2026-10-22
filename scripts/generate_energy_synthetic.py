from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/energy_daily_synthetic.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    end="2026-01-01 23:50:00",
    freq="10min"
)

power = []

for ts in timestamps:
    hour = ts.hour

    if 0 <= hour < 6:
        base = 120
    elif 6 <= hour < 8:
        base = 180
    elif 8 <= hour < 12:
        base = 350
    elif 12 <= hour < 14:
        base = 450
    elif 14 <= hour < 18:
        base = 320
    else:
        base = 170

    value = base + np.random.normal(0, 15)
    power.append(value)

df = pd.DataFrame({
    "timestamp": timestamps,
    "device_id": "lab-energy-01",
    "power_watt": np.round(power, 2)
})

df.to_csv(OUTPUT_PATH, index=False)
print(f"Data energi sintetik disimpan ke: {OUTPUT_PATH}")
print(df.head())
