from pathlib import Path
import numpy as np
import pandas as pd
INPUT_PATH = Path("data/synthetic/vibration_fault_injection.csv")
OUTPUT_PATH = Path("data/processed/vibration_window_features.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
window_size = 50
step_size = 25
records = []
def compute_features(signal: np.ndarray) -> dict:
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    min_val = np.min(signal)
    max_val = np.max(signal)
    range_val = max_val - min_val
    rms_val = np.sqrt(np.mean(signal ** 2))
    ptp_val = np.ptp(signal) # peak to peak
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
for start in range(0, len(df) - window_size + 1, step_size):
    end = start + window_size
    window = df.iloc[start:end]
    signal = window["vibration"].values
    features = compute_features(signal)
    # Label mayoritas dalam jendela
    label = window["status_label"].mode()[0]
    row = {
        "window_start": int(window["sample_id"].iloc[0]),
        "window_end": int(window["sample_id"].iloc[-1]),
        "machine_id": window["machine_id"].iloc[0],
        "status_label": label,
        **features
    }
    records.append(row)
features_df = pd.DataFrame(records)
features_df.to_csv(OUTPUT_PATH, index=False)
print(f"Fitur getaran disimpan ke: {OUTPUT_PATH}")
print(features_df.head())
print("\nDistribusi label:")
print(features_df["status_label"].value_counts())
