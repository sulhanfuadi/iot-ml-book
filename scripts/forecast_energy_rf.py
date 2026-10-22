"""
Hands-on 25 (Bab 10): Forecasting Konsumsi Energi - Random Forest Regressor
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: data/processed/regression_energy/energy_rf_predictions.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/regression_energy")


def evaluate(name, y_true, y_pred):
  mae = mean_absolute_error(y_true, y_pred)
  rmse = np.sqrt(mean_squared_error(y_true, y_pred))
  print(f"=== {name} ===")
  print("MAE :", mae)
  print("RMSE:", rmse)
  print()


def main():
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_val = pd.read_csv(DATA_DIR / "X_val.csv")
  y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = RandomForestRegressor(
      n_estimators=200,
      max_depth=10,
      random_state=42,
      n_jobs=-1,
  )
  model.fit(X_train, y_train)

  y_val_pred = model.predict(X_val)
  y_test_pred = model.predict(X_test)

  evaluate("Random Forest - Validation", y_val, y_val_pred)
  evaluate("Random Forest - Test", y_test, y_test_pred)

  result_df = pd.DataFrame({
      "actual": y_test,
      "pred_rf": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "energy_rf_predictions.csv", index=False)
  print("[SUKSES] Hasil Random Forest disimpan.")


if __name__ == "__main__":
  main()
