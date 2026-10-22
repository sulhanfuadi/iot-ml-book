"""
Hands-on 24 (Bab 10): Menyiapkan Dataset Forecasting Suhu Ruang
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: data/processed/forecast_room/ (train/validation/test + X/y splits)
"""

from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("data/processed/forecast_room")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").reset_index(drop=True)

  # Target 1 langkah ke depan (10 menit)
  df["target_temp_next_1step"] = df["temperature_c"].shift(-1)

  # Fitur waktu
  df["hour"] = df["timestamp"].dt.hour
  df["day_of_week"] = df["timestamp"].dt.dayofweek
  df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

  # Encoding siklik jam
  df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
  df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

  # Lag features
  df["temp_lag_1"] = df["temperature_c"].shift(1)
  df["temp_lag_2"] = df["temperature_c"].shift(2)
  df["temp_lag_6"] = df["temperature_c"].shift(6)  # 1 jam
  df["hum_lag_1"] = df["humidity_pct"].shift(1)

  # Rolling features
  df["temp_ma_3"] = df["temperature_c"].rolling(3).mean()
  df["temp_ma_6"] = df["temperature_c"].rolling(6).mean()
  df["temp_std_6"] = df["temperature_c"].rolling(6).std()

  # Difference
  df["temp_diff_1"] = df["temperature_c"].diff(1)
  df["temp_diff_6"] = df["temperature_c"].diff(6)

  # Hapus NaN
  df = df.dropna().reset_index(drop=True)

  feature_cols = [
      "temperature_c", "humidity_pct",
      "hour", "day_of_week", "is_weekend",
      "hour_sin", "hour_cos",
      "temp_lag_1", "temp_lag_2", "temp_lag_6",
      "hum_lag_1",
      "temp_ma_3", "temp_ma_6", "temp_std_6",
      "temp_diff_1", "temp_diff_6",
  ]
  target_col = "target_temp_next_1step"

  # Split time-aware: 70% train, 15% validation, 15% test
  n = len(df)
  train_end = int(n * 0.70)
  val_end = int(n * 0.85)
  train_df = df.iloc[:train_end].copy()
  val_df = df.iloc[train_end:val_end].copy()
  test_df = df.iloc[val_end:].copy()

  train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
  val_df.to_csv(OUTPUT_DIR / "validation.csv", index=False)
  test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)

  train_df[feature_cols].to_csv(OUTPUT_DIR / "X_train.csv", index=False)
  train_df[[target_col]].to_csv(OUTPUT_DIR / "y_train.csv", index=False)
  val_df[feature_cols].to_csv(OUTPUT_DIR / "X_val.csv", index=False)
  val_df[[target_col]].to_csv(OUTPUT_DIR / "y_val.csv", index=False)
  test_df[feature_cols].to_csv(OUTPUT_DIR / "X_test.csv", index=False)
  test_df[[target_col]].to_csv(OUTPUT_DIR / "y_test.csv", index=False)

  print("[SUKSES] Dataset forecasting suhu siap digunakan.")
  print(f"Train: {len(train_df)}, Validation: {len(val_df)}, Test: {len(test_df)}")
  print("File disimpan di:", OUTPUT_DIR)


if __name__ == "__main__":
  main()
