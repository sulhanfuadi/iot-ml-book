"""
Hands-on 24: Klasifikasi Status Perangkat - Random Forest Classifier
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
  accuracy_score,
  classification_report,
  confusion_matrix,
)

DATA_DIR = Path("data/processed/classification_status")
LABELS = ["normal", "warning", "fault"]


def main():
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_val = pd.read_csv(DATA_DIR / "X_val.csv")
  y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = RandomForestClassifier(
      n_estimators=200,
      max_depth=10,
      random_state=42,
      n_jobs=-1,
  )
  model.fit(X_train, y_train)

  y_val_pred = model.predict(X_val)
  print("=== RANDOM FOREST CLASSIFIER - VALIDATION ===")
  print("Accuracy:", accuracy_score(y_val, y_val_pred))
  print("\nConfusion Matrix:")
  print(confusion_matrix(y_val, y_val_pred, labels=LABELS))
  print("\nClassification Report:")
  print(classification_report(y_val, y_val_pred, zero_division=0))

  y_test_pred = model.predict(X_test)
  print("\n=== RANDOM FOREST CLASSIFIER - TEST ===")
  print("Accuracy:", accuracy_score(y_test, y_test_pred))
  print("\nConfusion Matrix:")
  print(confusion_matrix(y_test, y_test_pred, labels=LABELS))
  print("\nClassification Report:")
  print(classification_report(y_test, y_test_pred, zero_division=0))


if __name__ == "__main__":
  main()
