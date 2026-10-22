"""
Hands-on 25: Visualisasi Perbandingan Model + Kurva ROC
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, label_binarize

INPUT_PATH = Path("outputs/reports/model_comparison_status.csv")
DATA_DIR = Path("data/processed/classification_status")
OUTPUT_DIR = Path("outputs/figures")
LABELS = ["normal", "warning", "fault"]


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  plt.figure(figsize=(10, 5))
  plt.bar(df["model"], df["accuracy"], color="steelblue")
  plt.title("Perbandingan Accuracy Model")
  plt.xlabel("Model")
  plt.ylabel("Accuracy")
  plt.ylim(0.9, 1.0)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "compare_accuracy_models.png")
  plt.close()
  print("[SUKSES] outputs/figures/compare_accuracy_models.png")

  plt.figure(figsize=(10, 5))
  plt.bar(df["model"], df["f1_weighted"], color="seagreen")
  plt.title("Perbandingan F1 Weighted Model")
  plt.xlabel("Model")
  plt.ylabel("F1 Weighted")
  plt.ylim(0.9, 1.0)
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "compare_f1_models.png")
  plt.close()
  print("[SUKSES] outputs/figures/compare_f1_models.png")

  # Kurva ROC one-vs-rest untuk tiap model
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  y_test_bin = label_binarize(y_test, classes=LABELS)

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

  fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
  for ax, (name, model) in zip(axes, models.items()):
    model.fit(X_train, y_train)
    y_score = model.predict_proba(X_test)
    for i, label in enumerate(LABELS):
      fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
      ax.plot(fpr, tpr, label=f"{label} (AUC={auc(fpr, tpr):.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8)
    ax.set_title(name)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(fontsize=7)
  plt.suptitle("Kurva ROC One-vs-Rest per Model")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "compare_roc_curves.png")
  plt.close()
  print("[SUKSES] outputs/figures/compare_roc_curves.png")


if __name__ == "__main__":
  main()
