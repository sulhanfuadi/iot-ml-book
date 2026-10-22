"""
Hands-on 22: Evaluasi Baseline Model Regresi (Linear Regression)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Baseline regresi prediksi daya 10 menit ke depan pada
data/processed/regression_energy. Metrik: MAE dan RMSE.
Prediksi test disimpan ke test_predictions.csv.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/regression_energy")


def main():
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_val = pd.read_csv(DATA_DIR / "X_val.csv")
  y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = LinearRegression()
  model.fit(X_train, y_train)

  y_val_pred = model.predict(X_val)
  mae_val = mean_absolute_error(y_val, y_val_pred)
  rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))
  print("=== HASIL VALIDASI REGRESI ===")
  print("MAE :", mae_val)
  print("RMSE:", rmse_val)

  y_test_pred = model.predict(X_test)
  mae_test = mean_absolute_error(y_test, y_test_pred)
  rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
  print("\n=== HASIL TEST REGRESI ===")
  print("MAE :", mae_test)
  print("RMSE:", rmse_test)

  result_df = pd.DataFrame({
      "actual": y_test,
      "predicted": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "test_predictions.csv", index=False)
  print("\n[SUKSES] Prediksi test disimpan ke:", DATA_DIR / "test_predictions.csv")


if __name__ == "__main__":
  main()
