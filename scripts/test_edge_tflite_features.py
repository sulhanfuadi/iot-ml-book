"""Regresi untuk perbaikan pemilihan fitur di simulate_edge_inference_tflite.py.

Memastikan kolom non-numerik (status_label) dan kolom target (target_abnormal,
is_anomaly) tidak masuk fitur, dan jumlah fitur cocok dengan input model TFLite.
Jalankan dari root repo: python scripts/test_edge_tflite_features.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

MODEL_PATH = Path("models/room_binary.tflite")
DATA_PATH = Path("data/processed/classification_room/test.csv")
EXCLUDE = ["timestamp", "device_id", "target_abnormal", "status_label", "is_anomaly"]

df = pd.read_csv(DATA_PATH)
feature_cols = [col for col in df.columns if col not in EXCLUDE]
x = df[feature_cols].head(5).values.astype("float32")  # gagal bila ada kolom string
print(f"[INFO] {len(feature_cols)} fitur numerik lolos konversi float32")

try:
    import tensorflow as tf
except ImportError:
    print("[INFO] tensorflow tidak terpasang; cek fitur selesai tanpa uji model")
    raise SystemExit(0)

interpreter = tf.lite.Interpreter(model_path=str(MODEL_PATH))
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
expected = int(input_details[0]["shape"][-1])
assert x.shape[1] == expected, f"jumlah fitur {x.shape[1]} != input model {expected}"
interpreter.set_tensor(input_details[0]["index"], x[:1])
interpreter.invoke()
score = float(interpreter.get_tensor(interpreter.get_output_details()[0]["index"])[0][0])
print(f"[SUKSES] input model [{1}, {expected}] cocok; inferensi sampel score={score:.4f}")
