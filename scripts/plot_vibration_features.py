from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
INPUT_PATH = Path("data/processed/vibration_window_features.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
plt.figure(figsize=(12, 5))
plt.plot(df["window_start"], df["rms"], label="RMS")
plt.plot(df["window_start"], df["std"], label="STD")
plt.title("Fitur RMS dan STD per Jendela")
plt.xlabel("Window Start")
plt.ylabel("Nilai")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "vibration_features_rms_std.png")
plt.show()
