"""
Hands-on 15: Fitur Getaran Sederhana untuk Deteksi Kondisi Mesin
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Fitur per jendela (window=50, step=25): mean, std, min, max, range, RMS,
peak-to-peak, kurtosis sederhana (tanpa scipy). Label mayoritas per jendela.
Input : data/synthetic/vibration_fault_injection.csv
Output: data/processed/vibration_window_features.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/synthetic/vibration_fault_injection.csv")
OUTPUT_PATH = Path("data/processed/vibration_window_features.csv")
WINDOW_SIZE = 50
STEP_SIZE = 25


def compute_features(signal: np.ndarray) -> dict:
  mean_val = np.mean(signal)
  std_val = np.std(signal)
  min_val = np.min(signal)
  max_val = np.max(signal)
  range_val = max_val - min_val
  rms_val = np.sqrt(np.mean(signal ** 2))
  ptp_val = np.ptp(signal)  # peak to peak

  # Kurtosis sederhana tanpa scipy
  centered = signal - mean_val
  if std_val == 0:
    kurtosis_val = 0.0
  else:
    kurtosis_val = np.mean((centered / std_val) ** 4)

  return {
      "mean": mean_val,
      "std": std_val,
      "min": min_val,
      "max": max_val,
      "range": range_val,
      "rms": rms_val,
      "peak_to_peak": ptp_val,
      "kurtosis": kurtosis_val,
  }


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT_PATH)

  records = []
  for start in range(0, len(df) - WINDOW_SIZE + 1, STEP_SIZE):
    end = start + WINDOW_SIZE
    window = df.iloc[start:end]
    signal = window["vibration"].values
    features = compute_features(signal)
    label = window["status_label"].mode()[0]
    row = {
        "window_start": int(window["sample_id"].iloc[0]),
        "window_end": int(window["sample_id"].iloc[-1]),
        "machine_id": window["machine_id"].iloc[0],
        "status_label": label,
        **features,
    }
    records.append(row)

  features_df = pd.DataFrame(records)
  features_df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Fitur getaran disimpan ke: {OUTPUT_PATH} ({len(features_df)} jendela)")
  print(features_df.head())
  print("\n[INFO] Distribusi label:")
  print(features_df["status_label"].value_counts())


if __name__ == "__main__":
  main()
