"""
Hands-on 10: Label Hemat / Boros untuk Data Energi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Label: "hemat" jika power_watt <= rata-rata, "boros" jika di atasnya.
Input : data/synthetic/energy_30days.csv
Output: data/synthetic/energy_30days_labeled.csv
"""

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/synthetic/energy_30days.csv")
OUTPUT_PATH = Path("data/synthetic/energy_30days_labeled.csv")


def main():
  df = pd.read_csv(INPUT_PATH)
  mean_power = df["power_watt"].mean()
  df["efficiency_label"] = df["power_watt"].apply(
      lambda x: "hemat" if x <= mean_power else "boros"
  )
  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Label hemat/boros disimpan ke: {OUTPUT_PATH}")
  print(f"[INFO] Ambang rata-rata: {mean_power:.2f} watt")
  print(df["efficiency_label"].value_counts())
  print(df.head())


if __name__ == "__main__":
  main()
