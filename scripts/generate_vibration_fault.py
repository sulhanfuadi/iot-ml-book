"""
Hands-on 11: Generate Data Getaran Mesin dengan Fault Injection
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Sinyal getaran sintetis motor01: kondisi normal, lalu fault injection
(amplitudo naik, noise bertambah, spike sesaat). Output:
data/synthetic/vibration_fault_injection.csv dengan status_label.
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/synthetic/vibration_fault_injection.csv")


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  rng = np.random.default_rng(7)
  n = 3000
  t = np.arange(n)

  base_freq = 0.03
  normal_signal = 0.8 * np.sin(2 * np.pi * base_freq * t) + rng.normal(0, 0.08, n)

  fault_signal = normal_signal.copy()
  # Fault 1: amplitudo meningkat
  fault_signal[1000:2000] += 0.9 * np.sin(2 * np.pi * base_freq * t[1000:2000])
  # Fault 2: noise bertambah
  fault_signal[1500:2300] += rng.normal(0, 0.18, 800)
  # Fault 3: spike sesaat
  spike_idx = rng.choice(np.arange(1800, 2500), size=15, replace=False)
  fault_signal[spike_idx] += rng.uniform(1.0, 2.0, len(spike_idx))

  df = pd.DataFrame({
      "sample_id": np.arange(n),
      "machine_id": "motor01",
      "vibration": np.round(fault_signal, 5),
  })
  df["status_label"] = "normal"
  df.loc[1000:2499, "status_label"] = "fault"

  df.to_csv(OUTPUT_PATH, index=False)
  print(f"[SUKSES] Dataset getaran disimpan ke: {OUTPUT_PATH} ({len(df)} baris)")
  print(df.head())
  print("\n[INFO] Sekitar awal fault (sample 995-1005):")
  print(df.iloc[995:1005])
  print("\n[INFO] Sekitar area spike (sample 1795-1805):")
  print(df.iloc[1795:1805])
  print("\n[INFO] Distribusi label:")
  print(df["status_label"].value_counts())


if __name__ == "__main__":
  main()
