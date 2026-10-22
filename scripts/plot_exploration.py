from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH = Path("data/raw/room_sensor_week.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")
# Plot suhu
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["temperature_c"], marker="o")
plt.title("Eksplorasi Awal - Suhu Ruangan")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "explore_temperature.png")
plt.show()
# Plot CO2
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["co2_ppm"], marker="o")
plt.title("Eksplorasi Awal - CO2 Ruangan")
plt.xlabel("Waktu")
plt.ylabel("CO2 (ppm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "explore_co2.png")
plt.show()
