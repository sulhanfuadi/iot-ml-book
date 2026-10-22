"""
Hands-on 24 (Bab 10): Linear Regression Berbasis Lag untuk Forecasting Suhu
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: data/processed/forecast_room/linear_predictions.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/forecast_room")


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

  model = LinearRegression()
  model.fit(X_train, y_train)

  y_val_pred = model.predict(X_val)
  y_test_pred = model.predict(X_test)

  evaluate("Linear Regression - Validation", y_val, y_val_pred)
  evaluate("Linear Regression - Test", y_test, y_test_pred)

  result_df = pd.DataFrame({
      "actual": y_test,
      "pred_linear": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "linear_predictions.csv", index=False)
  print("[SUKSES] Prediksi disimpan ke:", DATA_DIR / "linear_predictions.csv")


if __name__ == "__main__":
  main()
