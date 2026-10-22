"""
Hands-on 14: Fitur Time-Series dari Data Suhu/Kelembaban
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Fitur: waktu dasar, encoding siklik jam, lag, difference, moving average,
rolling statistics, dan sensor fusion sederhana (comfort index).
Input : data/synthetic/room_30days.csv
Output: data/processed/room_30days_features.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_PATH = Path("data/processed/room_30days_features.csv")


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

  # 1. Baca data
  df = pd.read_csv(INPUT_PATH)

  # 2. Konversi timestamp dan urutkan
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").set_index("timestamp")

  # 3. Fitur waktu dasar
  df["hour"] = df.index.hour
  df["day_of_week"] = df.index.dayofweek
  df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

  # 4. Encoding siklik untuk jam
  df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
  df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

  # 5. Lag features
  df["temp_lag_1"] = df["temperature_c"].shift(1)
  df["temp_lag_6"] = df["temperature_c"].shift(6)  # 1 jam jika interval 10 menit
  df["hum_lag_1"] = df["humidity_pct"].shift(1)
  df["hum_lag_6"] = df["humidity_pct"].shift(6)

  # 6. Difference
  df["temp_diff_1"] = df["temperature_c"].diff(1)
  df["temp_diff_6"] = df["temperature_c"].diff(6)
  df["hum_diff_1"] = df["humidity_pct"].diff(1)

  # 7. Moving average / rolling mean
  df["temp_ma_3"] = df["temperature_c"].rolling(window=3).mean()
  df["temp_ma_6"] = df["temperature_c"].rolling(window=6).mean()
  df["hum_ma_3"] = df["humidity_pct"].rolling(window=3).mean()

  # 8. Rolling statistics
  df["temp_roll_std_6"] = df["temperature_c"].rolling(window=6).std()
  df["temp_roll_min_6"] = df["temperature_c"].rolling(window=6).min()
  df["temp_roll_max_6"] = df["temperature_c"].rolling(window=6).max()
  df["hum_roll_std_6"] = df["humidity_pct"].rolling(window=6).std()
  df["hum_roll_min_6"] = df["humidity_pct"].rolling(window=6).min()
  df["hum_roll_max_6"] = df["humidity_pct"].rolling(window=6).max()

  # 9. Sensor fusion sederhana
  df["comfort_index_simple"] = (
      0.6 * df["temperature_c"] + 0.4 * (100 - df["humidity_pct"])
  )

  # 10. Hapus baris awal yang masih NaN karena lag/rolling
  df_clean = df.dropna().copy()

  # 11. Simpan
  df_clean.to_csv(OUTPUT_PATH)
  print(f"[SUKSES] Fitur time-series disimpan ke: {OUTPUT_PATH} ({len(df_clean)} baris)")
  print(df_clean.head())
  print("\n[INFO] Kolom fitur:")
  print(df_clean.columns.tolist())


if __name__ == "__main__":
  main()
