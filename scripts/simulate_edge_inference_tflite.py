"""
Hands-on 28 (Bab 11): Simulasi Inferensi Lokal di Edge - TensorFlow Lite
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Inferensi lokal memakai interpreter TFLite, pola yang sama dengan deployment
TinyML / embedded.
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import argparse
import time
from pathlib import Path

import pandas as pd
import tensorflow as tf

MODEL_PATH = Path("outputs/models/room_binary.tflite")
DATA_PATH = Path("data/processed/classification_room/test.csv")


def main():
  parser = argparse.ArgumentParser(description="Simulasi inferensi edge TFLite")
  parser.add_argument("--max-rows", type=int, default=30,
                      help="Jumlah baris simulasi (default 30)")
  parser.add_argument("--delay", type=float, default=0.05,
                      help="Jeda antar-sampel dalam detik (default 0.05)")
  args = parser.parse_args()

  df = pd.read_csv(DATA_PATH).head(args.max_rows)
  feature_cols = [
      col for col in df.columns
      if col not in ["timestamp", "device_id", "status_label", "is_anomaly", "target_abnormal"]
  ]

  interpreter = tf.lite.Interpreter(model_path=str(MODEL_PATH))
  interpreter.allocate_tensors()
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  print("=== Simulasi inferensi TFLite lokal ===")
  for _, row in df.iterrows():
    x = row[feature_cols].values.astype("float32").reshape(1, -1)
    interpreter.set_tensor(input_details[0]["index"], x)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])[0][0]
    pred_label = 1 if output >= 0.5 else 0
    print(
        f"[{row['timestamp']}] "
        f"score={output:.4f} -> pred_abnormal={pred_label}"
    )
    time.sleep(args.delay)


if __name__ == "__main__":
  main()
