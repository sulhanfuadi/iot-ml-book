from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH = Path("data/raw/room_sensor_anomaly.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
# Aturan domain
df["anomaly_rule"] = (
    (df["temperature_c"] > 35) |
    (df["co2_ppm"] > 1200) |
    (df["power_watt"] > 250)
)
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["temperature_c"], marker="o", label="Temperature")
plt.scatter(
    df.loc[df["anomaly_rule"], "timestamp"],
    df.loc[df["anomaly_rule"], "temperature_c"],
    marker="x",
    s=100,
    label="Anomaly"
)
plt.title("Deteksi Anomali Suhu dengan Aturan Domain")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "anomaly_temperature_rule.png")
plt.show()
