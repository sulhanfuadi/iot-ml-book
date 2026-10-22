from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
INPUT_PATH = Path("data/processed/room_30days_features.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")
sample = df.loc["2026-01-01":"2026-01-03 23:59:59"]
plt.figure(figsize=(12, 5))
plt.plot(sample.index, sample["temperature_c"], label="Temp Raw")
plt.plot(sample.index, sample["temp_ma_6"], label="Temp MA 6")
plt.title("Suhu Mentah vs Moving Average")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "room_temp_ma6.png")
plt.show()
