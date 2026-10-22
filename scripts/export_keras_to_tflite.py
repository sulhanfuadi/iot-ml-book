"""
Hands-on 27 (Bab 11): Ekspor Model Keras ke TensorFlow Lite (Jalur B)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

MLP kecil untuk klasifikasi biner ruangan, disimpan sebagai .keras lalu
dikonversi ke .tflite untuk inferensi edge.
Output: outputs/models/room_binary.keras, outputs/models/room_binary.tflite
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path

import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import set_random_seed

DATA_DIR = Path("data/processed/classification_room")
MODEL_DIR = Path("outputs/models")


def main():
  set_random_seed(42)
  MODEL_DIR.mkdir(parents=True, exist_ok=True)

  X_train = pd.read_csv(DATA_DIR / "X_train.csv").values.astype("float32")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze().values.astype("float32")

  model = Sequential([
      Input(shape=(X_train.shape[1],)),
      Dense(16, activation="relu"),
      Dense(8, activation="relu"),
      Dense(1, activation="sigmoid"),
  ])
  model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
  model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

  keras_path = MODEL_DIR / "room_binary.keras"
  model.save(keras_path)

  converter = tf.lite.TFLiteConverter.from_keras_model(model)
  tflite_model = converter.convert()
  tflite_path = MODEL_DIR / "room_binary.tflite"
  with open(tflite_path, "wb") as f:
    f.write(tflite_model)

  print("[SUKSES] Model Keras disimpan ke:", keras_path)
  print("[SUKSES] Model TFLite disimpan ke:", tflite_path)
  print("[INFO] Ukuran file TFLite:", tflite_path.stat().st_size, "bytes")


if __name__ == "__main__":
  main()
