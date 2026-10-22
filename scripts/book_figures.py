"""
Figur persis sesuai listing buku (judul, label sumbu, ukuran, nama file).
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

  anomaly   Hands-on 8  : outputs/figures/anomaly_temperature_rule.png
  room      Hands-on 9  : outputs/figures/room_30days_sample.png
  vibration Hands-on 11 : outputs/figures/vibration_fault_injection.png
  features  Hands-on 14 : outputs/figures/room_temp_ma6.png
  rmsstd    Hands-on 15 : outputs/figures/vibration_features_rms_std.png

Pemakaian: python scripts/book_figures.py [--only anomaly|room|vibration|features|rmsstd]
Skrip plot lain di repositori menghasilkan versi yang lebih kaya (nama file berbeda).
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = Path("outputs/figures")


def fig_anomaly():
  df = pd.read_csv(Path("data/raw/room_sensor_anomaly.csv"))
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df["anomaly_rule"] = (
      (df["temperature_c"] > 35) |
      (df["co2_ppm"] > 1200) |
      (df["power_watt"] > 250)
  )
  plt.figure(figsize=(10, 5))
  plt.plot(df["timestamp"], df["temperature_c"], marker="o",
           label="Temperature")
  plt.scatter(
      df.loc[df["anomaly_rule"], "timestamp"],
      df.loc[df["anomaly_rule"], "temperature_c"],
      marker="x",
      s=100,
      label="Anomaly"
  )
  plt.title("Deteksi Anomali Suhu dengan Aturan Domain")
  plt.xlabel("Waktu")
  plt.ylabel("Suhu (C)")
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "anomaly_temperature_rule.png")
  plt.close()


def fig_room():
  df = pd.read_csv(Path("data/synthetic/room_30days.csv"))
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.set_index("timestamp")
  sample = df.loc["2026-01-01":"2026-01-03 23:59:59"]
  plt.figure(figsize=(12, 5))
  plt.plot(sample.index, sample["temperature_c"], label="Temperature")
  plt.plot(sample.index, sample["humidity_pct"], label="Humidity")
  plt.title("Data Sintetik Suhu-kelembaban (3 Hari Pertama)")
  plt.xlabel("Waktu")
  plt.ylabel("Nilai")
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_30days_sample.png")
  plt.close()


def fig_vibration():
  df = pd.read_csv(Path("data/synthetic/vibration_fault_injection.csv"))
  plt.figure(figsize=(12, 5))
  plt.plot(df["sample_id"], df["vibration"], linewidth=1)
  plt.title("Sinyal Getaran dengan Fault Injection")
  plt.xlabel("Sample ID")
  plt.ylabel("Vibration")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "vibration_fault_injection.png")
  plt.close()


def fig_features():
  df = pd.read_csv(Path("data/processed/room_30days_features.csv"))
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.set_index("timestamp")
  sample = df.loc["2026-01-01":"2026-01-03 23:59:59"]
  plt.figure(figsize=(12, 5))
  plt.plot(sample.index, sample["temperature_c"], label="Temp Raw")
  plt.plot(sample.index, sample["temp_ma_6"], label="Temp MA 6")
  plt.title("Suhu Mentah vs Moving Average")
  plt.xlabel("Waktu")
  plt.ylabel("Suhu (C)")
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "room_temp_ma6.png")
  plt.close()


def fig_rmsstd():
  df = pd.read_csv(Path("data/processed/vibration_window_features.csv"))
  plt.figure(figsize=(12, 5))
  plt.plot(df["window_start"], df["rms"], label="RMS")
  plt.plot(df["window_start"], df["std"], label="STD")
  plt.title("Fitur RMS dan STD per Jendela")
  plt.xlabel("Window Start")
  plt.ylabel("Nilai")
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "vibration_features_rms_std.png")
  plt.close()


FIGS = {"anomaly": fig_anomaly, "room": fig_room, "vibration": fig_vibration,
        "features": fig_features, "rmsstd": fig_rmsstd}


def main():
  parser = argparse.ArgumentParser(description="Figur persis buku")
  parser.add_argument("--only", choices=sorted(FIGS), default=None)
  args = parser.parse_args()
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  for name, fn in FIGS.items():
    if args.only in (None, name):
      fn()
      print(f"[SUKSES] figur '{name}' dibuat di {OUTPUT_DIR}")


if __name__ == "__main__":
  main()
