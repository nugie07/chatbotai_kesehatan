"""
Aplikasi Streamlit untuk Chatbot AI Kesehatan
"""
import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import HealthcareChatbot
import config

# Load environment variables
load_dotenv()

# Konfigurasi halaman
st.set_page_config(
    page_title="Chatbot AI Kesehatan",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar disembunyikan
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'chatbot' not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            st.session_state.chatbot = HealthcareChatbot(api_key)
            st.session_state.initialized = True
        except Exception as e:
            st.session_state.initialized = False
            st.session_state.error = str(e)
    else:
        st.session_state.initialized = False
        st.session_state.error = "GEMINI_API_KEY tidak ditemukan"

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

# Header utama
st.markdown('<div class="main-header">🏥 Chatbot AI Kesehatan</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asisten Virtual untuk Layanan Kesehatan RS Siloam</div>', unsafe_allow_html=True)

# Tombol Hapus Riwayat Chat di bagian atas
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        if st.session_state.initialized:
            st.session_state.chatbot.clear_history()
        st.session_state.messages = []
        st.session_state.show_recommendations = False
        st.rerun()

# Cek inisialisasi
if not st.session_state.initialized:
    st.error(f"❌ Error: {st.session_state.get('error', 'Unknown error')}")
    st.info("""
    **Cara Setup:**
    1. Buat file `.env` di root project
    2. Tambahkan `GEMINI_API_KEY=your_api_key_here`
    3. Dapatkan API key dari: https://makersuite.google.com/app/apikey
    4. Refresh halaman ini
    """)
    st.stop()

# Tampilkan riwayat chat
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Tampilkan rekomendasi jika ada
            if message["role"] == "assistant" and "recommendations" in message:
                st.markdown("---")
                for rec in message["recommendations"]:
                    st.info(rec)

# Input chat
if prompt := st.chat_input("Tuliskan pertanyaan Anda di sini..."):
    # Tambahkan pesan user ke history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Sedang memproses..."):
            response = st.session_state.chatbot.get_response(prompt)
            st.markdown(response)
            
            # Cek apakah perlu rekomendasi
            recommendations = []
            if config.CHATBOT_CONFIG["enable_rekomendasi"]:
                # Deteksi jika user menanyakan gejala
                gejala_keywords = ['gejala', 'sakit', 'nyeri', 'demam', 'batuk', 'pusing', 'mual']
                if any(keyword in prompt.lower() for keyword in gejala_keywords):
                    recommendations = st.session_state.chatbot.get_recommendations(prompt)
            
            # Simpan ke history
            message_data = {"role": "assistant", "content": response}
            if recommendations:
                message_data["recommendations"] = recommendations
                st.markdown("---")
                for rec in recommendations:
                    st.info(rec)
            
            st.session_state.messages.append(message_data)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>💡 <strong>Tips:</strong> Tanyakan tentang ketersediaan dokter, jadwal praktik, atau gejala penyakit</p>
    <p>⚠️ <strong>Peringatan:</strong> Chatbot ini tidak menggantikan konsultasi medis langsung dengan dokter</p>
</div>
""", unsafe_allow_html=True)
