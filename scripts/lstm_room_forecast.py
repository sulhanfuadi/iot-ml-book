"""
Hands-on 26 (Bab 10): LSTM Mini dengan Keras untuk Forecasting Suhu
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Output: data/processed/lstm_room/lstm_predictions.csv
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path

import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import set_random_seed
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("data/processed/lstm_room")


def main():
  set_random_seed(42)

  X_train = np.load(DATA_DIR / "X_train.npy")
  X_val = np.load(DATA_DIR / "X_val.npy")
  X_test = np.load(DATA_DIR / "X_test.npy")
  y_train = np.load(DATA_DIR / "y_train.npy")
  y_val = np.load(DATA_DIR / "y_val.npy")
  y_test = np.load(DATA_DIR / "y_test.npy")

  model = Sequential([
      LSTM(32, input_shape=(X_train.shape[1], X_train.shape[2])),
      Dense(1),
  ])
  model.compile(optimizer="adam", loss="mse")

  early_stop = EarlyStopping(
      monitor="val_loss",
      patience=5,
      restore_best_weights=True,
  )

  model.fit(
      X_train, y_train,
      validation_data=(X_val, y_val),
      epochs=30,
      batch_size=32,
      callbacks=[early_stop],
      verbose=0,
  )

  y_test_pred = model.predict(X_test, verbose=0).flatten()

  mae = mean_absolute_error(y_test, y_test_pred)
  rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

  print("=== LSTM MINI ===")
  print("MAE :", mae)
  print("RMSE:", rmse)

  result_df = pd.DataFrame({
      "actual": y_test,
      "pred_lstm": y_test_pred,
  })
  result_df.to_csv(DATA_DIR / "lstm_predictions.csv", index=False)
  print("[SUKSES] Prediksi LSTM disimpan.")


if __name__ == "__main__":
  main()
