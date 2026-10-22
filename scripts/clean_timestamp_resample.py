"""
Hands-on 7: Membersihkan Timestamp, Resampling, dan Imputasi Sederhana
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Alur:
  1. Parse timestamp (errors="coerce")
  2. Hapus timestamp invalid
  3. Urutkan waktu
  4. Hapus duplikasi waktu (keep="last")
  5. Set index waktu
  6. Resample ke interval 10 menit
  7. Imputasi: forward fill (demo) dan interpolasi linier (hasil akhir)
  8. Simpan data bersih ke data/processed/room_sensor_clean.csv
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/room_sensor_dirty.csv")
OUTPUT_PATH = Path("data/processed/room_sensor_clean.csv")
NUMERIC_COLS = ["temperature_c", "humidity_pct", "co2_ppm", "power_watt"]


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

  df = pd.read_csv(DATA_PATH)
  print(f"[INFO] Baris awal: {len(df)}")

  # 1. Parse timestamp
  df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

  # 2. Hapus timestamp invalid
  n_invalid = df["timestamp"].isna().sum()
  df = df.dropna(subset=["timestamp"])
  print(f"[INFO] Timestamp invalid dibuang: {n_invalid}")

  # 3. Urutkan waktu
  df = df.sort_values("timestamp")

  # 4. Hapus duplikasi waktu
  n_dup = df.duplicated(subset=["timestamp"]).sum()
  df = df.drop_duplicates(subset=["timestamp"], keep="last")
  print(f"[INFO] Duplikasi timestamp dibuang: {n_dup}")

  # 5. Set index waktu
  df = df.set_index("timestamp")

  # 6. Resample ke 10 menit
  df_resampled = df.resample("10min").mean(numeric_only=True)
  df_resampled["device_id"] = "room01"
  n_missing = df_resampled[NUMERIC_COLS].isna().any(axis=1).sum()
  print(f"[INFO] Baris dengan nilai hilang setelah resample: {n_missing}")
  print("\n=== Data setelah resampling 10 menit ===")
  print(df_resampled.head(12))

  # 7.1 Forward fill (demo)
  df_ffill = df_resampled.copy()
  df_ffill[NUMERIC_COLS] = df_ffill[NUMERIC_COLS].ffill()
  print("\n=== Setelah forward fill ===")
  print(df_ffill.head(12))

  # 7.2 Interpolasi linier (hasil akhir)
  df_interp = df_resampled.copy()
  df_interp[NUMERIC_COLS] = df_interp[NUMERIC_COLS].interpolate(method="linear")
  print("\n=== Setelah interpolasi linier ===")
  print(df_interp.head(12))

  # 8. Simpan data bersih
  df_interp.to_csv(OUTPUT_PATH)
  sisa_nan = df_interp[NUMERIC_COLS].isna().sum().sum()
  print(f"\n[SUKSES] Data bersih disimpan ke: {OUTPUT_PATH} ({len(df_interp)} baris)")
  print(f"[INFO] Sisa nilai hilang: {sisa_nan}")


if __name__ == "__main__":
  main()
