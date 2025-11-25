# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan Chatbot AI Kesehatan - RS Siloam.

## ⚡ Cara Cepat (Recommended)

**Windows:**
```powershell
.\run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

Script akan otomatis membuat virtual environment, install dependencies, dan menjalankan aplikasi!

## ⚡ Setup Manual (Windows)

1. **Buat file `.env` dan tambahkan API key:**
   ```powershell
   New-Item -Path .env -ItemType File
   ```
   Edit file `.env` dan tambahkan:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   Dapatkan API key di: https://makersuite.google.com/app/apikey

2. **Jalankan dengan script:**
   ```powershell
   .\run.bat
   ```

   Atau manual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   streamlit run main.py
   ```

## ⚡ Setup Manual (Linux/Mac)

1. **Buat file `.env` dan tambahkan API key:**
   ```bash
   touch .env
   ```
   Edit file `.env` dan tambahkan:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. **Jalankan dengan script:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   Atau manual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   streamlit run main.py
   ```

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Buat file .env
# Salin .env.example ke .env dan edit

# 5. Jalankan aplikasi
streamlit run main.py
```

## ✅ Verifikasi Setup

Setelah setup, pastikan:
- ✅ Virtual environment aktif (terlihat `(venv)` di terminal)
- ✅ File `.env` ada dan berisi `GEMINI_API_KEY`
- ✅ Tidak ada error saat menjalankan `streamlit run main.py`
- ✅ Browser terbuka di `http://localhost:8501`

## 🆘 Masalah Umum

**Error: "GEMINI_API_KEY tidak ditemukan"**
- Pastikan file `.env` ada di folder root project
- Pastikan format: `GEMINI_API_KEY=your_key` (tanpa spasi)

**Error: "Module not found"**
- Pastikan virtual environment aktif
- Jalankan: `pip install -r requirements.txt`

**Port sudah digunakan**
- Streamlit akan otomatis mencari port lain
- Atau hentikan aplikasi yang menggunakan port 8501
