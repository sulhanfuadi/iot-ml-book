from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# 1. Baca data
df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
# 2. Pilih fitur
X = df[["temperature_c", "humidity_pct"]].copy()
# 3. Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# 4. Coba beberapa nilai K
results = []
for k in range(2, 6):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    results.append((k, score))
print("=== Silhouette Score untuk beberapa K ===")
for k, score in results:
    print(f"K={k}, silhouette={score:.4f}")
# 5. Pilih K, misalnya 3
best_k = 3
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["cluster_kmeans"] = kmeans.fit_predict(X_scaled)
print("\nJumlah data per cluster:")
print(df["cluster_kmeans"].value_counts())
# 6. Simpan hasil
df.to_csv("outputs/reports/room_kmeans_cluster.csv", index=False)
# 7. Visualisasi
plt.figure(figsize=(8, 6))
plt.scatter(
    df["temperature_c"],
    df["humidity_pct"],
    c=df["cluster_kmeans"],
    s=10
)
plt.title("K-Means Clustering: Suhu vs kelembaban")
plt.xlabel("Temperature (C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig("outputs/figures/room_kmeans_scatter.png")
plt.show()
