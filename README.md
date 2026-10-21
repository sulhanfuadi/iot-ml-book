# iot-ml-book

Repositori praktikum Sistem Tertanam - Departemen Informatika Universitas Diponegoro (2026).
Referensi: *IoT Terintegrasi dengan Machine Learning & Data Analytics* oleh Onno W. Purbo.

---

## Struktur Direktori

```text
iot-ml-book/
├── .venv/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 00_uji_lingkungan.ipynb
├── scripts/
│   └── uji_lingkungan.py
├── outputs/
│   ├── figures/
│   └── reports/
├── requirements.txt
└── README.md
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
Buka Visual Studio Code pada folder `iot-ml-book`, buka file `notebooks/00_uji_lingkungan.ipynb`, lalu pilih kernel **Python (.venv iot-ml-book)**.
