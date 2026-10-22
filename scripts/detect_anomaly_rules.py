from pathlib import Path
import pandas as pd
DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
# Aturan domain
df["anomaly_rule"] = (
    (df["temperature_c"] > 35) |
    (df["co2_ppm"] > 1200) |
    (df["power_watt"] > 250)
)
print(df[["timestamp", "temperature_c", "co2_ppm", "power_watt", "anomaly_rule"]])
