"""
Hands-on 37 (Studi Kasus C): Forecasting Beban + Alert Beban Tidak Normal
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Random Forest memprediksi daya langkah berikutnya; alert bila daya > 500 W atau
|forecast error| > 80 W.
Output: outputs/reports/case_c_energy_results.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

INPUT = Path("data/synthetic/case_c_energy.csv")
OUTPUT = Path("outputs/reports/case_c_energy_results.csv")


def main():
  OUTPUT.parent.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp").reset_index(drop=True)

  df["target_next"] = df["power_watt"].shift(-1)
  df["hour"] = df["timestamp"].dt.hour
  df["day_of_week"] = df["timestamp"].dt.dayofweek
  df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
  df["power_lag_1"] = df["power_watt"].shift(1)
  df["power_lag_6"] = df["power_watt"].shift(6)
  df["power_ma_3"] = df["power_watt"].rolling(3).mean()
  df["power_ma_6"] = df["power_watt"].rolling(6).mean()
  df["power_std_6"] = df["power_watt"].rolling(6).std()
  df = df.dropna().reset_index(drop=True)

  feature_cols = [
      "power_watt", "hour", "day_of_week", "is_weekend",
      "power_lag_1", "power_lag_6", "power_ma_3", "power_ma_6", "power_std_6",
  ]

  n = len(df)
  train_end = int(n * 0.70)
  X_train = df.iloc[:train_end][feature_cols]
  y_train = df.iloc[:train_end]["target_next"]
  X_test = df.iloc[train_end:][feature_cols]
  y_test = df.iloc[train_end:]["target_next"]

  model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)
  mae = mean_absolute_error(y_test, y_pred)
  rmse = np.sqrt(mean_squared_error(y_test, y_pred))
  print("MAE :", mae)
  print("RMSE:", rmse)

  result = df.iloc[train_end:].copy()
  result["pred_next"] = y_pred
  result["forecast_error_abs"] = (result["target_next"] - result["pred_next"]).abs()

  # Alert beban tak normal
  result["alert_abnormal_load"] = (
      (result["power_watt"] > 500) | (result["forecast_error_abs"] > 80)
  ).astype(int)

  print("\nContoh hasil:")
  print(result[["timestamp", "power_watt", "pred_next",
                "forecast_error_abs", "alert_abnormal_load"]].head(20).to_string(index=False))

  result.to_csv(OUTPUT, index=False)
  print(f"\n[SUKSES] Disimpan ke: {OUTPUT}")
  print(f"[INFO] Jumlah alert: {int(result['alert_abnormal_load'].sum())} dari {len(result)} baris")


if __name__ == "__main__":
  main()
