"""
Hands-on 22 (Bab 9): Evaluasi Isolation Forest terhadap Ground Truth Sintetis
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

INPUT_PATH = Path("outputs/reports/current_iforest_results.csv")


def main():
  df = pd.read_csv(INPUT_PATH)

  y_true = df["ground_truth_anomaly"]
  y_pred = df["iforest_anomaly"]

  print("=== Confusion Matrix (baris: ground truth, kolom: prediksi) ===")
  print(confusion_matrix(y_true, y_pred))

  print("\n=== Classification Report ===")
  print(classification_report(
      y_true, y_pred, target_names=["normal", "anomaly"], zero_division=0
  ))


if __name__ == "__main__":
  main()
