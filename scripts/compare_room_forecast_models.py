"""
Hands-on 26 (Bab 10): Perbandingan Akhir Baseline vs Random Forest vs LSTM Mini
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: outputs/reports/room_forecast_model_comparison.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR = Path("data/processed/forecast_room")
LSTM_DIR = Path("data/processed/lstm_room")
OUTPUT_DIR = Path("outputs/reports")


def metrics(y_true, y_pred):
  mae = mean_absolute_error(y_true, y_pred)
  rmse = np.sqrt(mean_squared_error(y_true, y_pred))
  return mae, rmse


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  base_df = pd.read_csv(BASE_DIR / "baseline_predictions.csv")
  rf_df = pd.read_csv(BASE_DIR / "rf_predictions.csv")
  lstm_df = pd.read_csv(LSTM_DIR / "lstm_predictions.csv")

  # Ambil panjang minimum agar bisa dibandingkan
  n = min(len(base_df), len(rf_df), len(lstm_df))
  actual = base_df["actual"].iloc[:n].reset_index(drop=True)
  pred_last = base_df["pred_last"].iloc[:n].reset_index(drop=True)
  pred_ma = base_df["pred_ma"].iloc[:n].reset_index(drop=True)
  pred_rf = rf_df["pred_rf"].iloc[:n].reset_index(drop=True)
  pred_lstm = lstm_df["pred_lstm"].iloc[:n].reset_index(drop=True)

  results = []
  for name, pred in [
      ("LastValue", pred_last),
      ("MovingAverage", pred_ma),
      ("RandomForest", pred_rf),
      ("LSTMmini", pred_lstm),
  ]:
    mae, rmse = metrics(actual, pred)
    results.append({"model": name, "mae": mae, "rmse": rmse})

  results_df = pd.DataFrame(results).sort_values("rmse")
  print("=== PERBANDINGAN MODEL FORECASTING SUHU ===")
  print(results_df.to_string(index=False))

  results_df.to_csv(OUTPUT_DIR / "room_forecast_model_comparison.csv", index=False)
  print("\n[SUKSES] Hasil disimpan ke:", OUTPUT_DIR / "room_forecast_model_comparison.csv")


if __name__ == "__main__":
  main()
