from pathlib import Path
import time
import random
import joblib
import pandas as pd
MODEL_PATH = Path("models/room_status_rf.joblib")
OUTPUT_LOG = Path("outputs/reports/edge_room_predictions.csv")
OUTPUT_LOG.parent.mkdir(parents=True, exist_ok=True)
model = joblib.load(MODEL_PATH)
records = []
def build_feature_row(temp, hum, co2, power, hour, dow):
    # contoh fitur sederhana; pada implementasi nyata
    # beberapa lag/rolling sebaiknya dipertahankan dari buffer lokal
    row = {
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "hour": hour,
        "day_of_week": dow,
        "is_weekend": int(dow >= 5),
        "temp_lag_1": temp,
        "co2_lag_1": co2,
        "power_lag_1": power,
        "temp_ma_3": temp,
        "co2_ma_3": co2,
        "power_ma_3": power
    }
    return pd.DataFrame([row])
print("=== Mini proyek edge room classifier dimulai ===")
for step in range(30):
    temp = round(random.uniform(24.0, 33.0), 2)
    hum = round(random.uniform(40.0, 70.0), 2)
    co2 = random.randint(450, 1500)
    power = round(random.uniform(100.0, 300.0), 2)
    hour = (8 + step // 3) % 24
    dow = 2   # misal Rabu
    X = build_feature_row(temp, hum, co2, power, hour, dow)
    pred = model.predict(X)[0]
    print(
        f"step={step} | T={temp} H={hum} CO2={co2} P={power} -> status={pred}"
    )
    records.append({
        "step": step,
        "temperature_c": temp,
        "humidity_pct": hum,
        "co2_ppm": co2,
        "power_watt": power,
        "predicted_status": pred
    })
    time.sleep(0.3)
pd.DataFrame(records).to_csv(OUTPUT_LOG, index=False)
print("Log hasil inferensi disimpan ke:", OUTPUT_LOG)
