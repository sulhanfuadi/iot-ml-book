from pathlib import Path
import pandas as pd

INPUT_PATH = Path("data/synthetic/energy_daily_synthetic.csv")
OUTPUT_PATH = Path("data/synthetic/energy_daily_efficiency.csv")

df = pd.read_csv(INPUT_PATH)

mean_power = df["power_watt"].mean()

df["efficiency_label"] = df["power_watt"].apply(
    lambda x: "hemat" if x <= mean_power else "boros"
)

df.to_csv(OUTPUT_PATH, index=False)
print(df.head())
