"""
Hands-on 11: Visualisasi Fault pada Sinyal Getaran
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/synthetic/vibration_fault_injection.csv")
OUTPUT_DIR = Path("outputs/figures")


def main():
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  df = pd.read_csv(DATA_PATH)

  plt.figure(figsize=(12, 5))
  plt.plot(df["sample_id"], df["vibration"], lw=0.5, color="steelblue")
  fault = df[df["status_label"] == "fault"]
  plt.axvspan(fault["sample_id"].min(), fault["sample_id"].max(),
              color="tomato", alpha=0.15, label="zona fault")
  plt.title("Sinyal Getaran motor01 dengan Fault Injection")
  plt.xlabel("Sample")
  plt.ylabel("Amplitudo getaran")
  plt.legend()
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "vibration_fault.png")
  plt.close()
  print("[SUKSES] outputs/figures/vibration_fault.png")

  # Zoom area fault
  zoom = df[(df["sample_id"] >= 950) & (df["sample_id"] <= 2100)]
  plt.figure(figsize=(12, 4))
  warna = zoom["status_label"].map({"normal": "steelblue", "fault": "tomato"})
  plt.scatter(zoom["sample_id"], zoom["vibration"], c=warna, s=3)
  plt.title("Zoom Area Fault (sample 950-2100)")
  plt.xlabel("Sample")
  plt.ylabel("Amplitudo getaran")
  plt.tight_layout()
  plt.savefig(OUTPUT_DIR / "vibration_fault_zoom.png")
  plt.close()
  print("[SUKSES] outputs/figures/vibration_fault_zoom.png")


if __name__ == "__main__":
  main()
