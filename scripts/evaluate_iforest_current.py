from pathlib import Path
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
INPUT_PATH = Path("outputs/reports/current_iforest_results.csv")
df = pd.read_csv(INPUT_PATH)
y_true = df["ground_truth_anomaly"]
y_pred = df["iforest_anomaly"]
print("=== Evaluasi Isolation Forest vs Ground Truth Sintetis ===")
print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))
print("\nClassification Report:")
print(classification_report(y_true, y_pred, zero_division=0))
