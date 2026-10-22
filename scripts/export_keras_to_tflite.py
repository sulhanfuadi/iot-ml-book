from pathlib import Path
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
DATA_DIR = Path("data/processed/classification_room")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
X_train = pd.read_csv(DATA_DIR / "X_train.csv").values.astype("float32")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze().values.astype("float32")
model = Sequential([
    Dense(16, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(8, activation="relu"),
    Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)
keras_path = MODEL_DIR / "room_binary.keras"
model.save(keras_path)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
tflite_path = MODEL_DIR / "room_binary.tflite"
with open(tflite_path, "wb") as f:
    f.write(tflite_model)
print("Model Keras disimpan ke:", keras_path)
print("Model TFLite disimpan ke:", tflite_path)
print("Ukuran file TFLite:", tflite_path.stat().st_size, "bytes")
