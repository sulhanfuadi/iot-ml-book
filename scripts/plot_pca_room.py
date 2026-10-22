"""
Hands-on 16: Visualisasi PCA 2 Dimensi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("data/processed/room_30days_pca.csv")
FEATURES_PATH = Path("data/processed/room_30days_features.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)
  features = pd.read_csv(FEATURES_PATH)

  plt.figure(figsize=(8, 6))
  sc = plt.scatter(
      df["pc1"], df["pc2"], s=8,
      c=features["temperature_c"], cmap="coolwarm",
  )
  plt.colorbar(sc, label="Suhu (C)")
  plt.title("Visualisasi PCA: PC1 vs PC2 (warna = suhu)")
  plt.xlabel("PC1")
  plt.ylabel("PC2")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_pca_scatter.png")
  plt.close()
  print("[SUKSES] outputs/figures/room_pca_scatter.png")


if __name__ == "__main__":
  main()
