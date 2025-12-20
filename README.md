# 🧠 AI TradeWise Project
Platform Chat AI Profesional untuk Analisis Pasar, Trading, dan Investasi.

---

## 🚀 Fitur Utama
- Konsultasi AI Real-time (integrasi OpenAI)
- Update Otomatis Pasar (saham, forex, kripto, komoditas)
- Sistem Login JSON + Auto-create Admin Default
- Pilihan Notifikasi: WhatsApp / Telegram / Email
- Jadwal update otomatis sesuai preferensi user
- Siap Deploy ke VPS (Docker + systemd)

---

## 🏗️ Struktur Proyek
AI_TradeWise_Project/
│
├── .env                           # Variabel lingkungan (API key, token, SMTP, dsb)
├── .gitignore
├── requirements.txt               # Dependensi Python
├── README.md                      # Dokumentasi lengkap proyek
│
├── src/                           # Backend Flask
│   ├── main.py                    # Entry utama (Flask app)
│   │
│   ├── modules/                   # Logika utama
│   │   ├── ai_consultation.py     # Konsultasi AI (integrasi OpenAI)
│   │   ├── market_analysis.py     # Analisis pasar, berita, dan data
│   │   ├── notifications.py       # Notifikasi WA/Telegram/Email
│   │   ├── data_validation.py     # Validasi input data (saham, kripto, dsb)
│   │   └── multi_model.py         # Manajemen & pembobotan model AI
│   │
│   ├── routes/                    # Endpoint API (REST)
│   │   ├── __init__.py
│   │   ├── auth_routes.py         # Login/Register/Reset Password
│   │   ├── ai_routes.py           # Chat, insight, analisis, dsb.
│   │   ├── notify_routes.py       # Kirim pesan WA/Telegram (user pilih)
│   │   ├── admin_routes.py        # Endpoint khusus admin
│   │
│   ├── utils/                     # Utilitas & helper
│   │   ├── __init__.py
│   │   ├── config.py              # Baca file .env
│   │   ├── logger.py              # Logging aktivitas sistem
│   │   ├── auth.py                # JWT, hash, auto-create admin
│   │   └── scheduler.py           # Jadwal auto-update (sesuai waktu user)
│   │
│   └── data/
│       ├── users.json             # Database ringan (akun)
│       ├── insights.json          # Cache hasil analisis pasar
│       └── logs/                  # Log aktivitas backend
│
├── frontend/                      # Website (HTML, CSS, JS)
│   ├── index.html                 # Login/Register
│   ├── chat.html                  # Chat & insight AI
│   ├── market_analysis.html       # Analisis grafik pasar
│   ├── settings.html              # Pengaturan notifikasi & preferensi user
│   │
│   ├── style/                     # CSS
│   │   ├── style.css
│   │   └── darkmode.css
│   │
│   ├── scripts/                   # JavaScript
│   │   ├── script.js
│   │   ├── chat_script.js
│   │   └── notify.js
│   │
│   └── assets/                    # Gambar, ikon, dan logo
│       ├── logo.png
│       └── bg.jpg
│
├── deploy/                        # File untuk deployment
│   ├── Dockerfile                 # Build image backend
│   ├── docker-compose.yml         # Menyatukan backend + frontend + reverse proxy
│   ├── nginx/
│   │   └── default.conf           # Nginx reverse proxy ke Flask
│   ├── systemd/
│   │   ├── tradewise-api.service  # Service backend Flask
│   │   └── tradewise-nginx.service# Service proxy (jika manual)
│   └── startup.sh                 # Skrip otomatis setup VPS
│
└── docs/
    ├── README_DEPLOY.md           # Panduan deploy lengkap
    ├── user_manual.md             # Panduan penggunaan
    └── api_reference.md           # Dokumentasi endpoint API


---

## ⚙️ Instalasi Lokal
1. Clone repositori ini atau salin file ke dalam direktori:
   ```bash
   git clone https://github.com/yourusername/AI_TradeWise_Project.git
   cd AI_TradeWise_Project
   ```

2. Buat virtual environment dan instal dependensi:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. Buat file .env berdasarkan .env contoh (.env.example).

4. Jalankan aplikasi:
   ```bash
   python src/main.py
   ```
   Server akan berjalan di http://localhost:5000

---

## Deploy ke VPS (Docker)

1. Build image:
   ```bash
   docker build -t ai-tradewise .
   ```
2. Jalankan:
   ```bash
   docker-compose up -d
   ```
3. Pastikan aplikasi berjalan.

---

## Login Default
| Email | Password |
|---|---|
| admin@tradewise.ai | Admin12345! |

> Catatan: Login manual mungkin menggunakan username "admin" dan password "admin123" sesuai konfigurasi di `src/main.py`.

---

## Kontak

Dikembangkan oleh AI TradeWise Dev Team
Hubungi: support@tradewise.ai


---

Jika kamu menyetujui isi empat file root ini,  
kita lanjut ke tahap berikutnya:  
➡️ **bagian `src/` backend penuh** (FastAPI, login JSON, auto-admin, AI & notifikasi).  

Apakah saya lanjutkan langsung ke folder `src/` (backend lengkap)?

