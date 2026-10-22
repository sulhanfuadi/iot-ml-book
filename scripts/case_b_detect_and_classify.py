"""
Hands-on 36 (Studi Kasus B): Anomaly Detection + Klasifikasi Fault
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Isolation Forest untuk anomali + Random Forest untuk klasifikasi status.
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

INPUT = Path("data/processed/case_b_motor_features.csv")


def main():
  df = pd.read_csv(INPUT)
  feature_cols = ["vib_mean", "vib_std", "vib_rms", "vib_ptp", "cur_mean", "cur_max"]
  X = df[feature_cols]
  y = df["status_label"]

  # Isolation Forest
  iso = IsolationForest(n_estimators=200, contamination=0.15, random_state=42)
  df["anomaly_pred"] = (iso.fit_predict(X) == -1).astype(int)
  print("=== Isolation Forest ===")
  print(df["anomaly_pred"].value_counts().sort_index().to_string())

  # Klasifikasi fault dasar (split time-aware)
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, shuffle=False
  )
  clf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
  clf.fit(X_train, y_train)
  y_pred = clf.predict(X_test)

  print("\n=== Fault Classification ===")
  print(confusion_matrix(y_test, y_pred, labels=["normal", "warning", "fault"]))
  print(classification_report(y_test, y_pred, zero_division=0))


if __name__ == "__main__":
  main()
