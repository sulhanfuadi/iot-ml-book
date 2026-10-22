"""
Hands-on 25 (variasi): Perbandingan 3 Model Regresi Energi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Model: Linear Regression, Random Forest Regressor, Gradient Boosting Regressor.
Output: outputs/reports/model_comparison_regression.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/regression_energy")
OUTPUT_DIR = Path("outputs/reports")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  models = {
      "linear_regression": LinearRegression(),
      "random_forest": RandomForestRegressor(
          n_estimators=200, max_depth=10, random_state=42, n_jobs=-1
      ),
      "gradient_boosting": GradientBoostingRegressor(random_state=42),
  }

  results = []
  for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results.append({
        "model": name,
        "mae": mean_absolute_error(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
    })

  results_df = pd.DataFrame(results).sort_values("mae")
  print("=== HASIL PERBANDINGAN REGRESOR ===")
  print(results_df.to_string(index=False))
  results_df.to_csv(OUTPUT_DIR / "model_comparison_regression.csv", index=False)
  print("\n[SUKSES] Disimpan ke:", OUTPUT_DIR / "model_comparison_regression.csv")


if __name__ == "__main__":
  main()
