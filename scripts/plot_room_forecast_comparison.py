from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_DIR = Path("data/processed/forecast_room")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
base_df = pd.read_csv(DATA_DIR / "baseline_predictions.csv")
lin_df = pd.read_csv(DATA_DIR / "linear_predictions.csv")
plot_df = pd.DataFrame({
    "actual": lin_df["actual"],
    "pred_last": base_df["pred_last"],
    "pred_ma": base_df["pred_ma"],
    "pred_linear": lin_df["pred_linear"]
})
sample = plot_df.iloc[:120].copy()
plt.figure(figsize=(12, 5))
plt.plot(sample.index, sample["actual"], label="Actual")
plt.plot(sample.index, sample["pred_last"], label="Last Value")
plt.plot(sample.index, sample["pred_ma"], label="Moving Average")
plt.plot(sample.index, sample["pred_linear"], label="Linear Regression")
plt.title("Forecasting Suhu Ruang")
plt.xlabel("Index waktu test")
plt.ylabel("Temperature (C)")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "room_forecast_compare.png")
plt.show()
