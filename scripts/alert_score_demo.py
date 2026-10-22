"""
Hands-on 31 (Bab 12): Versi Sederhana Berbasis Skor Anomali
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Pendekatan B buku: skor numerik dari aturan sederhana
(suhu > 31 +0.4, CO2 > 1100 +0.4, daya > 220 +0.2; alert bila skor >= 0.7).
Dijalankan pada dataset sintetis ruangan agar jumlah alert dapat diamati.
"""

import pandas as pd

DATA_PATH = "data/synthetic/room_classification_dataset.csv"


def anomaly_score(payload):
  score = 0.0
  if float(payload["temperature_c"]) > 31:
    score += 0.4
  if float(payload["co2_ppm"]) > 1100:
    score += 0.4
  if float(payload["power_watt"]) > 220:
    score += 0.2
  return score


def main():
  df = pd.read_csv(DATA_PATH)
  scores = df.apply(anomaly_score, axis=1)
  alerts = df[scores >= 0.7]
  print(f"Total baris : {len(df)}")
  print(f"Alert (skor >= 0.7): {len(alerts)} ({len(alerts) / len(df) * 100:.2f}%)")
  print("Distribusi skor:")
  print(scores.round(1).value_counts().sort_index().to_string())
  print("\nContoh alert:")
  print(alerts.head(5).to_string(index=False))


if __name__ == "__main__":
  main()
