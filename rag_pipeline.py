


import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def load_system_prompt():
    """Load system prompt from file"""
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a Recruitment Assistant. Answer based on the provided data."


def build_rag_pipeline():
    """Build RAG pipeline for retail recruitment"""

    print("📄 Loading documents...")

    # Try loading from data folder first, otherwise from root folder
    try:
        loader = TextLoader("data/recruitment_data.txt", encoding="utf-8")
        documents = loader.load()
        print("✅ Data found in data folder")
    except FileNotFoundError:
        try:
            loader = TextLoader("recruitment_data.txt", encoding="utf-8")
            documents = loader.load()
            print("✅ Data found in root folder")
        except FileNotFoundError:
            raise FileNotFoundError("❌ recruitment_data.txt file not found!")

    print("✂️ Performing chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "[CANDIDATE", "[JOB VACANCY"]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✅ Generated {len(chunks)} chunks")

    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    print("💾 Saving to vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Check Groq API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found!")

    print("🤖 Setting up LLM (Groq)...")
    print("MODEL USED: llama-3.3-70b-versatile")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.5
    )

    # Load system prompt
    system_prompt = load_system_prompt()

    # Custom prompt template
    prompt_template = f"""
{system_prompt}

Context from recruitment documents:
{{context}}

User question:
{{question}}

Answer (based only on the context above, use English):
"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    print("🔗 Building RAG pipeline...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    print("✅ RAG pipeline is ready!")
    return qa_chain


# Direct testing
if __name__ == "__main__":

    pipeline = build_rag_pipeline()

    test_queries = [
        "Who is the best candidate for Store Manager?",
        "What are the qualifications for Visual Merchandiser?",
        "Who has retail management certification?"
    ]

    for query in test_queries:
        print(f"\n❓ Question: {query}")
        result = pipeline.invoke(query)
        print(f"💬 Answer: {result['result']}")
        print("-" * 50)