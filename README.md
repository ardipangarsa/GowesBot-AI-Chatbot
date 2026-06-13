# 🚲 GowesBot Pro: Chatbot Customer Service Berbasis AI

GowesBot Pro adalah aplikasi chatbot pintar berbasis kecerdasan buatan (*Artificial Intelligence*) yang dirancang khusus untuk skenario *Customer Service* di toko sepeda fiktif "GowesAja". Aplikasi ini dibangun menggunakan framework **Streamlit** dan ditenagai oleh model LLM **Google Gemini 2.5 Flash** melalui Google GenAI SDK resmi.

## 🌟 Fitur Utama & Parameter Kreatif
*   **Natural Language Processing (NLP):** Memahami konteks pertanyaan pengguna dengan sangat baik dan memberikan respons relevan menggunakan model `gemini-2.5-flash`.
*   **Persona & Gaya Bahasa Santai:** Menggunakan pembawaan kasual khas anak komunitas sepeda namun tetap responsif dan solutif sebagai asisten *customer service*.
*   **Domain Spesifik (Hobi/Sepeda):** Memiliki pemahaman mendalam seputar dunia sepeda, rute gowes, tips mekanik, dan secara halus menolak topik di luar domain tersebut.
*   **Integrasi API Eksternal (Simulasi):** Terintegrasi secara dinamis dengan modul pengecekan stok produk gudang (MTB, Road Bike, Sepeda Lipat) untuk menyajikan data harga dan unit secara *real-time*.
*   **Fitur Quick Recommendation Triggers:** Menyediakan tombol rekomendasi otomatis di sidebar untuk memicu pertanyaan populer secara instan dan meningkatkan *User Experience* (UX).
*   **Antarmuka Premium (Custom UI):** Desain balon chat interaktif berbasis grid dengan visual kontras warna ganjil-genap dan ikon avatar kustom (`🚴` & `🚲`).

---

## 🛠️ Arsitektur Teknologi & Library
*   **Bahasa Pemrograman:** Python 3.10+
*   **Framework UI:** Streamlit
*   **AI Engine:** Google GenAI SDK (`google-genai`)
*   **Jalur Publik (Tunneling):** PyNgrok (Terintegrasi Google Colab Secrets)

---

## 🚀 Cara Menjalankan Proyek (Melalui Google Colab)

1. **Persiapan Token & Key:**
   * Dapatkan Google AI Studio API Key.
   * Dapatkan Authtoken dari akun Ngrok Anda.
2. **Konfigurasi Colab Secrets:**
   * Buka menu *Secrets* (ikon kunci 🔑) di Google Colab.
   * Tambahkan secret baru dengan nama `NGROK_TOKEN` dan masukkan token Ngrok Anda.
3. **Eksekusi Cell:**
   * Jalankan instalasi dependensi: `pip install -r requirements.txt`.
   * Jalankan file aplikasi utama `gowes_app.py` menggunakan perintah eksekusi Ngrok jembatan port.
   * Buka tautan HTTPS publik yang dihasilkan oleh Ngrok untuk mengakses antarmuka chat.

