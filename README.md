ThunderSpan Elite Extreme

<p align="center">
<img src="https://img.shields.io/badge/Version-2.0.0-red" alt="Version">
<img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-green" alt="License">
<img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey" alt="Platform">
</p>

<p align="center">
<b>Ultimate Multi-Vector Load Testing Tool</b>
</p>
🚀 Overview

ThunderSpan Elite Extreme adalah alat load testing canggih yang dirancang untuk melakukan pengujian beban multi-vektor pada server. Tool ini menggabungkan berbagai teknik seperti HTTP Flood, TCP Flood, UDP Flood, ICMP Flood, DNS Amplification, dan Slowloris Attack dalam satu paket yang powerful.
⚠️ Peringatan Penting

PERHATIAN: Alat ini hanya boleh digunakan untuk tujuan:

    🧪 Menguji server yang Anda miliki sendiri.

    🎓 Penelitian dan edukasi tentang keamanan jaringan.

    📝 Pengujian dengan izin tertulis dari pemilik sistem.

Menggunakan alat ini pada sistem tanpa izin adalah TINDAKAN ILEGAL dan dapat berakibat hukum yang serius.
📦 Instalasi
Prasyarat

    Python 3.8 atau lebih baru

    pip (Python package manager)

Instalasi Dependensi

# Update package list (untuk Debian/Ubuntu)
sudo apt update

# Install Python dan pip (jika belum ada)
sudo apt install python3 python3-pip -y

# Install dependensi yang diperlukan
pip3 install requests

# (Opsional) Menggunakan virtual environment (direkomendasikan)
python3 -m venv thunderspan-env
source thunderspan-env/bin/activate
pip install requests

Unduh ThunderSpan

# Clone repositori (ganti dengan username Anda)
git clone [https://github.com/your-username/ThunderSpan.git](https://github.com/your-username/ThunderSpan.git)
cd ThunderSpan

# Atau unduh file secara manual
wget [https://raw.githubusercontent.com/your-username/ThunderSpan/main/thunderspan.py](https://raw.githubusercontent.com/your-username/ThunderSpan/main/thunderspan.py)

🎯 Penggunaan
Penggunaan Dasar

# Contoh penggunaan dasar dengan URL
python3 thunderspan.py [https://target-domain.com](https://target-domain.com)

# Contoh dengan alamat IP
python3 thunderspan.py 192.168.1.100

Penggunaan Lanjutan

# Konfigurasi ekstrem untuk pengujian selama 6 jam
python3 thunderspan.py [https://target-domain.com](https://target-domain.com) \
  --http-threads 3000 \
  --tcp-threads 800 \
  --udp-threads 800 \
  --slowloris-threads 200 \
  --icmp-threads 200 \
  --dns-threads 100 \
  --duration 21600

# Mode tak terbatas (berjalan hingga dihentikan manual dengan Ctrl+C)
python3 thunderspan.py [https://target-domain.com](https://target-domain.com) --infinite

# Menargetkan port khusus
python3 thunderspan.py [https://target-domain.com](https://target-domain.com) --ports 80,443,8080,8443

# Ukuran data dan paket kustom
python3 thunderspan.py [https://target-domain.com](https://target-domain.com) --method POST --data-size 4096 --packet-size 2048

Opsi Baris Perintah

Parameter
	

Deskripsi
	

Default

target
	

URL atau alamat IP target
	

Wajib

-t, --http-threads
	

Jumlah thread HTTP
	

2000

-tp, --tcp-threads
	

Jumlah thread TCP
	

500

-u, --udp-threads
	

Jumlah thread UDP
	

500

-s, --slowloris-threads
	

Jumlah thread Slowloris
	

100

-i, --icmp-threads
	

Jumlah thread ICMP
	

100

-dns, --dns-threads
	

Jumlah thread DNS
	

50

-d, --duration
	

Durasi pengujian (detik)
	

21600 (6 jam)

-dly, --delay
	

Jeda antar permintaan (detik)
	

0.00001

-m, --method
	

Metode HTTP (GET/POST/HEAD)
	

GET

-p, --ports
	

Port untuk TCP/UDP flood (dipisah koma)
	

80,443,8080

-ds, --data-size
	

Ukuran data untuk request POST (bytes)
	

2048

-ps, --packet-size
	

Ukuran paket untuk flood (bytes)
	

1024

-dns-srv, --dns-server
	

Server DNS untuk amplifikasi
	

8.8.8.8

--no-ssl
	

Gunakan HTTP, bukan HTTPS
	

False

--infinite
	

Jalankan tanpa batas waktu
	

False
🛡️ Vektor Serangan

ThunderSpan Elite Extreme mendukung 6 jenis vektor pengujian:

    HTTP Flood: Mengirimkan permintaan HTTP (GET/POST/HEAD) dalam jumlah besar.

    TCP Flood: Membanjiri port TCP target dengan paket SYN atau koneksi penuh.

    UDP Flood: Membanjiri port UDP target dengan paket data.

    ICMP Flood: Melakukan ping flood untuk menjenuhkan bandwidth (memerlukan hak akses root).

    DNS Amplification: Memanfaatkan server DNS publik untuk memperkuat lalu lintas ke target.

    Slowloris: Menghabiskan pool koneksi server dengan membuka banyak koneksi dan membuatnya tetap aktif.

📊 Fitur Unggulan

    ✅ Performa Tinggi: Menggunakan multi-threading untuk menghasilkan beban yang masif.

    ✅ Pemantauan Real-time: Menampilkan statistik serangan secara langsung di terminal.

    ✅ Koneksi Aman: Dukungan penuh untuk target yang menggunakan SSL/TLS (HTTPS).

    ✅ Anti-Deteksi: Menggunakan User-Agent acak dan header HTTP untuk menyamarkan lalu lintas.

    ✅ Bypass Cache: Teknik cache-busting memastikan setiap permintaan diproses oleh server.

    ✅ Parameter Fleksibel: Semua aspek serangan dapat dikonfigurasi melalui CLI.

    ✅ Antarmuka Menarik: Tampilan CLI yang berwarna dan mudah dibaca.

    ✅ Laporan Akhir: Ringkasan performa yang detail setelah pengujian selesai.

🔧 Detail Teknis
Kebutuhan Sistem

    CPU: Minimal 4 core (direkomendasikan 8+ core)

    RAM: Minimal 4GB (direkomendasikan 8+ GB)

    Jaringan: Koneksi internet stabil dengan bandwidth yang memadai.

    OS: Linux (sangat direkomendasikan untuk performa maksimal) atau Windows.

Tips Performa

    Gunakan sistem operasi berbasis Linux untuk hasil terbaik.

    Tingkatkan batas file descriptors di Linux sebelum menjalankan: ulimit -n 100000.

    Pastikan Anda memiliki koneksi internet dengan bandwidth upload yang tinggi.

    Sesuaikan jumlah thread dengan kemampuan perangkat keras Anda untuk menghindari bottleneck.

    Pantau penggunaan CPU dan RAM selama pengujian.

📝 Contoh Skenario
Menguji Server Pengembangan Lokal

# Uji server lokal dengan konfigurasi ringan selama 5 menit
python3 thunderspan.py http://localhost:8080 \
  --http-threads 100 \
  --tcp-threads 50 \
  --duration 300

Simulasi Beban Puncak (Dengan Izin)

# Uji server produksi untuk mensimulasikan beban puncak secara terus-menerus
python3 thunderspan.py [https://your-authorized-domain.com](https://your-authorized-domain.com) \
  --http-threads 5000 \
  --tcp-threads 1000 \
  --udp-threads 1000 \
  --infinite \
  --delay 0.000001

🚨 Pernyataan Hukum (Disclaimer)

Alat ini dibuat untuk tujuan edukasi dan pengujian pada lingkungan yang terkendali. Penulis tidak bertanggung jawab atas segala bentuk penyalahgunaan alat ini. Anda bertanggung jawab penuh atas tindakan Anda sendiri. Pastikan Anda:

    Memiliki izin tertulis dan eksplisit sebelum melakukan pengujian.

    Hanya menargetkan sistem dan jaringan yang Anda miliki.

    Memahami dan mematuhi semua hukum yang berlaku di yurisdiksi Anda.

📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail lebih lanjut.
🤝 Berkontribusi

Kontribusi sangat kami hargai! Jika Anda ingin berkontribusi, silakan:

    Fork proyek ini.

    Buat branch fitur baru (git checkout -b feature/AmazingFeature).

    Commit perubahan Anda (git commit -m 'Add some AmazingFeature').

    Push ke branch Anda (git push origin feature/AmazingFeature).

    Buat Pull Request baru.

⭐ Apresiasi

    Terima kasih kepada seluruh komunitas open source.

    Para peneliti keamanan siber yang karyanya menginspirasi.

    Semua kontributor yang telah membantu pengembangan tool ini.

<p align="center">
Dibuat dengan ❤️ oleh PHΛNTØM - Untuk dunia siber yang lebih tangguh.

</p>
#   T h u n d e r S p a n - V 2  
 