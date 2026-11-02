# Tes B (Raspberry Pi) via emulasi ARM64 - 2 November 2026

Pengujian `prompt_test_lokal.md` Tes B dijalankan tanpa perangkat Raspberry Pi fisik
(pengguna mengonfirmasi tidak punya hardware) memakai emulasi QEMU user-mode aarch64
di host x86_64 Linux:

- Emulator: qemu-aarch64-static 7.2.0 (user-mode, bukan virtualisasi penuh).
- Python: 3.11.18 aarch64 (python-build-standalone); Raspberry Pi OS 64-bit bookworm
  membawa Python 3.11.x, jadi versi minor sama.
- Pustaka sistem: paket `.deb` arm64 Debian bookworm asli (libc6 2.36, libssl3, dst).
- Broker: biner arm64 asli `mosquitto` 2.0.11 dari repo Debian bookworm (versi yang
  sama dengan yang dipasang `apt` di Raspberry Pi OS bookworm), dijalankan di bawah QEMU.

Ini BUKAN pengujian perangkat keras fisik: GPIO, kamera, performa CPU/RAM nyata, dan
`systemctl enable --now` tidak tercakup. Angka waktu inferensi adalah angka emulasi
di host x86_64, bukan patokan kecepatan Raspberry Pi.

## Hasil per langkah Tes B

| Langkah | Status | Bukti |
| --- | --- | --- |
| 1. apt install mosquitto mosquitto-clients python3-venv | OK (tersedia) | Ketiga paket ada di indeks repo Debian bookworm arm64: mosquitto 2.0.11-1.2+deb12u2, mosquitto-clients 2.0.11-1.2+deb12u2, python3-venv 3.11.2 (Python 3.11). Biner arm64 mosquitto 2.0.11 asli berjalan dan lolos pub/sub. systemctl tidak diuji (bukan bagian skrip buku). |
| 2. venv + pip install -r requirements.txt | OK, satu catatan | Semua paket terpasang untuk aarch64 cp311: pandas 3.1.0, numpy 2.4.6, matplotlib 3.11.2, seaborn 0.13.2, scikit-learn 1.9.1, amqtt 0.12.1, joblib 1.6.0, influxdb-client 1.50.0, jupyter, nbconvert. `tensorflow>=2.16` -> 2.21.0 KINI punya wheel aarch64 resmi di PyPI dan berhasil impor + komputasi (matmul OK) - kabar baik, dokumentasi lama yang menyatakan tensorflow gagal di Pi sudah usang. `paho-mqtt 1.6.1` hanya tersedia sebagai sdist (berlaku di semua platform, bukan khusus Pi); tetap terpasang dan impor OK. |
| 3. test_env.py + publish/subscribe | OK | `scripts/test_env.py` mencetak "Lingkungan Python IoT Analytics siap digunakan." `scripts/mqtt/publish_sensor.py` (apa adanya) publish ke biner arm64 mosquitto; `mosquitto_sub -t kampus/lab1/room01/telemetry` menerima payload JSON room01. |
| 4. HO28-29 + waktu inferensi | OK | `simulate_edge_inference_sklearn.py`: 324/324 sampel terprediksi, jalan penuh ~82 s (termasuk sleep 0,2 s/sampel dari buku). Inferensi RandomForest per sampel: mean 31,65 ms, median 31,28 ms, p95 35,04 ms (angka emulasi). `edge_room_classifier_project.py`: 30 prediksi ke `outputs/reports/edge_room_predictions.csv`, elapsed 15,3 s, peak RSS ~298 MB (proses emulasi). Peringatan InconsistentVersionWarning muncul karena model disimpan dengan scikit-learn 1.7.2 sedangkan yang terpasang 1.9.1 (requirements tidak mem-pin); prediksi tetap berjalan. |
| 5. nbconvert notebooks/03_subscribe_mqtt.ipynb | OK | Dieksekusi penuh dengan kernel arm64 dan broker mosquitto arm64 asli (run_broker.py menemukan mosquitto di PATH): publish, subscribe, wildcard `kampus/lab1/+/telemetry`, dan validasi payload semua berjalan; 0 sel error. |

## Temuan bug nyata dan perbaikannya

`scripts/simulate_edge_inference_tflite.py` sebelumnya GAGAL di semua platform (bukan
khas Pi): `feature_cols` hanya mengecualikan timestamp/device_id/target_abnormal,
sehingga kolom string `status_label` ikut dan `astype("float32")` melempar
`ValueError: could not convert string to float: 'warning'` pada CSV repo sendiri
(`data/processed/classification_room/test.csv`). Diperbaiki dengan mengecualikan juga
`status_label` dan `is_anomaly` -> 17 fitur, persis cocok dengan input model `[1, 17]`;
inferensi TFLite (delegate XNNPACK aarch64) berjalan, mean 0,19 ms/sampel (emulasi).
Regresi: `python scripts/test_edge_tflite_features.py`. Logika inferensi tetap persis
buku; yang berubah hanya daftar kolom yang dikecualikan.

## Batasan yang tetap terbuka

- Belum ada pengujian di Raspberry Pi fisik (tidak ada perangkat).
- `sudo apt ...` dan `systemctl enable --now mosquitto` diverifikasi pada level indeks
  repo + biner, bukan lewat apt/systemd sungguhan di Raspberry Pi OS.
- Performa (ms/sampel, RSS) adalah angka emulasi QEMU, bukan ukuran perangkat Pi.
