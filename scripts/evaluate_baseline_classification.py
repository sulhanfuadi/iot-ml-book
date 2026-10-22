from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
DATA_DIR = Path("data/processed/classification_room")
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
X_val = pd.read_csv(DATA_DIR / "X_val.csv")
y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()
# Model baseline
model = LogisticRegression(max_iter=1000)
# Training
model.fit(X_train, y_train)
# Validasi
y_val_pred = model.predict(X_val)
print("=== HASIL VALIDASI KLASIFIKASI ===")
print("Accuracy :", accuracy_score(y_val, y_val_pred))
print("Precision:", precision_score(y_val, y_val_pred, zero_division=0))
print("Recall   :", recall_score(y_val, y_val_pred, zero_division=0))
print("F1 Score :", f1_score(y_val, y_val_pred, zero_division=0))
print("\nConfusion Matrix:")
print(confusion_matrix(y_val, y_val_pred))
print("\nClassification Report:")
print(classification_report(y_val, y_val_pred, zero_division=0))
# Test
y_test_pred = model.predict(X_test)
print("\n=== HASIL TEST KLASIFIKASI ===")
print("Accuracy :", accuracy_score(y_test, y_test_pred))
print("Precision:", precision_score(y_test, y_test_pred, zero_division=0))
print("Recall   :", recall_score(y_test, y_test_pred, zero_division=0))
print("F1 Score :", f1_score(y_test, y_test_pred, zero_division=0))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))
