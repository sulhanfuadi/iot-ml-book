from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/synthetic/room_daily_synthetic.csv")
df = pd.read_csv(DATA_PATH)

print("=== Statistik dasar ===")
print(df.describe())

print("\n=== Korelasi ===")
print(df[["temperature_c", "humidity_pct"]].corr())

print("\n=== Cek nilai ekstrem ===")
print("Suhu min:", df["temperature_c"].min())
print("Suhu max:", df["temperature_c"].max())
print("Humidity min:", df["humidity_pct"].min())
print("Humidity max:", df["humidity_pct"].max())
