"""
Hands-on 26 (Bab 10): Random Forest untuk Forecasting Suhu Ruang
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: data/processed/forecast_room/rf_predictions.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/forecast_room")


def main():
  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = RandomForestRegressor(
      n_estimators=200,
      max_depth=10,
      random_state=42,
      n_jobs=-1,
  )
  model.fit(X_train, y_train)

  y_test_pred = model.predict(X_test)
  mae = mean_absolute_error(y_test, y_test_pred)
  rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

  print("=== RANDOM FOREST ROOM FORECAST ===")
  print("MAE :", mae)
  print("RMSE:", rmse)

  result_df = pd.DataFrame({
      "actual": y_test,
      "pred_rf": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "rf_predictions.csv", index=False)
  print("[SUKSES] Hasil Random Forest suhu disimpan.")


if __name__ == "__main__":
  main()
