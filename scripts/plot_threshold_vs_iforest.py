"""
Hands-on 23 (Bab 9): Visualisasi Perbandingan Threshold vs Isolation Forest
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/figures/threshold_vs_iforest_f1.png, threshold_vs_iforest_recall.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("outputs/reports/threshold_vs_iforest.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  plt.figure(figsize=(8, 5))
  plt.bar(df["method"], df["f1"], color=["steelblue", "seagreen"])
  plt.title("Perbandingan F1: Threshold vs Isolation Forest")
  plt.xlabel("Metode")
  plt.ylabel("F1 Score")
  plt.ylim(0, 1.05)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "threshold_vs_iforest_f1.png")
  plt.close()
  print("[SUKSES] outputs/figures/threshold_vs_iforest_f1.png")

  plt.figure(figsize=(8, 5))
  plt.bar(df["method"], df["recall"], color=["steelblue", "seagreen"])
  plt.title("Perbandingan Recall: Threshold vs Isolation Forest")
  plt.xlabel("Metode")
  plt.ylabel("Recall")
  plt.ylim(0, 1.05)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "threshold_vs_iforest_recall.png")
  plt.close()
  print("[SUKSES] outputs/figures/threshold_vs_iforest_recall.png")


if __name__ == "__main__":
  main()
