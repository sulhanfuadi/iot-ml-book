from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
INPUT_PATH = Path("data/processed/room_30days_pca.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
plt.figure(figsize=(8, 6))
plt.scatter(df["pc1"], df["pc2"], s=10)
plt.title("Visualisasi PCA: PC1 vs PC2")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "room_pca_scatter.png")
plt.show()
