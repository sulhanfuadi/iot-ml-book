"""
Hands-on 27 (Bab 11): Ekspor Model scikit-learn Ringan (Jalur A)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Random Forest dangkal untuk klasifikasi status ruangan, disimpan dengan joblib
agar siap dipakai di Raspberry Pi / mini PC dengan Python biasa.
Output: outputs/models/room_status_rf.joblib
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DATA_DIR = Path("data/processed/classification_status")
MODEL_DIR = Path("outputs/models")


def main():
  MODEL_DIR.mkdir(parents=True, exist_ok=True)

  X_train = pd.read_csv(DATA_DIR / "X_train.csv")
  y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
  X_test = pd.read_csv(DATA_DIR / "X_test.csv")
  y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

  model = RandomForestClassifier(
      n_estimators=100,
      max_depth=8,
      random_state=42,
      n_jobs=-1,
  )
  model.fit(X_train, y_train)

  acc = accuracy_score(y_test, model.predict(X_test))
  print(f"[INFO] Akurasi test model: {acc:.4f}")

  model_path = MODEL_DIR / "room_status_rf.joblib"
  joblib.dump(model, model_path)
  print("[SUKSES] Model scikit-learn disimpan ke:", model_path)
  print("[INFO] Ukuran file:", model_path.stat().st_size, "bytes")


if __name__ == "__main__":
  main()
