# IoT ML Data Analytics

Repositori praktikum Sistem Tertanam - Departemen Informatika Universitas Diponegoro (2026).
Referensi: *IoT Terintegrasi dengan Machine Learning & Data Analytics* oleh Onno W. Purbo.

---

## Struktur Direktori

```text
IoT_ML_DataAnalytics/
├── .venv/                 # Virtual environment Python
├── data/
│   ├── raw/               # Dataset mentah dari sensor / simulator
│   └── processed/         # Dataset hasil preprocessing
├── docs/                  # Dokumentasi praktikum
├── notebooks/             # Jupyter Notebook eksplorasi dan analisis
│   └── 00_uji_lingkungan.ipynb
├── outputs/
│   ├── figures/           # Plot visualisasi (PNG, SVG, PDF)
│   └── reports/           # Laporan hasil analitik
├── scripts/               # Skrip Python executable
│   └── uji_lingkungan.py
├── tmp/                   # File sementara
├── .gitignore
├── README.md
├── requirements.lock.txt
└── requirements.txt
```

---

## Setup dan Aktivasi Lingkungan Kerja

### 1. Aktivasi Virtual Environment
```bash
# macOS / Linux
source .venv/bin/activate
```

### 2. Verifikasi Instalasi Paket
```bash
python scripts/uji_lingkungan.py
```
Output yang diharapkan:
```text
Notebook aktif dan siap dipakai.
```

### 3. Menjalankan Jupyter Notebook
Buka Visual Studio Code, buka file `notebooks/00_uji_lingkungan.ipynb`, lalu pilih kernel **Python (.venv IoT_ML_DataAnalytics)** di pojok kanan atas editor.
