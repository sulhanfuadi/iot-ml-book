from pathlib import Path
import pandas as pd
DATA_PATH = Path("data/raw/room_sensor_dirty.csv")
OUTPUT_PATH = Path("data/processed/room_sensor_clean.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH)
print("=== Data awal ===")
print(df.head())
print(f"Jumlah baris awal: {len(df)}")
# Parse timestamp, ubah error menjadi NaT
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
# Buang baris dengan timestamp invalid
df = df.dropna(subset=["timestamp"])
# Urutkan berdasarkan waktu
df = df.sort_values("timestamp")
# Hilangkan duplikasi timestamp, ambil record terakhir
df = df.drop_duplicates(subset=["timestamp"], keep="last")
print("\n=== Setelah membersihkan timestamp ===")
print(df.head())
print(f"Jumlah baris setelah clean timestamp: {len(df)}")
