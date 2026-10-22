from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
DATA_DIR = Path("data/processed/classification_status")
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
X_val = pd.read_csv(DATA_DIR / "X_val.csv")
y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)
# Validasi
y_val_pred = model.predict(X_val)
print("=== LOGISTIC REGRESSION - VALIDATION ===")
print("Accuracy:", accuracy_score(y_val, y_val_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_val, y_val_pred, labels=["normal", "warning", "fault"]))
print("\nClassification Report:")
print(classification_report(y_val, y_val_pred, zero_division=0))
# Test
y_test_pred = model.predict(X_test)
print("\n=== LOGISTIC REGRESSION - TEST ===")
print("Accuracy:", accuracy_score(y_test, y_test_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred, labels=["normal", "warning", "fault"]))
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred, zero_division=0))
