"""
Modul Chatbot AI untuk Layanan Kesehatan
Menggunakan Gemini AI untuk pemrosesan bahasa alami
"""
import google.generativeai as genai
from typing import List, Dict, Optional
import config


class HealthcareChatbot:
    """Chatbot untuk customer service kesehatan dengan Gemini AI"""
    
    def __init__(self, api_key: str):
        """
        Inisialisasi chatbot
        
        Args:
            api_key: API key untuk Gemini AI
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan. Silakan set di file .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',  # Menggunakan model terbaru yang tersedia
            generation_config={
                'temperature': config.CHATBOT_CONFIG['temperature'],
                'max_output_tokens': config.CHATBOT_CONFIG['max_tokens'],
            }
        )
        
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = config.get_system_prompt()
        self.enable_memory = config.CHATBOT_CONFIG['enable_memory']
        self.api_key = api_key
    
    def update_temperature(self, temperature: float):
        """Update temperature untuk model"""
        import google.generativeai as genai
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',  # Menggunakan model terbaru yang tersedia
            generation_config={
                'temperature': temperature,
                'max_output_tokens': config.CHATBOT_CONFIG['max_tokens'],
            }
        )
        
    def _extract_doctor_info(self, query: str) -> Optional[Dict]:
        """
        Ekstrak informasi dokter dari query pengguna
        
        Args:
            query: Query dari pengguna
            
        Returns:
            Dictionary dengan informasi dokter atau None
        """
        query_lower = query.lower()
        
        # Cari berdasarkan nama dokter
        for rs_name, rs_info in config.RUMAH_SAKIT.items():
            for dokter_name, dokter_info in rs_info['dokter'].items():
                if any(word in query_lower for word in dokter_name.lower().split()):
                    return {
                        'dokter': dokter_name,
                        'rumah_sakit': rs_name,
                        'info': dokter_info,
                        'rs_info': rs_info
                    }
        
        # Cari berdasarkan spesialisasi
        spesialisasi_keywords = {
            'penyakit dalam': 'Penyakit Dalam',
            'anak': 'Anak',
            'jantung': 'Jantung dan Pembuluh Darah',
            'kandungan': 'Kandungan dan Kebidanan',
            'kebidanan': 'Kandungan dan Kebidanan',
            'bedah': 'Bedah Umum',
            'kulit': 'Kulit dan Kelamin',
            'kelamin': 'Kulit dan Kelamin',
            'saraf': 'Saraf',
            'mata': 'Mata'
        }
        
        for keyword, spesialisasi in spesialisasi_keywords.items():
            if keyword in query_lower:
                # Cari dokter dengan spesialisasi tersebut
                for rs_name, rs_info in config.RUMAH_SAKIT.items():
                    for dokter_name, dokter_info in rs_info['dokter'].items():
                        if dokter_info['spesialisasi'] == spesialisasi:
                            return {
                                'dokter': dokter_name,
                                'rumah_sakit': rs_name,
                                'info': dokter_info,
                                'rs_info': rs_info
                            }
        
        return None
    
    def _get_context_info(self, query: str) -> str:
        """
        Ambil informasi konteks tambahan berdasarkan query
        
        Args:
            query: Query dari pengguna
            
        Returns:
            String dengan informasi konteks tambahan
        """
        context = ""
        doctor_info = self._extract_doctor_info(query)
        
        if doctor_info:
            context += f"\n\n[INFORMASI DOKTER TERKAIT]\n"
            context += f"Dokter: {doctor_info['dokter']}\n"
            context += f"Rumah Sakit: {doctor_info['rumah_sakit']}\n"
            context += f"Spesialisasi: {doctor_info['info']['spesialisasi']}\n"
            context += f"Jadwal: {', '.join(doctor_info['info']['jadwal'])}\n"
            context += f"Status: {'Tersedia' if doctor_info['info']['tersedia'] else 'Tidak Tersedia'}\n"
            context += f"Alamat RS: {doctor_info['rs_info']['alamat']}\n"
            context += f"Telepon RS: {doctor_info['rs_info']['telepon']}\n"
        
        return context
    
    def get_response(self, user_message: str) -> str:
        """
        Dapatkan respons dari chatbot
        
        Args:
            user_message: Pesan dari pengguna
            
        Returns:
            Respons dari chatbot
        """
        # Tambahkan konteks informasi dokter jika relevan
        context_info = self._get_context_info(user_message)
        
        # Buat prompt lengkap
        full_prompt = self.system_prompt + context_info
        
        # Tambahkan history percakapan jika memory diaktifkan
        if self.enable_memory and self.conversation_history:
            conversation_text = "\n".join([
                f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                for msg in self.conversation_history[-5:]  # Ambil 5 percakapan terakhir
            ])
            full_prompt += f"\n\n[RIWAYAT PERCAKAPAN]\n{conversation_text}\n\n"
        
        full_prompt += f"\n\nUser: {user_message}\nAssistant:"
        
        try:
            # Generate response dari Gemini
            response = self.model.generate_content(full_prompt)
            bot_response = response.text.strip()
            
            # Simpan ke history
            if self.enable_memory:
                self.conversation_history.append({
                    'user': user_message,
                    'assistant': bot_response
                })
                # Batasi history maksimal 10 percakapan
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
            
            return bot_response
            
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {str(e)}. Silakan coba lagi."
    
    def clear_history(self):
        """Hapus riwayat percakapan"""
        self.conversation_history = []
    
    def get_recommendations(self, symptoms: str) -> List[str]:
        """
        Dapatkan rekomendasi berdasarkan gejala
        
        Args:
            symptoms: Gejala yang dijelaskan pengguna
            
        Returns:
            List rekomendasi
        """
        if not config.CHATBOT_CONFIG['enable_rekomendasi']:
            return []
        
        recommendations = []
        
        # Analisis gejala sederhana
        symptoms_lower = symptoms.lower()
        
        # Mapping gejala ke spesialisasi
        symptom_specialist = {
            'demam': 'Penyakit Dalam',
            'batuk': 'Penyakit Dalam',
            'pilek': 'Penyakit Dalam',
            'sakit kepala': 'Saraf',
            'migrain': 'Saraf',
            'nyeri dada': 'Jantung dan Pembuluh Darah',
            'sesak napas': 'Jantung dan Pembuluh Darah',
            'sakit perut': 'Penyakit Dalam',
            'diare': 'Penyakit Dalam',
            'ruam': 'Kulit dan Kelamin',
            'gatal': 'Kulit dan Kelamin',
            'mata merah': 'Mata',
            'pandangan kabur': 'Mata',
            'hamil': 'Kandungan dan Kebidanan',
            'kehamilan': 'Kandungan dan Kebidanan'
        }
        
        # Cari spesialisasi yang relevan
        relevant_specialists = set()
        for symptom, specialist in symptom_specialist.items():
            if symptom in symptoms_lower:
                relevant_specialists.add(specialist)
        
        # Cari dokter dengan spesialisasi tersebut (hanya RS Siloam)
        for specialist in relevant_specialists:
            rs_name = "RS Siloam"  # Hanya RS Siloam
            if rs_name in config.RUMAH_SAKIT:
                rs_info = config.RUMAH_SAKIT[rs_name]
                for dokter_name, dokter_info in rs_info['dokter'].items():
                    if dokter_info['spesialisasi'] == specialist and dokter_info['tersedia']:
                        recommendations.append(
                            f"💡 Rekomendasi: {dokter_name} ({specialist}) di {rs_name}"
                        )
                        break
        
        if not recommendations:
            recommendations.append(
                "💡 Untuk gejala yang Anda sebutkan, disarankan berkonsultasi dengan dokter umum atau spesialis penyakit dalam."
            )
        
        return recommendations
