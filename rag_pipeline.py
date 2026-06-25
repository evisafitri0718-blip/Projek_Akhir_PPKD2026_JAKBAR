


import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def load_system_prompt():
    """Load system prompt dari file"""
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Kamu adalah Asisten Rekrutmen. Jawab berdasarkan data yang diberikan."

def build_rag_pipeline():
    """Membangun pipeline RAG untuk rekrutmen ritel"""
    
    print("📄 Loading dokumen...")
    
    # Coba load dari folder data/ dulu, kalau tidak ada coba dari root
    try:
        loader = TextLoader("data/recruitment_data.txt", encoding="utf-8")
        documents = loader.load()
        print("✅ Data ditemukan di folder data/")
    except FileNotFoundError:
        try:
            loader = TextLoader("recruitment_data.txt", encoding="utf-8")
            documents = loader.load()
            print("✅ Data ditemukan di root folder")
        except FileNotFoundError:
            raise FileNotFoundError("❌ File recruitment_data.txt tidak ditemukan!")
    
    print("✂️ Melakukan chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "[KANDIDAT", "[LOWONGAN"]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Terbentuk {len(chunks)} chunk")
    
    print("🧠 Membuat embedding...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("💾 Menyimpan ke vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Cek API Key Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY tidak ditemukan!")
    
    print("🤖 Menyiapkan LLM (Groq)...")
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=api_key,
        temperature=0.3
    )
    
    # Load system prompt
    system_prompt = load_system_prompt()
    
    # Custom prompt template
    prompt_template = f"""
{system_prompt}

Context dari dokumen rekrutmen:
{{context}}

Pertanyaan user:
{{question}}

Jawaban (berdasarkan context di atas, gunakan Bahasa Indonesia):
"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    print("🔗 Membuat RAG pipeline...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("✅ Pipeline RAG siap digunakan!")
    return qa_chain

# Untuk testing langsung
if __name__ == "__main__":
    pipeline = build_rag_pipeline()
    
    # Test query
    test_queries = [
        "Siapa kandidat terbaik untuk Store Manager?",
        "Apa saja kualifikasi untuk Visual Merchandiser?",
        "Siapa saja yang punya sertifikasi manajemen ritel?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Pertanyaan: {query}")
        result = pipeline.invoke(query)
        print(f"💬 Jawaban: {result['result']}")
        print("-" * 50)