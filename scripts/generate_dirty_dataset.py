"""
Hands-on 7: Generator Dataset Kotor (untuk latihan cleaning)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Menghasilkan data/raw/room_sensor_dirty.csv dari dataset bersih 1 minggu
dengan masalah khas data IoT:
  - timestamp tidak valid / kosong,
  - baris duplikat,
  - nilai hilang (NaN),
  - interval waktu tidak konsisten (baris terhapus membentuk gap).
"""

from pathlib import Path
import random

import numpy as np
import pandas as pd

SOURCE_PATH = Path("data/raw/room_sensor_week.csv")
OUTPUT_PATH = Path("data/raw/room_sensor_dirty.csv")
SEED = 7


def main():
  random.seed(SEED)
  rng = np.random.default_rng(SEED)

  df = pd.read_csv(SOURCE_PATH)
  n = len(df)
  issues = {"invalid_timestamp": 0, "duplikat": 0, "nilai_hilang": 0, "baris_gap": 0}

  # 1. Timestamp tidak valid
  idx_bad_ts = rng.choice(n, size=20, replace=False)
  df.loc[idx_bad_ts[:10], "timestamp"] = "bukan-waktu"
  df.loc[idx_bad_ts[10:], "timestamp"] = ""
  issues["invalid_timestamp"] = 20

  # 2. Duplikasi baris
  dup_rows = df.sample(n=15, random_state=SEED)
  df = pd.concat([df, dup_rows], ignore_index=True)
  issues["duplikat"] = 15

  # 3. Nilai hilang pada kolom numerik (sekitar 3%)
  num_cols = ["temperature_c", "humidity_pct", "co2_ppm", "power_watt"]
  for col in num_cols:
    idx_nan = rng.choice(len(df), size=int(0.03 * len(df)), replace=False)
    df.loc[idx_nan, col] = np.nan
    issues["nilai_hilang"] += len(idx_nan)

  # 4. Gap: hapus 2% baris dengan timestamp valid agar interval tidak konsisten
  mask_valid = df["timestamp"].str.match(r"^\d{4}-\d{2}-\d{2}", na=False)
  idx_gap = rng.choice(df[mask_valid].index, size=int(0.02 * mask_valid.sum()), replace=False)
  df = df.drop(index=idx_gap)
  issues["baris_gap"] = len(idx_gap)

  df = df.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(OUTPUT_PATH, index=False)

  print(f"[SUKSES] Dataset kotor tersimpan: {OUTPUT_PATH} ({len(df)} baris)")
  for k, v in issues.items():
    print(f"[INFO] Masalah disuntikkan - {k}: {v}")


if __name__ == "__main__":
  main()
