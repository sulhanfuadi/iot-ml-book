from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# 1. Baca data dummy
data_path = Path("data/raw/room_sensor_dummy.csv")
df = pd.read_csv(data_path)

# 2. Konversi kolom waktu & set index
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")

# 3. Direktori output gambar
output_dir = Path("outputs/figures")
output_dir.mkdir(parents=True, exist_ok=True)

# 4. Plot Suhu Ruangan Utama
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["temperature_c"], marker="o", color="#111111", linewidth=1.5)
plt.title("Perubahan Suhu Ruangan")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(output_dir / "plot_suhu_ruangan.png", dpi=150)
plt.close()

# 5. Plot Individu Tiap Variabel (Suhu, Kelembaban, CO2)
# Suhu
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["temperature_c"], marker="o", color="#111111")
plt.title("Suhu Ruangan")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(output_dir / "temperature.png", dpi=150)
plt.close()

# Kelembaban
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["humidity_pct"], marker="o", color="#333333")
plt.title("Kelembaban Ruangan")
plt.xlabel("Waktu")
plt.ylabel("Kelembaban (%)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(output_dir / "humidity.png", dpi=150)
plt.close()

# CO2
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["co2_ppm"], marker="o", color="#222222")
plt.title("Kadar CO2 Ruangan")
plt.xlabel("Waktu")
plt.ylabel("CO2 (ppm)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(output_dir / "co2.png", dpi=150)
plt.close()

# 6. Scatter Plot Korelasi Suhu vs CO2
plt.figure(figsize=(7, 5))
plt.scatter(df["temperature_c"], df["co2_ppm"], color="#111111", alpha=0.8)
plt.title("Relasi Suhu dan CO2")
plt.xlabel("Suhu (C)")
plt.ylabel("CO2 (ppm)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(output_dir / "temperature_vs_co2.png", dpi=150)
plt.close()

# 7. Simpan data hasil olahan ke data/processed/ (halaman 63)
processed_path = Path("data/processed/room_sensor_clean.csv")
processed_path.parent.mkdir(parents=True, exist_ok=True)
df.reset_index().to_csv(processed_path, index=False)

print("[SUKSES] Visualisasi tersimpan di outputs/figures/:")
print(" - plot_suhu_ruangan.png")
print(" - temperature.png")
print(" - humidity.png")
print(" - co2.png")
print(" - temperature_vs_co2.png")
print(f"[SUKSES] Data bersih disimpan ke: {processed_path}")
