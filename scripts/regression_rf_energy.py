from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
DATA_DIR = Path("data/processed/regression_energy")
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
X_val = pd.read_csv(DATA_DIR / "X_val.csv")
y_val = pd.read_csv(DATA_DIR / "y_val.csv").squeeze()
X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
# Validasi
y_val_pred = model.predict(X_val)
mae_val = mean_absolute_error(y_val, y_val_pred)
rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))
# Test
y_test_pred = model.predict(X_test)
mae_test = mean_absolute_error(y_test, y_test_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
print("=== RANDOM FOREST REGRESSOR ===")
print("Validation MAE :", mae_val)
print("Validation RMSE :", rmse_val)
print("Test MAE        :", mae_test)
print("Test RMSE       :", rmse_test)
result_df = pd.DataFrame({
    "actual": y_test,
    "predicted_rf": y_test_pred
})
result_df.to_csv(DATA_DIR / "pred_rf_test.csv", index=False)
print("Prediksi test disimpan ke:", DATA_DIR / "pred_rf_test.csv")
