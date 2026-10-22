"""
Hands-on 23 (Bab 9): Deteksi Anomali dengan Threshold Statis
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/reports/current_threshold_results.csv
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

INPUT_PATH = Path("data/synthetic/current_sensor_anomaly.csv")
OUTPUT_DIR = Path("outputs/reports")

# Threshold statis sederhana (Ampere)
CURRENT_THRESHOLD = 10.0


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  df["threshold_anomaly"] = (df["current_amp"] > CURRENT_THRESHOLD).astype(int)

  print("=== Threshold Detection (current > 10.0 A) ===")
  print(df["threshold_anomaly"].value_counts().sort_index().to_string())

  y_true = df["ground_truth_anomaly"]
  y_pred = df["threshold_anomaly"]

  print("\nConfusion Matrix:")
  print(confusion_matrix(y_true, y_pred))

  print("\nClassification Report:")
  print(classification_report(
      y_true, y_pred, target_names=["normal", "anomaly"], zero_division=0
  ))

  df.to_csv(OUTPUT_DIR / "current_threshold_results.csv", index=False)
  print("[SUKSES] outputs/reports/current_threshold_results.csv")


if __name__ == "__main__":
  main()
