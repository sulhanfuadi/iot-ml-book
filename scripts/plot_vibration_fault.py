from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH = Path("data/synthetic/vibration_fault_injection.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH)
plt.figure(figsize=(12, 5))
plt.plot(df["sample_id"], df["vibration"], linewidth=1)
plt.title("Sinyal Getaran dengan Fault Injection")
plt.xlabel("Sample ID")
plt.ylabel("Vibration")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "vibration_fault_injection.png")
plt.show()
