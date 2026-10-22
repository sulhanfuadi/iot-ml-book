"""
Hands-on 21 (Bab 9): K-Means untuk Pola Ruangan dari Suhu-Kelembaban
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/reports/room_kmeans_cluster.csv, outputs/figures/room_kmeans_scatter.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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

  # 4. Coba beberapa nilai K
  results = []
  for k in range(2, 6):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    results.append((k, score))

  print("=== Silhouette Score untuk beberapa K ===")
  for k, score in results:
    print(f"K={k}, silhouette={score:.4f}")

  # 5. Pilih K = 3
  best_k = 3
  kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
  df["cluster_kmeans"] = kmeans.fit_predict(X_scaled)

  print("\nJumlah data per cluster:")
  print(df["cluster_kmeans"].value_counts().sort_index().to_string())

  # Ringkasan karakter tiap cluster
  summary = df.groupby("cluster_kmeans")[["temperature_c", "humidity_pct"]].mean().round(2)
  print("\nRata-rata per cluster:")
  print(summary.to_string())

  # 6. Simpan hasil
  df.to_csv(OUTPUT_DIR / "reports" / "room_kmeans_cluster.csv", index=False)
  print("\n[SUKSES] outputs/reports/room_kmeans_cluster.csv")

  # 7. Visualisasi
  plt.figure(figsize=(8, 6))
  plt.scatter(
      df["temperature_c"],
      df["humidity_pct"],
      c=df["cluster_kmeans"],
      s=10,
      cmap="viridis",
  )
  plt.title("K-Means Clustering: Suhu vs Kelembaban")
  plt.xlabel("Temperature (C)")
  plt.ylabel("Humidity (%)")
  plt.colorbar(label="Cluster")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "figures" / "room_kmeans_scatter.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_kmeans_scatter.png")


if __name__ == "__main__":
  main()
