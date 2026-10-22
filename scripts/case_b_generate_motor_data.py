"""
Hands-on 36 (Studi Kasus B): Generate Data Motor untuk Predictive Maintenance
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

3000 sampel getaran + arus dengan fase normal -> warning -> fault.
Output: data/synthetic/case_b_motor.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path("data/synthetic/case_b_motor.csv")


def main():
  OUTPUT.parent.mkdir(parents=True, exist_ok=True)
  rng = np.random.default_rng(42)
  n = 3000
  t = np.arange(n)

  vibration = 0.8 * np.sin(2 * np.pi * 0.03 * t) + rng.normal(0, 0.08, n)
  current = rng.normal(5.0, 0.2, n)

  status = np.array(["normal"] * n, dtype=object)

  status[1000:1800] = "warning"
  vibration[1000:1800] += 0.4 * np.sin(2 * np.pi * 0.03 * t[1000:1800])
  current[1000:1800] += rng.normal(0.6, 0.1, 800)

  status[1800:2600] = "fault"
  vibration[1800:2600] += 1.0 * np.sin(2 * np.pi * 0.03 * t[1800:2600])
  current[1800:2600] += rng.normal(1.5, 0.2, 800)

  df = pd.DataFrame({
      "sample_id": np.arange(n),
      "vibration": np.round(vibration, 5),
      "current_amp": np.round(current, 3),
      "status_label": status,
  })

  df.to_csv(OUTPUT, index=False)
  print("[SUKSES] Disimpan ke:", OUTPUT)
  print("[INFO] Distribusi status:", df["status_label"].value_counts().to_dict())


if __name__ == "__main__":
  main()
