from pathlib import Path
import time
import numpy as np
import pandas as pd
import tensorflow as tf
MODEL_PATH = Path("models/room_binary.tflite")
DATA_PATH = Path("data/processed/classification_room/test.csv")
df = pd.read_csv(DATA_PATH)
feature_cols = [col for col in df.columns if col not in ["timestamp", "device_id", "target_abnormal"]]
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
    time.sleep(0.2)
