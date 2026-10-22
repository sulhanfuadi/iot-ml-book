from pathlib import Path
import numpy as np
import pandas as pd
OUTPUT = Path("data/synthetic/case_c_energy.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(123)
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    end="2026-01-30 23:50:00",
    freq="10min"
)
records = []
for ts in timestamps:
    hour = ts.hour
    dow = ts.dayofweek
    is_weekend = dow >= 5
    if is_weekend:
        base = 110 if hour < 7 else 150 if hour < 18 else 120
    else:
        if hour < 6:
            base = 110
        elif hour < 8:
            base = 180
        elif hour < 12:
            base = 320
        elif hour < 14:
            base = 430
        elif hour < 18:
            base = 300
        else:
            base = 160
    power = base + rng.normal(0, 12)
records.append({
    "timestamp": ts,
    "device_id": "energy01",
    "power_watt": round(power, 2)
})
df = pd.DataFrame(records)
# inject beberapa anomali
anomaly_idx = rng.choice(df.index, size=20, replace=False)
df["is_anomaly"] = 0
df.loc[anomaly_idx, "power_watt"] += rng.uniform(120, 220, len(anomaly_idx))
df.loc[anomaly_idx, "is_anomaly"] = 1
df.to_csv(OUTPUT, index=False)
print("Disimpan ke:", OUTPUT)
