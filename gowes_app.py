import streamlit as st
import time
from datetime import datetime
from google import genai
from google.genai import types

# ── 1. KONFIGURASI HALAMAN & CUSTOM CSS ───────────────────────────────────────
st.set_page_config(page_title="GowesBot Pro - CS Sepeda AI", page_icon="🚲", layout="centered")

# CSS Kustom untuk mempercantik kolom chat dan animasi lampu status online di sidebar
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid #c2ebd0;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f2fbf6;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ffffff;
    }
    /* Animasi lampu berdenyut hijau untuk status server */
    .online-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #4CAF50;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        animation: pulsing 1.5s infinite;
    }
    @keyframes pulsing {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(76, 175, 80, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚲 GowesBot: Sobat Diskusi Sepeda")
st.caption("🚀 Premium Customer Service Bot v2.0 | Didukung oleh Gemini 2.5 Flash")

# ── 2. SIDEBAR: PROFESSIONAL DASHBOARD CONTROLS ──────────────────────────────
with st.sidebar:
    st.markdown("### 🛠️ Panel Kendali Bot")
    google_api_key = st.text_input("🔑 Google AI API Key", type="password", placeholder="Masukkan API Key...")
    
    st.markdown("---")
    
    # INDIKATOR STATUS REAL-TIME (PENGGANTI INFOBAR TOKEN)
    st.markdown("### 🛡️ Status Sistem CS")
    st.markdown('<div class="online-indicator"></div><span style="color:#4CAF50; font-weight:bold;">Sistem AI: Terhubung (Online)</span>', unsafe_allow_html=True)
    st.caption("Semua modul asisten virtual dan database simulasi stok berfungsi normal.")
    
    st.markdown("---")
    
    # FITUR TOMBOL JALAN PINTAS (QUICK RECOMMENDED TRIGGERS)
    st.markdown("### 🎯 Rekomendasi Pertanyaan")
    st.markdown("Bingung mau tanya apa? Klik tombol di bawah untuk langsung kirim perintah otomatis:")
    
    # Inisialisasi variabel bantu untuk menampung teks trigger tombol pintas
    pemicu_chat_otomatis = None
    if st.button("📍 Cari rute gowes terbaik akhir pekan", use_container_width=True):
        pemicu_chat_otomatis = "Rekomendasikan rute gowes akhir pekan yang seru dong bro!"
    if st.button("🔧 Cara cek rantai sepeda yang seret", use_container_width=True):
        pemicu_chat_otomatis = "Bro, minta tips cara benerin atau ngerawat rantai sepeda yang seret dong."
    if st.button("🚲 Cek ketersediaan sepeda Gunung (MTB)", use_container_width=True):
        pemicu_chat_otomatis = "Halo GowesBot, toko kita lagi ready stok sepeda MTB apa aja?"

    st.markdown("---")
    
    # INFORMASI METADATA OPERASIONAL OPERATOR
    st.markdown("### ℹ️ Informasi Toko")
    st.markdown("• **Jam Operasional Bot:** 24/7 (Non-stop)\n• **Mesin Pemroses:** Google Gemini LLM Engine\n• **Versi Sistem:** v2.5-Stable Production")
    
    st.markdown("---")
    reset_button = st.button("🔄 Bersihkan Obrolan Sesi Ini", use_container_width=True)
    if reset_button:
        st.session_state.chat_history = []
        st.success("Sesi obrolan dibersihkan!")
        time.sleep(0.5)
        st.rerun()

# ── 3. SIMULASI API EKSTERNAL (Cek Stok Produk) ──────────────────────────────
def panggil_api_stok_sepeda(jenis_sepeda: str) -> str:
    data_stok = {
        "mtb": "Polygon Siskiu D7 (Sisa 2 unit - Rp 12.000.000)",
        "road": "Polygon Strattos S5 (Sisa 1 unit - Rp 15.000.000)",
        "lipat": "Pacific Noris Arm (Sisa 5 unit - Rp 4.500.000)"
    }
    return data_stok.get(jenis_sepeda.lower().strip(), "Maaf banget kak, tipe sepeda itu lagi kosong di gudang kita.")

# ── 4. MANAJEMEN RIWAYAT PESAN (CHAT UI) ──────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    avatar_icon = "🚴" if message["role"] == "user" else "🚲"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.write(message["content"])

# ── 5. PROSES INPUT USER (DARI TEKS INPUT MAUPUN TOMBOL PINTAS) ───────────────
# Membaca input, apakah diketik manual atau dipicu oleh klik tombol rekomendasi di sidebar
user_input = st.chat_input("Ada yang bisa dibantu seputar sepeda, bro?")
if pemicu_chat_otomatis and not user_input:
    user_input = pemicu_chat_otomatis

if user_input:
    with st.chat_message("user", avatar="🚴"):
        st.write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if not google_api_key:
        with st.chat_message("assistant", avatar="🚲"):
            st.warning("🔑 Masukkan Google AI API Key Anda di sidebar terlebih dahulu ya, bro!")
        st.stop()
        
    try:
        client = genai.Client(api_key=google_api_key)
        
        # Deteksi Context API Toko Sepeda
        api_data_context = "Tidak membutuhkan data produk."
        if any(keyword in user_input.lower() for keyword in ["stok", "beli", "harga", "ready"]):
            if any(x in user_input.lower() for x in ["mtb", "gunung"]): api_data_context = panggil_api_stok_sepeda("mtb")
            elif any(x in user_input.lower() for x in ["road", "balap"]): api_data_context = panggil_api_stok_sepeda("road")
            elif any(x in user_input.lower() for x in ["lipat", "seli"]): api_data_context = panggil_api_stok_sepeda("lipat")

        system_instruction = f"""Kamu adalah GowesBot, seorang customer service yang ramah dan super santai di toko sepeda 'GowesAja'.
Gunakan bahasa gaul, santai, layaknya anak komunitas sepeda tapi tetap membantu (gunakan kata panggilan 'kak', 'bro', 'sis', 'nih', 'lho').

Domain Pengetahuan: Hanya seputar dunia sepeda (tips mekanik, rute gowes, komunitas, dan produk). 
Jika ditanya di luar topik sepeda, tolak dengan halus dan candaan khas anak gowes.

Fitur Tambahan:
1. Memori & Konteks: Perhatikan riwayat pesan sebelumnya. Ingat preferensi sepeda atau nama user jika disebutkan.
2. Rekomendasi: Berikan rekomendasi rute bersepeda atau aksesoris tambahan yang relevan di akhir jawabanmu.

INTEGRASI API TOKO:
Jika user bertanya tentang ketersediaan stok atau harga untuk sepeda jenis MTB/Gunung, Road/Balap, atau Lipat, gunakan data akurat dari sistem internal ini:
- Data Real-time dari Gudang: {api_data_context}
"""

        contents_payload = []
        for msg in st.session_state.chat_history:
            role_type = "user" if msg["role"] == "user" else "model"
            contents_payload.append(
                types.Content(role=role_type, parts=[types.Part.from_text(text=msg["content"])])
            )

        with st.chat_message("assistant", avatar="🚲"):
            with st.spinner("GowesBot lagi ngetik jawaban... 🚲💨"):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7
                    )
                )
                
                ai_response_text = response.text
                st.write(ai_response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response_text})
                
                st.rerun()

    except Exception as e:
        with st.chat_message("assistant", avatar="🚲"):
            st.error(f"Waduh ada kendala teknis nih bro: {str(e)}")
