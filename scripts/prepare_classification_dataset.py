"""
Hands-on 20: Menyiapkan Dataset Klasifikasi Normal vs Abnormal
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Target biner dari is_anomaly, fitur waktu + lag + rolling + diff,
split time-aware 70/15/15 (train/val/test).
Input : data/synthetic/room_classification_dataset.csv
Output: data/processed/classification_room/*.csv
"""

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/synthetic/room_classification_dataset.csv")
OUTPUT_DIR = Path("data/processed/classification_room")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  # 1. Baca data
  df = pd.read_csv(INPUT_PATH)

  # 2. Parse timestamp dan urutkan
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").reset_index(drop=True)

  # 3. Target biner normal vs abnormal
  if "is_anomaly" in df.columns:
    df["target_abnormal"] = df["is_anomaly"].astype(int)
  else:
    df["target_abnormal"] = (
        (df["temperature_c"] > 30)
        | (df["co2_ppm"] > 1000)
        | (df["power_watt"] > 220)
    ).astype(int)

  # 4. Fitur waktu sederhana
  df["hour"] = df["timestamp"].dt.hour
  df["day_of_week"] = df["timestamp"].dt.dayofweek
  df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

  # 5. Fitur lag dan rolling sederhana
  df["temp_lag_1"] = df["temperature_c"].shift(1)
  df["hum_lag_1"] = df["humidity_pct"].shift(1)
  df["co2_lag_1"] = df["co2_ppm"].shift(1)
  df["power_lag_1"] = df["power_watt"].shift(1)
  df["temp_ma_3"] = df["temperature_c"].rolling(3).mean()
  df["co2_ma_3"] = df["co2_ppm"].rolling(3).mean()
  df["power_ma_3"] = df["power_watt"].rolling(3).mean()
  df["temp_diff_1"] = df["temperature_c"].diff(1)
  df["co2_diff_1"] = df["co2_ppm"].diff(1)
  df["power_diff_1"] = df["power_watt"].diff(1)

  # 6. Hapus baris awal NaN karena lag/rolling
  df = df.dropna().reset_index(drop=True)

  # 7. Kolom fitur dan target
  feature_cols = [
      "temperature_c", "humidity_pct", "co2_ppm", "power_watt",
      "hour", "day_of_week", "is_weekend",
      "temp_lag_1", "hum_lag_1", "co2_lag_1", "power_lag_1",
      "temp_ma_3", "co2_ma_3", "power_ma_3",
      "temp_diff_1", "co2_diff_1", "power_diff_1",
  ]
  target_col = "target_abnormal"

  # 8. Split time-aware: 70% train, 15% val, 15% test
  n = len(df)
  train_end = int(n * 0.70)
  val_end = int(n * 0.85)
  train_df = df.iloc[:train_end].copy()
  val_df = df.iloc[train_end:val_end].copy()
  test_df = df.iloc[val_end:].copy()

  train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
  val_df.to_csv(OUTPUT_DIR / "val.csv", index=False)
  test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)
  train_df[feature_cols].to_csv(OUTPUT_DIR / "X_train.csv", index=False)
  train_df[[target_col]].to_csv(OUTPUT_DIR / "y_train.csv", index=False)
  val_df[feature_cols].to_csv(OUTPUT_DIR / "X_val.csv", index=False)
  val_df[[target_col]].to_csv(OUTPUT_DIR / "y_val.csv", index=False)
  test_df[feature_cols].to_csv(OUTPUT_DIR / "X_test.csv", index=False)
  test_df[[target_col]].to_csv(OUTPUT_DIR / "y_test.csv", index=False)

  print("=== Ringkasan Dataset Klasifikasi ===")
  print(f"Total data      : {len(df)}")
  print(f"Train           : {len(train_df)}")
  print(f"Validation      : {len(val_df)}")
  print(f"Test            : {len(test_df)}")
  print("\n[INFO] Distribusi target keseluruhan:")
  print(df[target_col].value_counts())
  print("\n[INFO] Distribusi target train:")
  print(train_df[target_col].value_counts())
  print("\n[INFO] Distribusi target validation:")
  print(val_df[target_col].value_counts())
  print("\n[INFO] Distribusi target test:")
  print(test_df[target_col].value_counts())
  print(f"\n[SUKSES] File disimpan di: {OUTPUT_DIR}")


if __name__ == "__main__":
  main()
