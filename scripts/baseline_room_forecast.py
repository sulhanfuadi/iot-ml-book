from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
DATA_DIR = Path("data/processed/forecast_room")
test_df = pd.read_csv(DATA_DIR / "test.csv")
y_true = test_df["target_temp_next_1step"]
# Baseline 1: last value
y_pred_last = test_df["temperature_c"]
# Baseline 2: moving average 3 langkah terakhir
y_pred_ma = test_df["temp_ma_3"]
def evaluate(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"=== {name} ===")
    print("MAE :", mae)
    print("RMSE:", rmse)
    print()
evaluate("Baseline Last Value", y_true, y_pred_last)
evaluate("Baseline Moving Average", y_true, y_pred_ma)
result_df = pd.DataFrame({
    "actual": y_true,
    "pred_last": y_pred_last,
    "pred_ma": y_pred_ma
})
result_df.to_csv(DATA_DIR / "baseline_predictions.csv", index=False)
print("Hasil baseline disimpan ke:", DATA_DIR / "baseline_predictions.csv")
