from pathlib import Path
import numpy as np
import pandas as pd
INPUT_PATH = Path("data/synthetic/room_daily_synthetic.csv")
OUTPUT_PATH = Path("data/synthetic/room_daily_synthetic_corrupted.csv")
df = pd.read_csv(INPUT_PATH)
# 1. Missing value acak
missing_idx = np.random.choice(df.index, size=8, replace=False)
df.loc[missing_idx, "temperature_c"] = np.nan
# 2. Drift bertahap pada suhu
df["temperature_c"] = df["temperature_c"] + np.linspace(0, 1.2, len(df))
# 3. Outlier buatan
outlier_idx = np.random.choice(df.index, size=3, replace=False)
df.loc[outlier_idx, "temperature_c"] = df.loc[outlier_idx, "temperature_c"] + 8
df.to_csv(OUTPUT_PATH, index=False)
print(f"Data dengan missing value, drift, dan outlier disimpan ke: {OUTPUT_PATH}")
print("Index missing:", missing_idx)
print("Index outlier:", outlier_idx)
