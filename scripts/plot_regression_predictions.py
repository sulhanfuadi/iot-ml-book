from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
DATA_DIR = Path("data/processed/regression_energy")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_linear = pd.read_csv(DATA_DIR / "pred_linear_test.csv")
df_rf = pd.read_csv(DATA_DIR / "pred_rf_test.csv")
# Gabungkan
plot_df = pd.DataFrame({
    "actual": df_linear["actual"],
    "pred_linear": df_linear["predicted_linear"],
    "pred_rf": df_rf["predicted_rf"]
})
sample = plot_df.iloc[:120].copy()    # ambil subset agar grafik nyaman dibaca
plt.figure(figsize=(12, 5))
plt.plot(sample.index, sample["actual"], label="Actual")
plt.plot(sample.index, sample["pred_linear"], label="Linear Regression")
plt.plot(sample.index, sample["pred_rf"], label="Random Forest Regressor")
plt.title("Prediksi Energi: Aktual vs Model")
plt.xlabel("Index waktu test")
plt.ylabel("Power Watt")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "regression_predictions_compare.png")
plt.show()
