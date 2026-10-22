from pathlib import Path
import numpy as np
import pandas as pd
OUTPUT_PATH = Path("data/synthetic/current_sensor_anomaly.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(42)
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=500,
    freq="10min"
)
current_amp = rng.normal(loc=6.0, scale=0.5, size=len(timestamps))
voltage = rng.normal(loc=220.0, scale=3.0, size=len(timestamps))
power_watt = current_amp * voltage
df = pd.DataFrame({
    "timestamp": timestamps,
    "device_id": "meter01",
    "current_amp": np.round(current_amp, 3),
    "voltage": np.round(voltage, 2),
    "power_watt": np.round(power_watt, 2)
})
# Inject anomali
anomaly_idx = rng.choice(df.index, size=15, replace=False)
df.loc[anomaly_idx, "current_amp"] += rng.uniform(4, 8, len(anomaly_idx))
df.loc[anomaly_idx, "power_watt"] = (
    df.loc[anomaly_idx, "current_amp"] * df.loc[anomaly_idx, "voltage"]
)
df["ground_truth_anomaly"] = 0
df.loc[anomaly_idx, "ground_truth_anomaly"] = 1
df.to_csv(OUTPUT_PATH, index=False)
print("Dataset arus listrik disimpan ke:", OUTPUT_PATH)
print(df.head())
print("Jumlah anomali buatan:", df["ground_truth_anomaly"].sum())
