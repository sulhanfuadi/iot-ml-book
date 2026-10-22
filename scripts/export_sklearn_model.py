from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
DATA_DIR = Path("data/processed/classification_status")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
model_path = MODEL_DIR / "room_status_rf.joblib"
joblib.dump(model, model_path)
print("Model scikit-learn berhasil disimpan ke:", model_path)
