from pathlib import Path
import numpy as np
import pandas as pd
OUTPUT_PATH = Path("data/synthetic/vibration_fault_injection.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)
n = 3000
t = np.arange(n)
# Sinyal dasar mesin normal
base_freq = 0.03
normal_signal = 0.8 * np.sin(2 * np.pi * base_freq * t) + rng.normal(0, 0.08, n)
# Buat salinan untuk fault
fault_signal = normal_signal.copy()
# Fault 1: amplitudo meningkat
fault_signal[1000:2000] += 0.9 * np.sin(2 * np.pi * base_freq * t[1000:2000])
# Fault 2: noise bertambah
fault_signal[1500:2300] += rng.normal(0, 0.18, 800)
# Fault 3: spike sesaat
spike_idx = rng.choice(np.arange(1800, 2500), size=15, replace=False)
fault_signal[spike_idx] += rng.uniform(1.0, 2.0, len(spike_idx))
df = pd.DataFrame({
    "sample_id": np.arange(n),
    "machine_id": "motor01",
    "vibration": np.round(fault_signal, 5)
})
# Label sintetis
df["status_label"] = "normal"
df.loc[1000:2499, "status_label"] = "fault"
df.to_csv(OUTPUT_PATH, index=False)
print(f"Dataset getaran disimpan ke: {OUTPUT_PATH}")
print(df.head())
print(df.iloc[995:1005])
print(df.iloc[1795:1805])
