# 👔 Asisten Rekrutmen & Screening - PT. Mitra Retail Indonesia

Chatbot AI untuk tim HR yang membantu mencari, mengevaluasi, dan membandingkan kandidat pekerjaan di bidang ritel. Dibangun menggunakan teknologi RAG (Retrieval-Augmented Generation) dengan LangChain.

## Arsitektur Sistem

```
Data Kandidat (TXT)
       |
  Document Loader        <- Membaca file data kandidat
       |
  Text Splitter          <- Memotong dokumen jadi chunk kecil
       |
HuggingFace Embeddings   <- Mengubah teks jadi vektor angka
       |
  FAISS Vector Store     <- Menyimpan vektor untuk pencarian cepat
       |
    Retriever            <- Mencari chunk paling relevan saat ada query
       |
 Groq LLM (Llama 3)     <- Merangkai jawaban dari chunk yang diambil
       |
  Jawaban Final
```

## Tech Stack

- LLM: Groq API + Llama 3 70B / Mixtral 8x7B
- RAG Framework: LangChain
- Embeddings: HuggingFace (all-MiniLM-L6-v2)
- Vector Store: FAISS (lokal, tidak perlu server)
- UI: Streamlit

## Cara Setup dan Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Buat file .env

Salin file `.env.example` dan rename menjadi `.env`:

```bash
cp .env.example .env
```

Lalu isi API key Groq di file `.env`:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Cara mendapatkan API key:
1. Buka https://console.groq.com
2. Daftar atau login
3. Klik "Create API Key"
4. Salin dan tempelkan ke file .env

### 3. Jalankan aplikasi

```bash
streamlit run app.py
```

Buka browser dan akses http://localhost:8501

## Struktur Project

```
Recruitment & Screening/
├── app.py                  <- Antarmuka Streamlit (entry point)
├── rag_pipeline.py         <- Logika RAG LangChain
├── requirements.txt        <- Daftar library yang dibutuhkan
├── system_prompt.txt       <- System prompt + security guardrails
├── .env.example            <- Template konfigurasi API key
├── .env                    <- API key (JANGAN di-commit ke GitHub)
├── .gitignore
├── README.md
└── data/
    └── recruitment_data.txt  <- Knowledge base kandidat
```

## Data Kandidat yang Tersedia

### Posisi yang Dibuka

| Posisi | Lokasi | Kualifikasi |
|--------|--------|-------------|
| Store Manager | Jakarta Selatan | S1 Manajemen/Ekonomi, 3+ tahun pengalaman |
| Visual Merchandiser | Jakarta Pusat | D3/S1 Desain, 2+ tahun pengalaman |
| Cashier Supervisor | Tangerang | Minimal SMA, 1+ tahun pengalaman |

### Daftar Kandidat (10 Orang)

| No | Nama | Posisi Dilamar | Pengalaman |
|----|------|----------------|------------|
| 1 | Andi Pratama | Store Manager | 5 tahun (Alfamart, Indomaret) |
| 2 | Budi Santoso | Store Manager | 5 tahun (Giant, Lotte Mart) |
| 3 | Citra Dewi | Visual Merchandiser | 4 tahun (ZARA, H&M) |
| 4 | Dedi Firmansyah | Cashier Supervisor | 4 tahun (Carrefour) |
| 5 | Eka Yulianti | Visual Merchandiser | 4 tahun (Uniqlo) |
| 6 | Fitri Handayani | Store Manager | 6 tahun (Sogo, Seibu, Metro) |
| 7 | Gilang Ramadhan | Cashier Supervisor | 3 tahun (Hypermart) |
| 8 | Hana Permata | Visual Merchandiser | 3 tahun (IKEA) |
| 9 | Iwan Setiawan | Store Manager | 5 tahun (Ramayana) |
| 10 | Jihan Maulida | Cashier Supervisor | 3 tahun (Transmart) |

## Contoh Pertanyaan

- "Siapa kandidat terbaik untuk posisi Store Manager?"
- "Tampilkan semua kandidat Visual Merchandiser"
- "Siapa saja yang punya sertifikasi manajemen ritel?"
- "Cari kandidat untuk Cashier Supervisor di Tangerang"
- "Bandingkan Andi Pratama dan Iwan Setiawan untuk Store Manager"
- "Apa saja kualifikasi untuk posisi Visual Merchandiser?"
- "Kandidat mana yang memiliki pengalaman lebih dari 3 tahun?"

## Contoh Output

**Pertanyaan:** "Siapa kandidat terbaik untuk Store Manager?"

**Jawaban:**
```
Berdasarkan data yang tersedia, kandidat terbaik untuk posisi Store Manager adalah:

1. Andi Pratama
   - Pendidikan: S1 Manajemen - UI
   - Pengalaman: 5 tahun (Store Manager di Alfamart & Indomaret)
   - Sertifikasi: Manajemen Ritel - LSP Ritel
   - Kelebihan: Pengalaman kelola 20 karyawan, siap bergabung dalam 2 minggu

2. Fitri Handayani
   - Pendidikan: S1 Manajemen - UNIBRAW
   - Pengalaman: 6 tahun (Store Manager di Metro, Sogo, Seibu)
   - Sertifikasi: Manajemen Ritel - LSP Ritel
   - Kelebihan: Pengalaman di department store kelas atas

Rekomendasi: Andi Pratama lebih siap karena pengalaman terbaru di ritel modern dan ketersediaan yang lebih cepat.
```

## Deployment ke Streamlit Community Cloud

1. Upload project ke GitHub (pastikan .env tidak ikut ter-commit)
2. Buka https://share.streamlit.io
3. Hubungkan dengan repository GitHub
4. Tambahkan GROQ_API_KEY di bagian Secrets:
   ```
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
   ```
5. Deploy

Catatan: File .env tidak digunakan di Streamlit Cloud. API key dibaca dari Secrets yang dikonfigurasi di dashboard.

## 🛡️ Keamanan

| Proteksi | Implementasi |
|----------|--------------|
| Prompt Injection | System prompt dengan security guardrails |
| Data Sensitif | Dilarang mengakses di luar dokumen |
| Diskriminasi | Dilarang membandingkan SARA/gender/usia |
| Hallucination | Jawaban hanya berdasarkan data yang ada |

## 📝 Lisensi

Proyek ini dibuat untuk tujuan pendidikan dan portofolio.

## 👤 Author

**Nama:** [Nama Anda]  
**Peran:** Data Analyst Amateur  

---

**Dibuat dengan ❤️ untuk proyek LLM + RAG**