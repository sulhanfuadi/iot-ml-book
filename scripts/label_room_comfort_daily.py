from pathlib import Path
import pandas as pd

INPUT_PATH = Path("data/synthetic/room_daily_synthetic.csv")
OUTPUT_PATH = Path("data/synthetic/room_daily_labeled.csv")

df = pd.read_csv(INPUT_PATH)

df["comfort_label"] = df.apply(
    lambda row: "nyaman"
    if (24 <= row["temperature_c"] <= 28 and 45 <= row["humidity_pct"] <= 65)
    else "tidak_nyaman",
    axis=1
)

df.to_csv(OUTPUT_PATH, index=False)
print(df.head())
