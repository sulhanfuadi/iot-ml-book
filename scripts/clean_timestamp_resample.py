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

# Resample ke interval 10 menit
df = df.set_index("timestamp").sort_index()
df = df.resample("10min").first()
# Imputasi nilai hilang dengan interpolasi linier
num_cols = ["temperature_c", "humidity_pct", "co2_ppm", "power_watt"]
df[num_cols] = df[num_cols].interpolate(method="linear")
df["device_id"] = df["device_id"].ffill().bfill()
df = df.reset_index()
print("\n=== Setelah resample 10 menit + interpolasi linier ===")
print(df.head())
print(f"Jumlah baris akhir: {len(df)}")
print(f"Sisa nilai hilang: {int(df[num_cols].isna().sum().sum())}")
df.to_csv(OUTPUT_PATH, index=False)
print(f"[SUKSES] Dataset bersih tersimpan: {OUTPUT_PATH}")
