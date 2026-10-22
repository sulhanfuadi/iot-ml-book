from pathlib import Path
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
INPUT_PATH = Path("data/synthetic/current_sensor_anomaly.csv")
df = pd.read_csv(INPUT_PATH)
# Threshold statis sederhana
CURRENT_THRESHOLD = 10.0
df["threshold_anomaly"] = (df["current_amp"] > CURRENT_THRESHOLD).astype(int)
print("=== Threshold Detection ===")
print(df["threshold_anomaly"].value_counts())
y_true = df["ground_truth_anomaly"]
y_pred = df["threshold_anomaly"]
print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))
print("\nClassification Report:")
print(classification_report(y_true, y_pred, zero_division=0))
df.to_csv("outputs/reports/current_threshold_results.csv", index=False)
