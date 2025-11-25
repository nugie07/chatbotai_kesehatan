@echo off
REM Script untuk menjalankan Chatbot AI Kesehatan (Windows)
REM Script ini akan otomatis:
REM 1. Membuat virtual environment jika belum ada
REM 2. Menginstall dependencies jika belum terinstall
REM 3. Menjalankan aplikasi Streamlit

echo ==========================================
echo   Chatbot AI Kesehatan - RS Siloam
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python 3.11 terlebih dahulu
    pause
    exit /b 1
)

echo Python ditemukan:
python --version
echo.

REM Check atau buat virtual environment
if not exist "venv" (
    echo Membuat virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Gagal membuat virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment berhasil dibuat
) else (
    echo Virtual environment sudah ada
)

echo.

REM Aktifkan virtual environment
echo Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Check apakah requirements sudah terinstall
echo Mengecek dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    set MISSING_DEPS=1
) else (
    python -c "import google.generativeai" >nul 2>&1
    if errorlevel 1 (
        set MISSING_DEPS=1
    ) else (
        python -c "import dotenv" >nul 2>&1
        if errorlevel 1 (
            set MISSING_DEPS=1
        )
    )
)

if defined MISSING_DEPS (
    echo Dependencies belum lengkap, menginstall...
    pip install --upgrade pip --quiet
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Gagal menginstall dependencies
        pause
        exit /b 1
    )
    echo Dependencies berhasil diinstall
) else (
    echo Semua dependencies sudah terinstall
)

echo.

REM Check file .env
if not exist ".env" (
    echo PERINGATAN: File .env tidak ditemukan!
    echo Buat file .env dan tambahkan GEMINI_API_KEY
    echo Contoh: GEMINI_API_KEY=your_api_key_here
    echo.
    echo Dapatkan API key di: https://makersuite.google.com/app/apikey
    echo.
    pause
) else (
    echo File .env ditemukan
)

echo.
echo ==========================================
echo   Menjalankan aplikasi Streamlit...
echo ==========================================
echo.
echo Aplikasi akan terbuka di: http://localhost:8501
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

REM Jalankan Streamlit
streamlit run main.py

pause

