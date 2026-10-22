from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/vibration_machine_synthetic.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

n = 1000
t = np.arange(n)

# Sinyal normal
normal_signal = 0.8 * np.sin(2 * np.pi * 0.03 * t) + np.random.normal(0, 0.1, n)

# Sinyal fault
fault_signal = 1.6 * np.sin(2 * np.pi * 0.03 * t) + np.random.normal(0, 0.25, n)

df_normal = pd.DataFrame({
    "sample_id": range(n),
    "machine_id": "motor01",
    "vibration": np.round(normal_signal, 4),
    "label": "normal"
})

df_fault = pd.DataFrame({
    "sample_id": range(n, 2*n),
    "machine_id": "motor01",
    "vibration": np.round(fault_signal, 4),
    "label": "fault"
})

df = pd.concat([df_normal, df_fault], ignore_index=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Data getaran sintetik disimpan ke: {OUTPUT_PATH}")
print(df.head())
print(df.tail())
