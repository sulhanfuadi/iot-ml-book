from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
# baca data
data_path = Path("data/raw/room_sensor_dummy.csv")
df = pd.read_csv(data_path)
# ubah timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")
# buat folder output jika belum ada
output_dir = Path("outputs/figures")
output_dir.mkdir(parents=True, exist_ok=True)
# plot suhu
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["temperature_c"], marker="o")
plt.title("Perubahan Suhu Ruangan")
plt.xlabel("Waktu")
plt.ylabel("Suhu (C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "plot_suhu_ruangan.png")
plt.show()
