from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
INPUT_PATH = Path("data/synthetic/room_30days.csv")
# 1. Baca data
df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
# 2. Pilih fitur
X = df[["temperature_c", "humidity_pct"]].copy()
# 3. Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# 4. DBSCAN
dbscan = DBSCAN(eps=0.35, min_samples=10)
df["cluster_dbscan"] = dbscan.fit_predict(X_scaled)
print("=== Hasil DBSCAN ===")
print(df["cluster_dbscan"].value_counts().sort_index())
# 5. Simpan hasil
df.to_csv("outputs/reports/room_dbscan_cluster.csv", index=False)
# 6. Visualisasi
plt.figure(figsize=(8, 6))
plt.scatter(
    df["temperature_c"],
    df["humidity_pct"],
    c=df["cluster_dbscan"],
    s=10
)
plt.title("DBSCAN: Suhu vs kelembaban")
plt.xlabel("Temperature (C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig("outputs/figures/room_dbscan_scatter.png")
plt.show()
