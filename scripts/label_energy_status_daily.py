from pathlib import Path
import pandas as pd

INPUT_PATH = Path("data/synthetic/energy_daily_synthetic.csv")
OUTPUT_PATH = Path("data/synthetic/energy_daily_labeled.csv")

df = pd.read_csv(INPUT_PATH)

def label_energy(power):
    if power < 250:
        return "normal"
    elif power < 400:
        return "warning"
    return "fault"

df["status_label"] = df["power_watt"].apply(label_energy)
df.to_csv(OUTPUT_PATH, index=False)
print(df.head())
