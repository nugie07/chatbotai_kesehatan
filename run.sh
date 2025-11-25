#!/bin/bash

# Script untuk menjalankan Chatbot AI Kesehatan
# Script ini akan otomatis:
# 1. Membuat virtual environment jika belum ada
# 2. Menginstall dependencies jika belum terinstall
# 3. Menjalankan aplikasi Streamlit

echo "=========================================="
echo "  Chatbot AI Kesehatan - RS Siloam"
echo "=========================================="
echo ""

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ ERROR: Python tidak ditemukan!"
        echo "   Silakan install Python 3.11 atau Python 3 terlebih dahulu"
        exit 1
    else
        PYTHON_CMD=python3
        echo "⚠️  Python 3.11 tidak ditemukan, menggunakan python3"
    fi
else
    PYTHON_CMD=python3.11
fi

echo "✅ Python ditemukan: $($PYTHON_CMD --version)"
echo ""

# Check atau buat virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Membuat virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Gagal membuat virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment berhasil dibuat"
else
    echo "✅ Virtual environment sudah ada"
fi

echo ""

# Aktifkan virtual environment
echo "🔄 Mengaktifkan virtual environment..."
source venv/bin/activate

# Check apakah requirements sudah terinstall
echo "🔍 Mengecek dependencies..."
MISSING_DEPS=false

# Check beberapa package utama
if ! python -c "import streamlit" 2>/dev/null; then
    MISSING_DEPS=true
elif ! python -c "import google.generativeai" 2>/dev/null; then
    MISSING_DEPS=true
elif ! python -c "import dotenv" 2>/dev/null; then
    MISSING_DEPS=true
fi

if [ "$MISSING_DEPS" = true ]; then
    echo "📥 Dependencies belum lengkap, menginstall..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Gagal menginstall dependencies"
        exit 1
    fi
    echo "✅ Dependencies berhasil diinstall"
else
    echo "✅ Semua dependencies sudah terinstall"
fi

echo ""

# Check file .env
if [ ! -f ".env" ]; then
    echo "⚠️  PERINGATAN: File .env tidak ditemukan!"
    echo "   Buat file .env dan tambahkan GEMINI_API_KEY"
    echo "   Contoh: GEMINI_API_KEY=your_api_key_here"
    echo ""
    echo "   Dapatkan API key di: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "   Lanjutkan tanpa .env? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ File .env ditemukan"
fi

echo ""
echo "=========================================="
echo "  Menjalankan aplikasi Streamlit..."
echo "=========================================="
echo ""
echo "🌐 Aplikasi akan terbuka di: http://localhost:8501"
echo "🛑 Tekan Ctrl+C untuk menghentikan aplikasi"
echo ""

# Jalankan Streamlit
streamlit run main.py

