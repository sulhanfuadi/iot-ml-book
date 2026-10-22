from pathlib import Path
import pandas as pd
import numpy as np
INPUT_PATH = Path("data/synthetic/energy_30days.csv")
OUTPUT_DIR = Path("data/processed/regression_energy")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# 1. Baca data
df = pd.read_csv(INPUT_PATH)
# 2. Parse waktu dan urutkan
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
# 3. Target satu langkah ke depan
df["target_power_next_1step"] = df["power_watt"].shift(-1)
# 4. Fitur waktu
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
# Encoding siklik jam
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
# 5. Fitur lag
df["power_lag_1"] = df["power_watt"].shift(1)
df["power_lag_2"] = df["power_watt"].shift(2)
df["power_lag_6"] = df["power_watt"].shift(6)          # 1 jam jika 10 menit
# 6. Fitur rolling
df["power_ma_3"] = df["power_watt"].rolling(3).mean()
df["power_ma_6"] = df["power_watt"].rolling(6).mean()
df["power_std_6"] = df["power_watt"].rolling(6).std()
# 7. Difference
df["power_diff_1"] = df["power_watt"].diff(1)
df["power_diff_6"] = df["power_watt"].diff(6)
# 8. Hapus NaN
df = df.dropna().reset_index(drop=True)
# 9. Pilih fitur
feature_cols = [
    "power_watt",
    "hour", "day_of_week", "is_weekend",
    "hour_sin", "hour_cos",
    "power_lag_1", "power_lag_2", "power_lag_6",
    "power_ma_3", "power_ma_6", "power_std_6",
    "power_diff_1", "power_diff_6"
]
target_col = "target_power_next_1step"
# 10. Split time-aware
n = len(df)
train_end = int(n * 0.70)
val_end = int(n * 0.85)
train_df = df.iloc[:train_end].copy()
val_df = df.iloc[train_end:val_end].copy()
test_df = df.iloc[val_end:].copy()
# 11. Simpan
df.to_csv(OUTPUT_DIR / "full_dataset.csv", index=False)
train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
val_df.to_csv(OUTPUT_DIR / "validation.csv", index=False)
test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)
train_df[feature_cols].to_csv(OUTPUT_DIR / "X_train.csv", index=False)
train_df[[target_col]].to_csv(OUTPUT_DIR / "y_train.csv", index=False)
val_df[feature_cols].to_csv(OUTPUT_DIR / "X_val.csv", index=False)
val_df[[target_col]].to_csv(OUTPUT_DIR / "y_val.csv", index=False)
test_df[feature_cols].to_csv(OUTPUT_DIR / "X_test.csv", index=False)
test_df[[target_col]].to_csv(OUTPUT_DIR / "y_test.csv", index=False)
print("=== Ringkasan Dataset Regresi ===")
print(f"Total data : {len(df)}")
print(f"Train      : {len(train_df)}")
print(f"Validation : {len(val_df)}")
print(f"Test       : {len(test_df)}")
print("\nPreview:")
print(df[["timestamp", "power_watt", "target_power_next_1step"]].head(10))
print("\nFile disimpan di:", OUTPUT_DIR)
