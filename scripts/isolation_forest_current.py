from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
INPUT_PATH = Path("data/synthetic/current_sensor_anomaly.csv")
df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
# Pilih fitur
feature_cols = ["current_amp", "voltage", "power_watt"]
X = df[feature_cols].copy()
# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.03,
    random_state=42
)
df["iforest_pred"] = model.fit_predict(X_scaled)
# sklearn: -1 anomali, 1 normal
df["iforest_anomaly"] = (df["iforest_pred"] == -1).astype(int)
print("=== Hasil Isolation Forest ===")
print(df["iforest_anomaly"].value_counts())
# Simpan
df.to_csv("outputs/reports/current_iforest_results.csv", index=False)
# Visualisasi
plt.figure(figsize=(12, 5))
plt.plot(df["timestamp"], df["current_amp"], label="Current (A)")
plt.scatter(
    df.loc[df["iforest_anomaly"] == 1, "timestamp"],
    df.loc[df["iforest_anomaly"] == 1, "current_amp"],
    marker="x",
    s=80,
    label="Anomaly"
)
plt.title("Isolation Forest - Deteksi Anomali Arus Listrik")
plt.xlabel("Waktu")
plt.ylabel("Current (A)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("outputs/figures/current_iforest_anomaly.png")
plt.show()
