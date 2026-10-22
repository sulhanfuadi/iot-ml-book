"""
Hands-on 33 (Bab 13): Feature Importance untuk Menjelaskan Prediksi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Ekstrak feature importance dari Random Forest room status + narasi sederhana.
Output: outputs/reports/feature_importance_room_model.csv,
        outputs/figures/feature_importance_room_model.png
"""

from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

MODEL_PATH = Path("outputs/models/room_status_rf.joblib")
X_TRAIN_PATH = Path("data/processed/classification_status/X_train.csv")
OUTPUT_DIR = Path("outputs")


def main():
  (OUTPUT_DIR / "reports").mkdir(parents=True, exist_ok=True)
  (OUTPUT_DIR / "figures").mkdir(parents=True, exist_ok=True)

  model = joblib.load(MODEL_PATH)
  X_train = pd.read_csv(X_TRAIN_PATH)

  importances = model.feature_importances_
  importance_df = pd.DataFrame({
      "feature": X_train.columns,
      "importance": importances,
  }).sort_values("importance", ascending=False)

  importance_df.to_csv(OUTPUT_DIR / "reports" / "feature_importance_room_model.csv",
                       index=False)

  print("=== Feature Importance ===")
  print(importance_df.round(4).to_string(index=False))

  # Visualisasi top 10
  top_n = 10
  plot_df = importance_df.head(top_n).sort_values("importance", ascending=True)

  plt.figure(figsize=(8, 6))
  plt.barh(plot_df["feature"], plot_df["importance"], color="steelblue")
  plt.title("Top Feature Importance - Random Forest Room Status")
  plt.xlabel("Importance")
  plt.ylabel("Feature")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "figures" / "feature_importance_room_model.png")
  plt.close()
  print("\n[SUKSES] outputs/figures/feature_importance_room_model.png")

  # Narasi sederhana
  top_features = importance_df.head(3)["feature"].tolist()
  print("\nTiga fitur paling berpengaruh:", top_features)
  print("Narasi: prediksi status ruangan paling dipengaruhi oleh "
        + ", ".join(top_features)
        + ", sehingga model melihat kombinasi kondisi lingkungan dan beban, "
        "bukan satu sensor tunggal.")


if __name__ == "__main__":
  main()
