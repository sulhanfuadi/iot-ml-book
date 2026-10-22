"""
Hands-on 32 (Bab 13): Memonitor Perubahan Distribusi Data (Data Drift)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Baseline: 14 hari pertama. Current: 7 hari terakhir.
Bandingkan mean/std/median + histogram, dengan indikator drift sederhana.
Output: outputs/reports/data_distribution_monitor.csv, outputs/figures/dist_compare_*.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("outputs")

# Ambang indikator drift sederhana (satuan fitur)
DRIFT_THRESHOLD = 1.0


def main():
  (OUTPUT_DIR / "reports").mkdir(parents=True, exist_ok=True)
  fig_dir = OUTPUT_DIR / "figures"
  fig_dir.mkdir(parents=True, exist_ok=True)

  df = pd.read_csv(INPUT_PATH)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.sort_values("timestamp")

  # Baseline: 14 hari pertama
  baseline_end = df["timestamp"].min() + pd.Timedelta(days=14)
  baseline_df = df[df["timestamp"] < baseline_end].copy()

  # Current: 7 hari terakhir
  current_start = df["timestamp"].max() - pd.Timedelta(days=7)
  current_df = df[df["timestamp"] >= current_start].copy()

  print(f"[INFO] Baseline: {len(baseline_df)} baris, Current: {len(current_df)} baris")

  features = ["temperature_c", "humidity_pct"]
  results = []
  for col in features:
    baseline_mean = baseline_df[col].mean()
    current_mean = current_df[col].mean()
    baseline_std = baseline_df[col].std()
    current_std = current_df[col].std()
    baseline_median = baseline_df[col].median()
    current_median = current_df[col].median()

    mean_shift = current_mean - baseline_mean
    std_shift = current_std - baseline_std

    results.append({
        "feature": col,
        "baseline_mean": baseline_mean,
        "current_mean": current_mean,
        "mean_shift": mean_shift,
        "baseline_std": baseline_std,
        "current_std": current_std,
        "std_shift": std_shift,
        "baseline_median": baseline_median,
        "current_median": current_median,
    })

  results_df = pd.DataFrame(results)
  results_df.to_csv(OUTPUT_DIR / "reports" / "data_distribution_monitor.csv", index=False)

  print("=== Ringkasan perubahan distribusi ===")
  print(results_df.round(3).to_string(index=False))

  # Indikator drift sederhana
  print("\n=== Indikator drift ===")
  for _, row in results_df.iterrows():
    if abs(row["mean_shift"]) > DRIFT_THRESHOLD:
      print(f"[PERINGATAN] {row['feature']}: mean bergeser signifikan "
            f"({row['mean_shift']:+.3f})")
    else:
      print(f"[INFO] {row['feature']}: tidak ada drift mencolok "
            f"({row['mean_shift']:+.3f})")

  # Visualisasi histogram
  for col in features:
    plt.figure(figsize=(8, 5))
    plt.hist(baseline_df[col], bins=30, alpha=0.6, label="Baseline")
    plt.hist(current_df[col], bins=30, alpha=0.6, label="Current")
    plt.title(f"Perbandingan Distribusi {col}")
    plt.xlabel(col)
    plt.ylabel("Frekuensi")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / f"dist_compare_{col}.png")
    plt.close()
    print(f"[SUKSES] outputs/figures/dist_compare_{col}.png")


if __name__ == "__main__":
  main()
