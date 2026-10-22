from pathlib import Path
import pandas as pd
INPUT_PATH = Path("data/synthetic/energy_30days.csv")
OUTPUT_PATH = Path("data/synthetic/energy_30days_labeled.csv")
df = pd.read_csv(INPUT_PATH)
mean_power = df["power_watt"].mean()
df["efficiency_label"] = df["power_watt"].apply(
    lambda x: "hemat" if x <= mean_power else "boros"
)
df.to_csv(OUTPUT_PATH, index=False)
print(f"Label hemat/boros disimpan ke: {OUTPUT_PATH}")
print(df.head())
