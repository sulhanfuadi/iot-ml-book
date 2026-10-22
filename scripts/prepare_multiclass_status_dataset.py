"""
Hands-on 24: Menyiapkan Dataset Multi-Kelas Status Perangkat
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Label: normal / warning / fault. Fitur waktu + lag + rolling.
Split time-aware 70/15/15.
Input : data/synthetic/room_classification_dataset.csv
Output: data/processed/classification_status/*.csv
"""

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/synthetic/room_classification_dataset.csv")
OUTPUT_DIR = Path("data/processed/classification_status")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  df = pd.read_csv(INPUT_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").reset_index(drop=True)

  # Pastikan label ada
  if "status_label" not in df.columns:
    def make_label(row):
      if (
          row["temperature_c"] > 33
          or row["co2_ppm"] > 1400
          or row["power_watt"] > 280
      ):
        return "fault"
      elif (
          row["temperature_c"] > 29
          or row["co2_ppm"] > 900
          or row["power_watt"] > 200
      ):
        return "warning"
      return "normal"

    df["status_label"] = df.apply(make_label, axis=1)

  # Fitur waktu
  df["hour"] = df["timestamp"].dt.hour
  df["day_of_week"] = df["timestamp"].dt.dayofweek
  df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

  # Lag dan rolling sederhana
  df["temp_lag_1"] = df["temperature_c"].shift(1)
  df["co2_lag_1"] = df["co2_ppm"].shift(1)
  df["power_lag_1"] = df["power_watt"].shift(1)
  df["temp_ma_3"] = df["temperature_c"].rolling(3).mean()
  df["co2_ma_3"] = df["co2_ppm"].rolling(3).mean()
  df["power_ma_3"] = df["power_watt"].rolling(3).mean()

  df = df.dropna().reset_index(drop=True)

  feature_cols = [
      "temperature_c", "humidity_pct", "co2_ppm", "power_watt",
      "hour", "day_of_week", "is_weekend",
      "temp_lag_1", "co2_lag_1", "power_lag_1",
      "temp_ma_3", "co2_ma_3", "power_ma_3",
  ]

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
  train_df[["status_label"]].to_csv(OUTPUT_DIR / "y_train.csv", index=False)
  val_df[feature_cols].to_csv(OUTPUT_DIR / "X_val.csv", index=False)
  val_df[["status_label"]].to_csv(OUTPUT_DIR / "y_val.csv", index=False)
  test_df[feature_cols].to_csv(OUTPUT_DIR / "X_test.csv", index=False)
  test_df[["status_label"]].to_csv(OUTPUT_DIR / "y_test.csv", index=False)

  print("[INFO] Distribusi label:")
  print(df["status_label"].value_counts())
  print(f"[SUKSES] File disimpan di: {OUTPUT_DIR}")


if __name__ == "__main__":
  main()
