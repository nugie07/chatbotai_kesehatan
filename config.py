"""
Konfigurasi untuk Chatbot AI Kesehatan
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Chatbot Configuration
CHATBOT_CONFIG = {
    "gaya_bahasa": "santai",  # Options: "formal", "santai"
    "domain": "kesehatan",
    "temperature": 0.7,  # Kreativitas respons (0.0 - 1.0)
    "max_tokens": 1000,
    "enable_memory": True,
    "enable_rekomendasi": True,
}

# Data Dummy Rumah Sakit dan Dokter
# Hanya RS Siloam yang digunakan
RUMAH_SAKIT = {
    "RS Siloam": {
        "alamat": "Jl. Garnisun Dalam No. 8, Jakarta Selatan",
        "telepon": "021-29962888",
        "dokter": {
            "Dr. Rizki Pratama, Sp.B": {
                "spesialisasi": "Bedah Umum",
                "jadwal": ["Senin: 09:00-13:00", "Rabu: 14:00-18:00"],
                "tersedia": True
            },
            "Dr. Indah Permata, Sp.KK": {
                "spesialisasi": "Kulit dan Kelamin",
                "jadwal": ["Selasa: 09:00-13:00", "Kamis: 14:00-18:00", "Jumat: 09:00-13:00"],
                "tersedia": True
            }
        }
    }
}

# Sistem Prompt untuk Chatbot
SYSTEM_PROMPT = """Anda adalah asisten AI customer service yang ramah dan profesional untuk layanan kesehatan. 
Tugas Anda adalah membantu pasien dengan:

1. Mencari informasi ketersediaan dokter di rumah sakit
2. Menjelaskan gejala penyakit dan memberikan saran awal
3. Memberikan informasi jadwal praktik dokter
4. Menjawab pertanyaan umum tentang kesehatan

Gaya komunikasi: {gaya_bahasa}
Domain: {domain}

Penting:
- Selalu gunakan bahasa Indonesia
- Bersikap empati dan ramah
- Jika tidak yakin, sarankan untuk berkonsultasi langsung dengan dokter
- Jangan memberikan diagnosis medis definitif
- Berikan informasi yang akurat dan mudah dipahami

Informasi Rumah Sakit dan Dokter yang tersedia:
{rumah_sakit_info}
"""

def get_system_prompt():
    """Generate system prompt dengan konfigurasi saat ini"""
    rumah_sakit_info = "\n".join([
        f"\n{rs_name}:\n  Alamat: {info['alamat']}\n  Telepon: {info['telepon']}\n  Dokter:"
        for rs_name, info in RUMAH_SAKIT.items()
    ])
    
    for rs_name, info in RUMAH_SAKIT.items():
        rumah_sakit_info += f"\n  {rs_name}:\n"
        for dokter_name, dokter_info in info['dokter'].items():
            rumah_sakit_info += f"    - {dokter_name} ({dokter_info['spesialisasi']})\n"
            rumah_sakit_info += f"      Jadwal: {', '.join(dokter_info['jadwal'])}\n"
    
    return SYSTEM_PROMPT.format(
        gaya_bahasa=CHATBOT_CONFIG["gaya_bahasa"],
        domain=CHATBOT_CONFIG["domain"],
        rumah_sakit_info=rumah_sakit_info
    )
