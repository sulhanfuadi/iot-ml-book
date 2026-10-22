"""
Hands-on 23 (Bab 9): Perbandingan Threshold Statis vs Isolation Forest
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/reports/threshold_vs_iforest.csv
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import (
  accuracy_score,
  f1_score,
  precision_score,
  recall_score,
)

THRESH_PATH = Path("outputs/reports/current_threshold_results.csv")
IFOREST_PATH = Path("outputs/reports/current_iforest_results.csv")
OUTPUT_DIR = Path("outputs/reports")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df_thr = pd.read_csv(THRESH_PATH)
  df_if = pd.read_csv(IFOREST_PATH)

  y_true = df_thr["ground_truth_anomaly"]

  results = []

  # Threshold
  y_thr = df_thr["threshold_anomaly"]
  results.append({
      "method": "Threshold",
      "accuracy": accuracy_score(y_true, y_thr),
      "precision": precision_score(y_true, y_thr, zero_division=0),
      "recall": recall_score(y_true, y_thr, zero_division=0),
      "f1": f1_score(y_true, y_thr, zero_division=0),
  })

  # Isolation Forest
  y_if = df_if["iforest_anomaly"]
  results.append({
      "method": "IsolationForest",
      "accuracy": accuracy_score(y_true, y_if),
      "precision": precision_score(y_true, y_if, zero_division=0),
      "recall": recall_score(y_true, y_if, zero_division=0),
      "f1": f1_score(y_true, y_if, zero_division=0),
  })

  results_df = pd.DataFrame(results)
  print("=== Perbandingan Threshold vs Isolation Forest ===")
  print(results_df.to_string(index=False))

  results_df.to_csv(OUTPUT_DIR / "threshold_vs_iforest.csv", index=False)
  print("\n[SUKSES] outputs/reports/threshold_vs_iforest.csv")


if __name__ == "__main__":
  main()
