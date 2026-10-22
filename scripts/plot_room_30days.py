from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")
# Plot 3 hari pertama agar mudah dibaca
sample = df.loc["2026-01-01":"2026-01-03 23:59:59"]
plt.figure(figsize=(12, 5))
plt.plot(sample.index, sample["temperature_c"], label="Temperature")
plt.plot(sample.index, sample["humidity_pct"], label="Humidity")
plt.title("Data Sintetik Suhu-kelembaban (3 Hari Pertama)")
plt.xlabel("Waktu")
plt.ylabel("Nilai")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "room_30days_sample.png")
plt.show()
