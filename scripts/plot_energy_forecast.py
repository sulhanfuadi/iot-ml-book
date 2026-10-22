from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_DIR = Path("data/processed/regression_energy")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
lin_df = pd.read_csv(DATA_DIR / "energy_linear_predictions.csv")
rf_df = pd.read_csv(DATA_DIR / "energy_rf_predictions.csv")
plot_df = pd.DataFrame({
    "actual": lin_df["actual"],
    "pred_linear": lin_df["pred_linear"],
    "pred_rf": rf_df["pred_rf"]
})
sample = plot_df.iloc[:150].copy()
plt.figure(figsize=(12, 5))
plt.plot(sample.index, sample["actual"], label="Actual")
plt.plot(sample.index, sample["pred_linear"], label="Linear Regression")
plt.plot(sample.index, sample["pred_rf"], label="Random Forest")
plt.title("Forecasting Konsumsi Energi")
plt.xlabel("Index waktu test")
plt.ylabel("Power Watt")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "energy_forecast_compare.png")
plt.show()
