Kamu menguji repo https://github.com/sulhanfuadi/iot-ml-book (branch main) di mesin lokal ini. Repo ini adalah praktikum buku "IoT Terintegrasi dengan Machine Learning Data Analytics" (Onno W. Purbo). Jangan ubah kode kecuali ada bug nyata; kalau ada, catat dulu, perbaiki di branch baru dari main, buka PR, merge dengan `gh pr merge --merge`, jangan hapus branch. Jangan pakai emoji. Jangan keluarkan uang. Laporkan jujur: apa yang lolos, apa yang gagal, apa yang tidak bisa diuji, dengan keluaran perintah sebagai bukti.

Persiapan umum
1. git clone https://github.com/sulhanfuadi/iot-ml-book && cd iot-ml-book
2. python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   (paho-mqtt harus 1.6.x. Cek: pip show paho-mqtt. Jangan pasang 2.x.)
3. Baca README bagian "Setup di macOS", "Mosquitto, InfluxDB dan Grafana" dan "Skrip persis buku".

TES A - Docker compose (mesin dengan Docker)
1. cd docker && docker compose up -d && docker compose ps  (mosquitto 1883, influxdb 8086, grafana 3000 harus Up)
2. Cek InfluxDB: buka http://localhost:8086, pastikan org iotlab dan bucket sensor_data ada. Token default compose adalah GANTI_DENGAN_TOKEN_ANDA (sama dengan default skrip dan buku).
3. Cek Grafana: http://localhost:3000, datasource InfluxDB harus sehat (Save and test) dan dashboard "iot-ml-capstone" (8 panel) muncul otomatis.
4. Dari root repo, kirim data: python scripts/mqtt/run_broker.py TIDAK perlu (broker sudah di Docker). Jalankan:
   python scripts/publisher_room_simulator.py &   (skrip buku apa adanya: while True, tanpa flag; hentikan dengan kill atau Ctrl+C)
   python scripts/pipeline_room_with_alert.py   (skrip buku apa adanya: loop_forever, menulis ke InfluxDB dengan token bawaan GANTI_DENGAN_TOKEN_ANDA; biarkan sekitar 30 detik lalu Ctrl+C)
   lalu cek data masuk di Influx (Data Explorer, measurement room_pipeline dan room_alerts) dan panel Grafana terisi.
5. Ulangi untuk capstone: scripts/publishers/capstone_publisher.py (&) dan scripts/subscribers/capstone_subscriber_with_alert.py (measurement capstone_device_monitoring dan capstone_alerts). Catatan: timestamp Influx berpresisi detik, pesan dalam detik yang sama menimpa satu sama lain; ini sifat skrip buku.
6. docker compose down. Laporkan setiap langkah yang gagal beserta log (docker compose logs).

TES B - Raspberry Pi (Raspberry Pi OS 64-bit, Python 3.10+)
1. sudo apt update && sudo apt install -y mosquitto mosquitto-clients python3-venv && sudo systemctl enable --now mosquitto
2. Clone, buat venv, pip install -r requirements.txt. Catat bila tensorflow gagal dipasang di Pi (itu hanya untuk Hands-on 26 sampai 29 bagian LSTM/TFLite); catat paket mana yang butuh alternatif (misal tflite-runtime).
3. Jalankan: python scripts/test_env.py, lalu mosquitto_sub -t 'kampus/lab1/room01/telemetry' & dan python scripts/mqtt/publish_sensor.py (Ctrl+C setelah beberapa pesan).
4. Jalankan HO28-29 (scripts/simulate_edge_inference_sklearn.py, scripts/edge_room_classifier_project.py) dan ukur waktu inferensi. Catat penggunaan CPU/RAM.
5. Jalankan notebook yang bisa: jupyter nbconvert --to notebook --execute notebooks/03_subscribe_mqtt.ipynb (butuh broker aktif). Laporkan hasil.

TES C - macOS (Apple Silicon atau Intel, Python 3.10-3.12)
1. brew install mosquitto python@3.12 (opsional: brew install --cask docker)
2. Clone, venv, pip install -r requirements.txt. Catat bila tensorflow gagal (Apple Silicon butuh Python 3.10-3.12).
3. Jalankan broker: python scripts/mqtt/run_broker.py (harus memakai Mosquitto dari Homebrew; IOT_BROKER=amqtt memaksa amqtt).
4. Jalankan semua notebook berurutan: for nb in notebooks/*.ipynb; do jupyter nbconvert --to notebook --execute --output-dir /tmp/mac-out "$nb" || echo "FAIL $nb"; done
   Catat notebook yang gagal dan penyebabnya (path, backend matplotlib, plt.show yang memblokir, port).
5. Jalankan skrip persis buku: python scripts/test_env.py; python scripts/check_label_distribution.py; python scripts/compare_synthetic_vs_real.py; python scripts/publish_csv_to_mqtt.py bersama python scripts/subscribe_verify_mqtt.py. Semua skrip MQTT buku berjalan terus; hentikan dengan Ctrl+C. Notebook 03, 04, 30-32, 36, 39-41 menjalankannya sebagai subprocess dengan timeout eksternal dan butuh InfluxDB aktif (org iotlab, bucket sensor_data, token GANTI_DENGAN_TOKEN_ANDA) untuk notebook 31, 32, 36, 39, 40, 41.

Laporan akhir (satu per tes A, B, C): tabel langkah | status (OK/GAGAL/TIDAK DIUJI) | bukti singkat | catatan perbaikan yang disarankan. Pisahkan jelas yang terverifikasi dan yang tidak.
