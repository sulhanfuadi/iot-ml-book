"""
Hands-on 21 (Bab 9): DBSCAN untuk Pola Ruangan dan Deteksi Noise
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/reports/room_dbscan_cluster.csv, outputs/figures/room_dbscan_scatter.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("outputs")


def main():
  (OUTPUT_DIR / "reports").mkdir(parents=True, exist_ok=True)
  (OUTPUT_DIR / "figures").mkdir(parents=True, exist_ok=True)

  # 1. Baca data
  df = pd.read_csv(INPUT_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])

  # 2. Pilih fitur
  X = df[["temperature_c", "humidity_pct"]].copy()

  # 3. Scaling
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)

  # 4. DBSCAN (label -1 = noise / titik menyendiri)
  dbscan = DBSCAN(eps=0.35, min_samples=10)
  df["cluster_dbscan"] = dbscan.fit_predict(X_scaled)

  print("=== Hasil DBSCAN ===")
  print(df["cluster_dbscan"].value_counts().sort_index().to_string())

  n_noise = int((df["cluster_dbscan"] == -1).sum())
  print(f"\n[INFO] Titik noise (label -1): {n_noise} baris")

  # 5. Simpan hasil
  df.to_csv(OUTPUT_DIR / "reports" / "room_dbscan_cluster.csv", index=False)
  print("[SUKSES] outputs/reports/room_dbscan_cluster.csv")

  # 6. Visualisasi
  plt.figure(figsize=(8, 6))
  plt.scatter(
      df["temperature_c"],
      df["humidity_pct"],
      c=df["cluster_dbscan"],
      s=10,
      cmap="viridis",
  )
  plt.title("DBSCAN: Suhu vs kelembaban")
  plt.xlabel("Temperature (C)")
  plt.ylabel("Humidity (%)")
  plt.colorbar(label="Cluster")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "figures" / "room_dbscan_scatter.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_dbscan_scatter.png")


if __name__ == "__main__":
  main()
