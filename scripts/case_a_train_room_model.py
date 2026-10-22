"""
Hands-on 35 (Studi Kasus A): Latih Model Kenyamanan Ruangan
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Label aturan sederhana: nyaman jika suhu 24-28 C, kelembaban 45-65%, CO2 < 1000;
selain itu tidak_nyaman. Fitur: 9 fitur lingkungan + lag/rolling.
Output: models/case_a_room_rf.joblib, outputs/reports/case_a_evaluation.csv
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

INPUT_PATH = Path("data/synthetic/room_classification_dataset.csv")
MODEL_PATH = Path("models/case_a_room_rf.joblib")
REPORT_PATH = Path("outputs/reports/case_a_evaluation.csv")

FEATURE_COLS = [
    "temperature_c", "humidity_pct", "co2_ppm",
    "hour", "is_weekend",
    "temp_lag_1", "co2_lag_1", "temp_ma_3", "co2_ma_3",
]


def label_rule(row):
  nyaman = (
      24.0 <= row["temperature_c"] <= 28.0
      and 45.0 <= row["humidity_pct"] <= 65.0
      and row["co2_ppm"] < 1000
  )
  return "nyaman" if nyaman else "tidak_nyaman"


def main():
  MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
  REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

  df = pd.read_csv(INPUT_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").reset_index(drop=True)

  # Fitur
  df["hour"] = df["timestamp"].dt.hour
  df["is_weekend"] = (df["timestamp"].dt.dayofweek >= 5).astype(int)
  df["temp_lag_1"] = df["temperature_c"].shift(1)
  df["co2_lag_1"] = df["co2_ppm"].shift(1)
  df["temp_ma_3"] = df["temperature_c"].rolling(3).mean()
  df["co2_ma_3"] = df["co2_ppm"].rolling(3).mean()
  df = df.dropna().reset_index(drop=True)

  # Label
  df["label"] = df.apply(label_rule, axis=1)
  print("[INFO] Distribusi label:", df["label"].value_counts().to_dict())

  X = df[FEATURE_COLS]
  y = df["label"]
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42, stratify=y
  )

  # Baseline: Logistic Regression
  lr = Pipeline([
      ("scaler", StandardScaler()),
      ("model", LogisticRegression(max_iter=2000)),
  ])
  lr.fit(X_train, y_train)
  lr_acc = lr.score(X_test, y_test)

  # Model utama: Random Forest
  rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
  rf.fit(X_train, y_train)
  y_pred = rf.predict(X_test)

  print(f"\n=== Baseline Logistic Regression (accuracy): {lr_acc:.4f} ===")
  print("\n=== Random Forest - Confusion Matrix ===")
  print(confusion_matrix(y_test, y_pred))
  print("\n=== Random Forest - Classification Report ===")
  report = classification_report(y_test, y_pred, output_dict=True)
  print(classification_report(y_test, y_pred))

  rows = [{"model": "logistic_regression", "accuracy": lr_acc},
          {"model": "random_forest",
           "accuracy": report["accuracy"],
           "f1_nyaman": report["nyaman"]["f1-score"],
           "f1_tidak_nyaman": report["tidak_nyaman"]["f1-score"]}]
  pd.DataFrame(rows).to_csv(REPORT_PATH, index=False)

  joblib.dump(rf, MODEL_PATH)
  print("[SUKSES] Model disimpan ke:", MODEL_PATH)
  print("[SUKSES] Laporan disimpan ke:", REPORT_PATH)


if __name__ == "__main__":
  main()
