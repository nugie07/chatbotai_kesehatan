# 🏥 Chatbot AI Kesehatan - RS Siloam

Chatbot berbasis AI untuk customer service di dunia kesehatan menggunakan Gemini AI. Chatbot ini dikhususkan untuk **RS Siloam** dan dapat membantu pengguna untuk:
- ✅ Mengecek ketersediaan dokter di RS Siloam
- ✅ Menjelaskan gejala penyakit dan memberikan saran awal
- ✅ Memberikan informasi jadwal praktik dokter
- ✅ Menjawab pertanyaan umum tentang kesehatan

## 🚀 Teknologi yang Digunakan

- **Python 3.11**
- **Streamlit** - Framework untuk web interface
- **Google Gemini AI** - Model LLM untuk pemrosesan bahasa alami
- **python-dotenv** - Untuk manajemen environment variables

## 📋 Fitur

### Konfigurasi Default:
- **Gaya Bahasa**: Santai (tidak dapat diubah dari UI)
- **Kreativitas Respons**: 0.70 (tidak dapat diubah dari UI)
- **Memory**: Aktif - Chatbot mengingat percakapan sebelumnya
- **Rekomendasi**: Aktif - Memberikan rekomendasi dokter berdasarkan gejala

### Fitur Utama:
- 💬 Chat interface yang user-friendly dan sederhana
- 🧠 Memory untuk mengingat konteks percakapan
- 🏥 Database dokter RS Siloam (dummy data)
- 🔍 Deteksi gejala dan rekomendasi dokter otomatis
- 📱 Responsive design dengan Streamlit
- 🎯 Fokus pada layanan RS Siloam

## 🛠️ Instalasi dan Setup

### Cara Cepat (Recommended)

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```powershell
.\run.bat
```

Script akan otomatis:
- ✅ Membuat virtual environment jika belum ada
- ✅ Menginstall dependencies jika belum terinstall
- ✅ Menjalankan aplikasi Streamlit

### Setup Manual

#### 1. Clone atau Download Project

```bash
cd chatbotai
```

#### 2. Setup API Key Gemini

1. Dapatkan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Buat file `.env` di root project:
```bash
# Windows PowerShell
New-Item -Path .env -ItemType File

# Linux/Mac
touch .env
```

3. Tambahkan API key ke file `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 3. Jalankan dengan Script

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```powershell
.\run.bat
```

Atau jalankan manual:
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run main.py
```

Aplikasi akan terbuka di browser secara otomatis di `http://localhost:8501` atau tergantung dari port availbility nya

## 📖 Cara Penggunaan

### Contoh Pertanyaan yang Bisa Ditanyakan:

1. **Ketersediaan Dokter:**
   - "Apakah ada dokter bedah yang tersedia di RS Siloam?"
   - "Saya butuh dokter kulit, ada yang tersedia?"
   - "Kapan jadwal praktik Dr. Rizki Pratama?"

2. **Gejala Penyakit:**
   - "Saya demam dan batuk, apa yang harus saya lakukan?"
   - "Gejala sakit kepala terus menerus, perlu ke dokter apa?"
   - "Saya mengalami ruam kulit, dokter spesialis apa yang cocok?"

3. **Informasi Rumah Sakit:**
   - "Berapa nomor telepon RS Siloam?"
   - "Dimana alamat RS Siloam?"
   - "Dokter apa saja yang tersedia di RS Siloam?"

## 📁 Struktur Project

```
chatbotai/
├── main.py              # Aplikasi Streamlit utama
├── chatbot.py           # Core chatbot logic dengan Gemini AI
├── config.py            # Konfigurasi dan data RS Siloam
├── requirements.txt     # Dependencies Python
├── run.sh               # Script untuk menjalankan aplikasi (Linux/Mac)
├── run.bat              # Script untuk menjalankan aplikasi (Windows)
├── .env                 # Environment variables (buat sendiri)
├── env.template         # Template file .env
├── .gitignore          # Git ignore rules
└── README.md           # Dokumentasi ini
```

## ⚙️ Konfigurasi Lanjutan

Anda dapat mengubah konfigurasi di file `config.py`:

- **RUMAH_SAKIT**: Tambah/edit data dokter RS Siloam
- **CHATBOT_CONFIG**: Ubah parameter default chatbot (gaya bahasa, temperature, dll)
- **SYSTEM_PROMPT**: Sesuaikan prompt system untuk AI

**Catatan:** Aplikasi ini dikhususkan untuk RS Siloam. Untuk menambah rumah sakit lain, edit file `config.py` dan tambahkan data rumah sakit di dictionary `RUMAH_SAKIT`.

## ⚠️ Peringatan Penting

**Chatbot ini tidak menggantikan konsultasi medis langsung dengan dokter profesional.** 
Selalu konsultasikan masalah kesehatan serius dengan dokter yang berlisensi.

## 🔧 Troubleshooting

### Error: GEMINI_API_KEY tidak ditemukan
- Pastikan file `.env` ada di root project
- Pastikan format: `GEMINI_API_KEY=your_key_here` (tanpa spasi)

### Error: Module not found
- Pastikan virtual environment aktif
- Install ulang dependencies: `pip install -r requirements.txt`

### Error: API key invalid
- Pastikan API key Gemini valid
- Cek di [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📝 License

Project ini dibuat untuk keperluan edukasi dan demonstrasi.

## 👨‍💻 Author

Dibuat dengan ❤️ menggunakan Gemini AI dan Streamlit
