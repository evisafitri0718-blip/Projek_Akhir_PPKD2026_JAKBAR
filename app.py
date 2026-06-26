


import streamlit as st
from rag_pipeline import build_rag_pipeline

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Recruitment AI",
    page_icon="👔",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.title-box {
    background: linear-gradient(90deg, #1f4e79, #2e75b6);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="title-box">
    <h1>👔 Recruitment & Screening AI</h1>
    <h3>PT. KPOP IN INDONESIA</h3>
    <p>AI-Powered Recruitment Decision Support System</p>
</div>
""", unsafe_allow_html=True)

st.info(
    "🎓 Final Project PPKD 2026 Jakarta Barat | 🤖 LLM + RAG Recruitment System"
)

# =========================
# LOAD PIPELINE
# =========================
@st.cache_resource
def load_pipeline():
    return build_rag_pipeline()

try:
    qa_chain = load_pipeline()
    st.success("✅ Recruitment Assistant Ready")
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# =========================
# SESSION STATE
# =========================
if "query" not in st.session_state:
    st.session_state.query = ""

if "result" not in st.session_state:
    st.session_state.result = None

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.header("📋 Available Positions")

    st.markdown("""
    👔 Store Manager

    🎨 Visual Merchandiser

    💰 Cashier Supervisor
    """)

    st.markdown("---")

    st.header("💡 Example Questions")

    st.markdown("""
    🔹 Who is the best candidate for Store Manager?

    🔹 Who has retail management certification?

    🔹 Show candidates for Visual Merchandiser.

    🔹 Recommend the most suitable candidate.

    🔹 Which candidate has the highest experience?
    """)

    st.markdown("---")

    st.header("🚀 Technologies")

    st.markdown("""
    ✅ Streamlit

    ✅ LangChain

    ✅ ChromaDB

    ✅ Llama 3

    ✅ Retrieval Augmented Generation (RAG)
    """)

# =========================
# MAIN
# =========================
st.header("💬 Ask About Candidates")

query = st.text_input(
    "Enter your question:",
    placeholder="Example: Who is the best candidate for Store Manager?",
    key="query"
)

# BUTTONS
col1, col2 = st.columns(2)

with col1:
    search_btn = st.button(
        "🚀 Search Candidate",
        use_container_width=True
    )

def reset_app():
    st.session_state.clear()

with col2:
    st.button(
        "🔄 Reset",
        use_container_width=True,
        on_click=reset_app
    )

# SEARCH
if search_btn:

    if query:

        with st.spinner("🤖 Analyzing candidate profiles..."):

            try:

                result = qa_chain.invoke(query)

                st.session_state.result = result

            except Exception as e:
                st.error(f"Error: {e}")

# SHOW RESULT
if st.session_state.result:

    st.markdown("## 🎯 Recommendation")

    st.success(
        st.session_state.result["result"]
    )

    with st.expander("📄 Retrieved Candidate Documents"):

        for i, doc in enumerate(
            st.session_state.result["source_documents"],
            start=1
        ):

            st.markdown(f"### Source {i}")

            st.code(
                doc.page_content[:800],
                language="text"
            )

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown("""
<div class="footer">
<b>🎓 Final Project PPKD 2026 Jakarta Barat</b><br>
Recruitment & Screening Assistant using LLM + RAG<br>
Powered by Streamlit, LangChain, ChromaDB, and Llama 3
</div>
""", unsafe_allow_html=True)