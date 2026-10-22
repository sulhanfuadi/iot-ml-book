from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
# Contoh:
# synthetic_train.csv dan real_test.csv harus punya kolom fitur/target yang sama
SYN_PATH = Path("data/processed/regression_energy/train.csv")
REAL_PATH = Path("data/processed/regression_energy/test.csv")
df_syn = pd.read_csv(SYN_PATH)
df_real = pd.read_csv(REAL_PATH)
feature_cols = [
    "power_watt",
    "hour", "day_of_week", "is_weekend",
    "hour_sin", "hour_cos",
    "power_lag_1", "power_lag_2", "power_lag_6",
    "power_ma_3", "power_ma_6", "power_std_6",
    "power_diff_1", "power_diff_6"
]
target_col = "target_power_next_1step"
X_syn = df_syn[feature_cols]
y_syn = df_syn[target_col]
X_real = df_real[feature_cols]
y_real = df_real[target_col]
model = LinearRegression()
model.fit(X_syn, y_syn)
y_real_pred = model.predict(X_real)
mae_real = mean_absolute_error(y_real, y_real_pred)
rmse_real = np.sqrt(mean_squared_error(y_real, y_real_pred))
print("=== Train pada data sintetik, test pada data nyata/test holdout ===")
print("MAE :", mae_real)
print("RMSE :", rmse_real)
