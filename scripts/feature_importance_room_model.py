from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
MODEL_PATH = Path("models/room_status_rf.joblib")
X_TRAIN_PATH = Path("data/processed/classification_status/X_train.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
model = joblib.load(MODEL_PATH)
X_train = pd.read_csv(X_TRAIN_PATH)
importances = model.feature_importances_
importance_df = pd.DataFrame({
    "feature": X_train.columns,
    "importance": importances
}).sort_values("importance", ascending=False)
importance_df.to_csv("outputs/reports/feature_importance_room_model.cs v", index=False)
print("=== Feature Importance ===")
print(importance_df)
# Visualisasi top 10
top_n = 10
plot_df = importance_df.head(top_n).sort_values("importance", ascending=True)
plt.figure(figsize=(8, 6))
plt.barh(plot_df["feature"], plot_df["importance"])
plt.title("Top Feature Importance - Random Forest Room Status")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("outputs/figures/feature_importance_room_model.png")
plt.show()
