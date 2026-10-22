"""
Hands-on 25: Perbandingan 3 Model Klasifikasi Status Perangkat
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Model: Logistic Regression, Random Forest, Gradient Boosting.
Metrik: accuracy, precision/recall/F1 weighted pada data test.
Output: outputs/reports/model_comparison_status.csv
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
  accuracy_score,
  f1_score,
  precision_score,
  recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data/processed/classification_status")
OUTPUT_DIR = Path("outputs/reports")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  models = {
      "logistic_regression": Pipeline([
          ("scaler", StandardScaler()),
          ("model", LogisticRegression(max_iter=2000)),
      ]),
      "random_forest": RandomForestClassifier(
          n_estimators=200, max_depth=10, random_state=42, n_jobs=-1
      ),
      "gradient_boosting": GradientBoostingClassifier(random_state=42),
  }

  results = []
  for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    results.append({
        "model": name,
        "accuracy": acc,
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
    })

  results_df = pd.DataFrame(results)
  results_df = results_df.sort_values("f1_weighted", ascending=False)

  print("=== HASIL PERBANDINGAN MODEL ===")
  print(results_df.to_string(index=False))

  results_df.to_csv(OUTPUT_DIR / "model_comparison_status.csv", index=False)
  print("\n[SUKSES] Disimpan ke:", OUTPUT_DIR / "model_comparison_status.csv")


if __name__ == "__main__":
  main()
