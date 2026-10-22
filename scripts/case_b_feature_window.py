"""
Hands-on 36 (Studi Kasus B): Ekstraksi Fitur per Jendela
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Window 50 sampel, step 25: mean/std/RMS/peak-to-peak getaran + mean/max arus.
Output: data/processed/case_b_motor_features.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

INPUT = Path("data/synthetic/case_b_motor.csv")
OUTPUT = Path("data/processed/case_b_motor_features.csv")


def main():
  OUTPUT.parent.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(INPUT)

  window_size = 50
  step = 25
  rows = []
  for start in range(0, len(df) - window_size + 1, step):
    end = start + window_size
    w = df.iloc[start:end]

    vib = w["vibration"].values
    cur = w["current_amp"].values

    row = {
        "window_start": int(w["sample_id"].iloc[0]),
        "window_end": int(w["sample_id"].iloc[-1]),
        "vib_mean": np.mean(vib),
        "vib_std": np.std(vib),
        "vib_rms": np.sqrt(np.mean(vib ** 2)),
        "vib_ptp": np.ptp(vib),
        "cur_mean": np.mean(cur),
        "cur_max": np.max(cur),
        "status_label": w["status_label"].mode()[0],
    }
    rows.append(row)

  feat_df = pd.DataFrame(rows)
  feat_df.to_csv(OUTPUT, index=False)
  print("[SUKSES] Disimpan ke:", OUTPUT)
  print(f"[INFO] {len(feat_df)} jendela fitur diekstrak.")


if __name__ == "__main__":
  main()
