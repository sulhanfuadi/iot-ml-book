from pathlib import Path
import time
import pandas as pd
import joblib
MODEL_PATH = Path("models/room_status_rf.joblib")
DATA_PATH = Path("data/processed/classification_status/test.csv")
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)
feature_cols = [
    "temperature_c", "humidity_pct", "co2_ppm", "power_watt",
    "hour", "day_of_week", "is_weekend",
    "temp_lag_1", "co2_lag_1", "power_lag_1",
    "temp_ma_3", "co2_ma_3", "power_ma_3"
]
print("=== Simulasi inferensi lokal di edge ===")
for i, row in df.iterrows():
    x = row[feature_cols].to_frame().T
    pred = model.predict(x)[0]
    print(
        f"[{row['timestamp']}] "
        f"T={row['temperature_c']:.2f}C, "
        f"H={row['humidity_pct']:.2f}%, "
        f"CO2={row['co2_ppm']}, "
        f"P={row['power_watt']:.2f}W "
        f"-> status_pred={pred}"
    )
    time.sleep(0.2)   # simulasi aliran data
