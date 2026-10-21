# iot-ml-book

Repositori praktikum Sistem Tertanam - Departemen Informatika Universitas Diponegoro (2026).

---

## Buku & Dokumen Referensi Utama

Seluruh implementasi hands-on, arsitektur kode, skrip simulator, serta model analitik dan machine learning di repositori ini mengacu langsung pada dokumen rujukan yang tersimpan di dalam folder `docs/`:

1. **Buku Utama:**
   - Path: `docs/Onno W. Purbo, IoT Terintegrasi dengan Machine Learning Data Analytics, 2026.pdf`
   - Penulis: Onno W. Purbo (ITTS / OnnoCenter, 2026)
   - Deskripsi: Sumber acuan utama (536 halaman) yang mencakup Hands-on 1 hingga Hands-on 40 (Fondasi Praktis IoT Analytics, Data Analytics Python, Machine Learning IoT, Integrasi End-to-End Open Source, dan Studi Kasus Praktis).
2. **Slide Praktikum:**
   - Path: `docs/08. Sister IF 2026 - Persiapan Lingkungan Kerja.pdf`
   - Pemateri: Indra Waspada (Universitas Diponegoro, 2026)
   - Deskripsi: Slide panduan silabus dan persiapan lingkungan kerja praktikum.

---

## Struktur Direktori

```text
iot-ml-book/
├── .venv/                 # Virtual environment Python
├── data/
│   ├── raw/               # Dataset sensor mentah
│   └── processed/         # Dataset hasil olahan/pembersihan
├── docs/                  # Buku referensi utama dan slide kuliah
│   ├── 08. Sister IF 2026 - Persiapan Lingkungan Kerja.pdf
│   └── Onno W. Purbo, IoT Terintegrasi dengan Machine Learning Data Analytics, 2026.pdf
├── notebooks/             # Jupyter Notebook eksperimen
│   └── 00_uji_lingkungan.ipynb
├── outputs/
│   ├── figures/           # Hasil visualisasi grafik
│   └── reports/           # Laporan dan metrik model
├── scripts/               # Skrip Python executable
│   ├── uji_lingkungan.py
│   └── baseline_evaluation.py
├── requirements.lock.txt
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
Buka Visual Studio Code pada direktori `iot-ml-book`, buka file `notebooks/00_uji_lingkungan.ipynb`, lalu pilih kernel **Python (.venv iot-ml-book)**.
