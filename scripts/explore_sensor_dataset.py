from pathlib import Path
import pandas as pd
DATA_PATH = Path("data/raw/room_sensor_week.csv")
df = pd.read_csv(DATA_PATH)
print("=== 5 baris pertama ===")
print(df.head())
print("\n=== Ukuran data ===")
print(df.shape)
print("\n=== Nama kolom ===")
print(df.columns.tolist())
print("\n=== Info dataset ===")
print(df.info())
print("\n=== Statistik numerik ===")
print(df.describe(include="all"))
