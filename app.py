


import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

# ==================== SYSTEM PROMPT ====================
SYSTEM_PROMPT = """
Kamu adalah Asisten Rekrutmen & Screening untuk PT. Mitra Retail Indonesia.
Tugasmu membantu tim HR mencari dan mengevaluasi kandidat.

ATURAN:
1. Jawab HANYA berdasarkan dokumen recruitment_data.txt
2. Jika data tidak ada, katakan: "Maaf, data tidak tersedia"
3. Jangan gunakan pengetahuan di luar dokumen
4. JANGAN berikan rekomendasi diskriminatif (SARA, gender, usia)
5. Gunakan Bahasa Indonesia yang profesional dan formal
"""

# ==================== BUILD RAG ====================
def build_rag_pipeline():
    # Load dokumen
    try:
        loader = TextLoader("data/recruitment_data.txt", encoding="utf-8")
        documents = loader.load()
    except:
        loader = TextLoader("recruitment_data.txt", encoding="utf-8")
        documents = loader.load()
    
    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    
    # Embedding
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Vector Store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # LLM Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan di .env")
    
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=api_key,
        temperature=0.3
    )
    
    # Prompt
    prompt_template = f"""
{SYSTEM_PROMPT}

Context:
{{context}}

Pertanyaan: {{question}}

Jawaban:
"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # RAG Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

# ==================== STREAMLIT UI ====================
st.set_page_config(
    page_title="Asisten Rekrutmen Ritel",
    page_icon="👔",
    layout="wide"
)

st.title("👔 Asisten Rekrutmen & Screening")
st.subheader("PT. Mitra Retail Indonesia")
st.markdown("---")

@st.cache_resource
def load_pipeline():
    with st.spinner("🔄 Memuat pipeline RAG..."):
        return build_rag_pipeline()

try:
    qa_chain = load_pipeline()
    st.success("✅ Pipeline RAG siap digunakan!")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("Pastikan file .env berisi GROQ_API_KEY dan data/recruitment_data.txt ada")
    st.stop()

with st.sidebar:
    st.header("📋 Informasi")
    st.markdown("""
    **10 Kandidat | 3 Posisi**
    - Store Manager
    - Visual Merchandiser  
    - Cashier Supervisor
    """)
    st.header("💡 Contoh Pertanyaan")
    st.markdown("""
    - Siapa kandidat terbaik untuk Store Manager?
    - Tampilkan semua kandidat Visual Merchandiser
    - Siapa yang punya sertifikasi manajemen ritel?
    """)

st.header("💬 Tanya tentang Kandidat")

query = st.text_input(
    "Masukkan pertanyaan Anda:",
    placeholder="Contoh: Siapa kandidat yang cocok untuk Store Manager?",
    key="query_input"
)

col1, col2 = st.columns([1, 5])

with col1:
    submit = st.button("🔍 Tanya", type="primary", use_container_width=True)

with col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.query_input = ""
        st.rerun()

if submit and query:
    with st.spinner("🧠 Mencari jawaban..."):
        try:
            result = qa_chain.invoke(query)
            st.markdown("### 📝 Jawaban")
            st.info(result["result"])
            
            with st.expander("📄 Sumber Dokumen"):
                for i, doc in enumerate(result["source_documents"], 1):
                    st.markdown(f"**Sumber {i}:**")
                    st.text(doc.page_content[:300] + "...")
                    st.markdown("---")
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("Dibuat untuk proyek LLM + RAG | Data analis amatur")