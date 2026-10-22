"""
Hands-on 16: PCA untuk Merangkum Beberapa Sensor
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Standarisasi fitur time-series lalu reduksi ke 3 komponen utama.
Input : data/processed/room_30days_features.csv
Output: data/processed/room_30days_pca.csv
"""

from pathlib import Path

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

INPUT_PATH = Path("data/processed/room_30days_features.csv")
OUTPUT_PATH = Path("data/processed/room_30days_pca.csv")

FEATURE_COLS = [
  "temperature_c",
  "humidity_pct",
  "temp_lag_1",
  "temp_lag_6",
  "hum_lag_1",
  "hum_lag_6",
  "temp_diff_1",
  "temp_diff_6",
  "hum_diff_1",
  "temp_ma_3",
  "temp_ma_6",
  "hum_ma_3",
  "temp_roll_std_6",
  "temp_roll_min_6",
  "temp_roll_max_6",
  "hum_roll_std_6",
  "hum_roll_min_6",
  "hum_roll_max_6",
  "comfort_index_simple",
  "hour_sin",
  "hour_cos",
  "is_weekend",
]


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  X = df[FEATURE_COLS].copy()

  # Standarisasi (PCA sensitif terhadap skala)
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)

  # PCA jadi 3 komponen
  pca = PCA(n_components=3)
  X_pca = pca.fit_transform(X_scaled)

  pca_df = pd.DataFrame(X_pca, columns=["pc1", "pc2", "pc3"])
  result_df = pd.concat(
      [df[["timestamp", "device_id"]].reset_index(drop=True), pca_df], axis=1
  )
  result_df.to_csv(OUTPUT_PATH, index=False)

  print(f"[SUKSES] Hasil PCA disimpan ke: {OUTPUT_PATH} ({len(result_df)} baris)")
  print(result_df.head())
  print("\n[INFO] Explained variance ratio:")
  for i, ratio in enumerate(pca.explained_variance_ratio_, start=1):
    print(f"  PC{i}: {ratio:.4f}")
  print(f"\n[INFO] Total varian 3 komponen: {pca.explained_variance_ratio_.sum():.4f}")


if __name__ == "__main__":
  main()
