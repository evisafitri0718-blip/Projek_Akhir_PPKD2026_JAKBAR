

# 👔 Recruitment & Screening Assistant - PT. Mitra Retail Indonesia

AI chatbot for HR teams to help search, evaluate, and compare job candidates in the retail sector. Built using RAG (Retrieval-Augmented Generation) technology with LangChain.

---

## System Architecture

```
Candidate Data (TXT)
       |
  Document Loader        <- Reads candidate data file
       |
  Text Splitter          <- Splits documents into small chunks
       |
HuggingFace Embeddings   <- Converts text to vector numbers
       |
  FAISS Vector Store     <- Stores vectors for fast search
       |
    Retriever            <- Finds most relevant chunks for queries
       |
 Groq LLM (Llama 3)     <- Generates answers from retrieved chunks
       |
  Final Answer
```

---

## Tech Stack

- **LLM:** Groq API + Llama 3 70B / Mixtral 8x7B
- **RAG Framework:** LangChain
- **Embeddings:** HuggingFace (all-MiniLM-L6-v2)
- **Vector Store:** FAISS (local, no server needed)
- **UI:** Streamlit

---

## Setup and Run Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create .env file

Copy `.env.example` and rename to `.env`:

```bash
cp .env.example .env
```

Then fill in your Groq API key in `.env`:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

**How to get an API key:**
1. Go to https://console.groq.com
2. Sign up or log in
3. Click "Create API Key"
4. Copy and paste it into the .env file

### 3. Run the application

```bash
streamlit run app.py
```

Open your browser and go to **http://localhost:8501**

---

## Project Structure

```
Recruitment & Screening/
├── app.py                  <- Streamlit interface (entry point)
├── rag_pipeline.py         <- RAG LangChain logic
├── requirements.txt        <- Required libraries
├── system_prompt.txt       <- System prompt + security guardrails
├── .env.example            <- API key template
├── .env                    <- API key (DO NOT commit to GitHub)
├── .gitignore
├── README.md
└── data/
    └── recruitment_data.txt  <- Candidate knowledge base
```

---

## Available Candidate Data

### Open Positions

| Position | Location | Qualifications |
|----------|----------|----------------|
| Store Manager | South Jakarta | Bachelor's in Management/Economics, 3+ years experience |
| Visual Merchandiser | Central Jakarta | D3/Bachelor's in Design, 2+ years experience |
| Cashier Supervisor | Tangerang | Minimum high school, 1+ years experience |

### Candidate List (10 People)

| No | Name | Position Applied | Experience |
|----|------|------------------|------------|
| 1 | Andi Pratama | Store Manager | 5 years (Alfamart, Indomaret) |
| 2 | Budi Santoso | Store Manager | 5 years (Giant, Lotte Mart) |
| 3 | Citra Dewi | Visual Merchandiser | 4 years (ZARA, H&M) |
| 4 | Dedi Firmansyah | Cashier Supervisor | 4 years (Carrefour) |
| 5 | Eka Yulianti | Visual Merchandiser | 4 years (Uniqlo) |
| 6 | Fitri Handayani | Store Manager | 6 years (Sogo, Seibu, Metro) |
| 7 | Gilang Ramadhan | Cashier Supervisor | 3 years (Hypermart) |
| 8 | Hana Permata | Visual Merchandiser | 3 years (IKEA) |
| 9 | Iwan Setiawan | Store Manager | 5 years (Ramayana) |
| 10 | Jihan Maulida | Cashier Supervisor | 3 years (Transmart) |

---

## Example Questions

- "Who is the best candidate for Store Manager?"
- "Show all Visual Merchandiser candidates"
- "Who has retail management certification?"
- "Find candidates for Cashier Supervisor in Tangerang"
- "Compare Andi Pratama and Iwan Setiawan for Store Manager"
- "What are the qualifications for Visual Merchandiser?"
- "Which candidates have more than 3 years of experience?"

---

## Example Output

**Question:** "Who is the best candidate for Store Manager?"

**Answer:**

```
Based on available data, the best candidates for Store Manager are:

1. Andi Pratama
   - Education: Bachelor's in Management - UI
   - Experience: 5 years (Store Manager at Alfamart & Indomaret)
   - Certification: Retail Management - LSP Ritel
   - Strength: Experience managing 20 employees, available in 2 weeks

2. Fitri Handayani
   - Education: Bachelor's in Management - UNIBRAW
   - Experience: 6 years (Store Manager at Metro, Sogo, Seibu)
   - Certification: Retail Management - LSP Ritel
   - Strength: Experience in high-end department stores

Recommendation: Andi Pratama is more ready due to recent experience in modern retail and faster availability.
```

---

## Deployment to Streamlit Community Cloud

1. Upload project to GitHub (make sure .env is NOT committed)
2. Go to https://share.streamlit.io
3. Connect to your GitHub repository
4. Add GROQ_API_KEY in Secrets:
   ```
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
   ```
5. Deploy

**Note:** The .env file is not used on Streamlit Cloud. The API key is read from Secrets configured in the dashboard.

---

## 🛡️ Security Features

| Protection | Implementation |
|------------|----------------|
| Prompt Injection | System prompt with security guardrails |
| Sensitive Data | Restricted from accessing outside documents |
| Discrimination | Prohibited from comparing race/gender/age |
| Hallucination | Answers based only on available data |

---

## 📝 License

This project is created for educational and portfolio purposes.

---

## 👤 Author

**Name:** [Your Name]  
**Role:** Data Analyst Amateur  

---

**Made with ❤️ for LLM + RAG project**