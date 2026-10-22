"""
Hands-on 10: Visualisasi Konsumsi Energi Berbasis Jam Kerja
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/synthetic/energy_30days_labeled.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])

  # Profil daya seminggu pertama
  week = df[df["timestamp"] < "2026-01-08"]
  plt.figure(figsize=(12, 5))
  plt.plot(week["timestamp"], week["power_watt"], lw=0.8, color="darkorange")
  plt.axhline(350, color="red", ls="--", lw=1, label="ambang warning 350 W")
  plt.title("Konsumsi Energi - Minggu Pertama (pola jam kerja)")
  plt.xlabel("Waktu")
  plt.ylabel("Daya (watt)")
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "energy_week1.png")
  plt.close()
  print("[SUKSES] outputs/figures/energy_week1.png")

  # Rata-rata per jam: hari kerja vs akhir pekan
  df["hour"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60.0
  df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5
  profil = df.groupby(["is_weekend", "hour"])["power_watt"].mean().unstack(0)
  plt.figure(figsize=(10, 5))
  plt.plot(profil.index, profil[False], label="hari kerja", color="steelblue")
  plt.plot(profil.index, profil[True], label="akhir pekan", color="seagreen")
  plt.title("Profil Daya Rata-rata per Jam")
  plt.xlabel("Jam")
  plt.ylabel("Daya rata-rata (watt)")
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "energy_hourly_profile.png")
  plt.close()
  print("[SUKSES] outputs/figures/energy_hourly_profile.png")

  # Distribusi label
  counts = df["efficiency_label"].value_counts()
  plt.figure(figsize=(5, 5))
  plt.bar(counts.index, counts.values, color=["seagreen", "tomato"])
  plt.title("Distribusi Label Hemat / Boros")
  plt.ylabel("Jumlah sampel")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "energy_labels.png")
  plt.close()
  print("[SUKSES] outputs/figures/energy_labels.png")


if __name__ == "__main__":
  main()
