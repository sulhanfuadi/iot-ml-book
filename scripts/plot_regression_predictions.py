"""
Hands-on 23: Visualisasi Prediksi Regresi (Aktual vs Model)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path("data/processed/regression_energy")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  df_linear = pd.read_csv(DATA_DIR / "pred_linear_test.csv")
  df_ridge = pd.read_csv(DATA_DIR / "pred_ridge_test.csv")
  df_rf = pd.read_csv(DATA_DIR / "pred_rf_test.csv")

  plot_df = pd.DataFrame({
      "actual": df_linear["actual"],
      "pred_linear": df_linear["predicted_linear"],
      "pred_ridge": df_ridge["predicted_ridge"],
      "pred_rf": df_rf["predicted_rf"],
  })

  sample = plot_df.iloc[:120].copy()
  plt.figure(figsize=(12, 5))
  plt.plot(sample.index, sample["actual"], label="Actual", lw=1.5)
  plt.plot(sample.index, sample["pred_linear"], label="Linear Regression", lw=1)
  plt.plot(sample.index, sample["pred_ridge"], label="Ridge Regression", lw=1)
  plt.plot(sample.index, sample["pred_rf"], label="Random Forest", lw=1)
  plt.title("Prediksi Energi: Aktual vs Model")
  plt.xlabel("Index waktu test")
  plt.ylabel("Power Watt")
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "regression_predictions_compare.png")
  plt.close()
  print("[SUKSES] outputs/figures/regression_predictions_compare.png")


if __name__ == "__main__":
  main()
