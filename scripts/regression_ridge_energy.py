"""
Hands-on 23: Prediksi Energi dengan Ridge Regression
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Varian linear dengan regularisasi L2 (alpha=1.0), fitur distandarisasi.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data/processed/regression_energy")


def main():
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_val = pd.read_csv(DATA_DIR / "X_val.csv")
  y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = Pipeline([
      ("scaler", StandardScaler()),
      ("model", Ridge(alpha=1.0)),
  ])
  model.fit(X_train, y_train)

  y_val_pred = model.predict(X_val)
  mae_val = mean_absolute_error(y_val, y_val_pred)
  rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))

  y_test_pred = model.predict(X_test)
  mae_test = mean_absolute_error(y_test, y_test_pred)
  rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))

  print("=== RIDGE REGRESSION ===")
  print("Validation MAE :", mae_val)
  print("Validation RMSE:", rmse_val)
  print("Test MAE       :", mae_test)
  print("Test RMSE      :", rmse_test)

  result_df = pd.DataFrame({
      "actual": y_test,
      "predicted_ridge": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "pred_ridge_test.csv", index=False)
  print("[SUKSES] Prediksi test disimpan ke:", DATA_DIR / "pred_ridge_test.csv")


if __name__ == "__main__":
  main()
