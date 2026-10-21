from pathlib import Path
import pandas as pd

# Lokasi file data
data_path = Path("data/raw/room_sensor_dummy.csv")

# Baca CSV
df = pd.read_csv(data_path)

print("=== Lima baris pertama ===")
print(df.head())

print("\n=== Info dataset ===")
print(df.info())

print("\n=== Statistik numerik ===")
print(df.describe())

# Konversi timestamp menjadi datetime dan jadikan index
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")

print("\n=== Rentang waktu data ===")
print(f"{df.index.min()} sampai {df.index.max()}")

print("\n=== Ringkasan Analitik Awal ===")
print(f"Suhu minimum       : {df['temperature_c'].min():.1f} C")
print(f"Suhu maksimum      : {df['temperature_c'].max():.1f} C")
print(f"Rata-rata suhu     : {df['temperature_c'].mean():.2f} C")

print(f"\nCO2 minimum        : {df['co2_ppm'].min()} ppm")
print(f"CO2 maksimum       : {df['co2_ppm'].max()} ppm")
print(f"Rata-rata CO2      : {df['co2_ppm'].mean():.2f} ppm")

print(f"\nDaya minimum       : {df['power_watt'].min()} watt")
print(f"Daya maksimum      : {df['power_watt'].max()} watt")
print(f"Rata-rata daya     : {df['power_watt'].mean():.2f} watt")
