"""
Hands-on 8: Visualisasi Anomali
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/processed/room_sensor_anomaly_flags.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
  df = df.set_index("timestamp")

  series = [
      ("temperature_c", "Suhu (C)", "anomali_suhu.png"),
      ("co2_ppm", "CO2 (ppm)", "anomali_co2.png"),
      ("power_watt", "Daya (watt)", "anomali_daya.png"),
  ]
  mask = df[["anomaly_rule", "anomaly_zscore", "anomaly_iqr"]].any(axis=1)

  for col, ylabel, fname in series:
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df[col], label=col, color="steelblue")
    plt.scatter(
        df.index[mask], df.loc[mask, col],
        color="red", zorder=5, label="anomali",
    )
    plt.title(f"Deteksi Anomali - {ylabel}")
    plt.xlabel("Waktu")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / fname)
    plt.close()
    print(f"[SUKSES] outputs/figures/{fname}")


if __name__ == "__main__":
  main()
