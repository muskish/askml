import streamlit as st
from src.generate import answer_question

import sys
import os

st.set_page_config(
    page_title="AskML",
    page_icon="assets/logo.png",
    layout="centered"
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from startup import is_vectorstore_ready, build_knowledge_base

if not is_vectorstore_ready():
    with st.status("⏳ Setting up knowledge base for the first time...", expanded=True) as status:
        st.write("📥 Downloading AI/ML articles from Wikipedia...")
        st.write("✂️  Chunking and embedding documents...")
        st.write("🔍 Building search indexes...")
        build_knowledge_base()
        status.update(label="✅ Knowledge base ready!", state="complete")
    st.rerun()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── Background ── */
.stApp {
    background-color: #fce8e0;
    background-image: radial-gradient(ellipse at 20% 20%, #fad4c8 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 80%, #f5e6d8 0%, transparent 50%);
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Main title ── */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #1a2744 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    text-shadow: none !important;
}

h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1a2744 !important;
    text-shadow: none !important;
}

/* ── All text ── */
.stApp p, .stApp div, .stApp span, .stApp li {
    font-family: 'DM Sans', sans-serif !important;
    color: #2d3a52 !important;
    text-shadow: none !important;
}

/* ── Caption ── */
div[data-testid="stCaptionContainer"] p {
    color: #544a45 !important;
    font-size: 0.9rem !important;
    font-style: italic !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #fdf4f0 !important;
    border-right: 1px solid #e8d5cc !important;
}

[data-testid="stSidebar"] h1 {
    font-family: 'Playfair Display', serif !important;
    color: #1a2744 !important;
    font-size: 1.4rem !important;
    text-shadow: none !important;
    letter-spacing: 0 !important;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #c4756a !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    text-shadow: none !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    color: #6b5c55 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] .stButton button {
    background: #ffffff !important;
    border: 1px solid #e0cdc7 !important;
    border-radius: 8px !important;
    color: #1a2744 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: #fff5f2 !important;
    border-color: #c4756a !important;
    color: #c4756a !important;
    box-shadow: 0 2px 8px rgba(196,117,106,0.12) !important;
    transform: translateY(-1px) !important;
}

/* ── Clear chat button ── */
[data-testid="stSidebar"] .stButton:last-child button {
    background: #fff5f2 !important;
    border: 1px solid #e0cdc7 !important;
    color: #c4756a !important;
    font-weight: 500 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 1px solid #edddd7 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    margin-bottom: 8px !important;
}

[data-testid="stChatMessageContent"] {
    padding: 0.85rem 1rem !important;
}

[data-testid="stChatMessage"] p {
    color: #1a2744 !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.7 !important;
    font-size: 0.95rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1.5px solid #e0cdc7 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #c4756a !important;
    box-shadow: 0 0 0 3px rgba(196,117,106,0.12) !important;
}

[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #f2f2f2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #b0a09a !important;
}

/* ── Status box ── */
[data-testid="stStatus"] {
    background-color: #fff9f7 !important;
    border: 1px solid #edddd7 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #6b5c55 !important;
}

[data-testid="stStatus"] p {
    color: #f2f2f2 !important;
    font-size: 0.85rem !important;
}

/* ── Expander (Sources) ── */
[data-testid="stExpander"] {
    background-color: #fff5f2 !important;
    border: 1px solid #edddd7 !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] summary {
    color: #c4756a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

[data-testid="stExpander"] a {
    color: #1a2744 !important;
    text-decoration: underline !important;
    text-decoration-color: #c4756a !important;
}

[data-testid="stExpander"] a:hover {
    color: #c4756a !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    gap: 0.45rem !important;
    font-size: 0.95rem !important;
}

[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0 !important;
    font-size: 1.15rem !important;
    line-height: 1 !important;
}

[data-testid="stExpander"] ul {
    margin: 0.5rem 0 0 1rem !important;
    padding: 0 !important;
}

[data-testid="stExpander"] li {
    margin-bottom: 0.35rem !important;
}

[data-testid="stExpander"] p {
    margin: 0 !important;
}

/* ── Text input (URL bar) ── */
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    border: 1px solid #e0cdc7 !important;
    border-radius: 8px !important;
    color: #1a2744 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #b0a09a !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #c4756a !important;
    box-shadow: 0 0 0 3px rgba(196,117,106,0.1) !important;
}

/* ── Divider ── */
hr {
    border-color: #e8d5cc !important;
    opacity: 1 !important;
}

/* ── Top toolbar ── */
[data-testid="stToolbar"] {
    background-color: #ffffff !important;
    border-bottom: 1px solid #e8d5cc !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #fce8e0; }
::-webkit-scrollbar-thumb { background: #dcc4bc; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #c4756a; }

/* ── Success/error messages ── */
[data-testid="stAlert"] {
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important;
}
            
/* ── Hide sidebar collapse button text ── */
[data-testid="collapsedControl"] {
    display: none !important;
}

button[kind="headerNoPadding"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AskML",
    page_icon="assets/logo.png",
    layout="centered"
)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    col1, col2 = st.columns([0.2, 0.8], gap="small")
    with col1:
        st.image("assets/logo.png", width=45)
    with col2:
        st.markdown("<h3 style='margin: 0; padding: 0; padding-top: 5px;'>AskML</h3>", unsafe_allow_html=True)
    st.markdown("A production-grade RAG chatbot over AI/ML knowledge.")
    st.divider()

    st.markdown("### 💡 Try these questions")
    example_questions = [
        "What is a transformer model?",
        "How does backpropagation work?",
        "What is the difference between CNN and RNN?",
        "Explain gradient descent",
        "What is overfitting and how to prevent it?",
        "How does attention mechanism work?",
        "What is transfer learning?",
        "Explain word2vec",
    ]

    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.divider()
    st.markdown("### 🛠️ How it works")
    st.markdown("""
    1. **Hybrid Retrieval** — BM25 + Vector Search
    2. **Re-ranking** — Cohere re-ranker
    3. **Generation** — Groq LLaMA 3.1
    4. **Citations** — Every claim is grounded
    """)

    st.divider()
    st.markdown("### 🌐 Add a URL")
    url_input = st.text_input("Paste any webpage URL", placeholder="https://...")
    if st.button("⚡ Ingest URL", use_container_width=True):
        if url_input.strip():
            with st.spinner("Scraping and ingesting..."):
                try:
                    from src.scraper import ingest_url
                    count = ingest_url(url_input.strip())
                    st.success(f"✅ Added {count} chunks!")
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
        else:
            st.warning("Please enter a URL first")


    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main UI ───────────────────────────────────────────────
col1, col2 = st.columns([0.1, 0.9], gap="small")
with col1:
    st.image("assets/logo.png", width=70)
with col2:
    st.markdown("<h1 style='margin: 0; padding: 0; padding-top: 8px;'>AskML</h1>", unsafe_allow_html=True)
st.caption("Ask anything about AI and Machine Learning — answers grounded in Wikipedia sources.")

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Helper for explicit chat avatars
def _chat_avatar_for_role(role):
    return "🟥" if role == "user" else "🌕" if role == "assistant" else role

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=_chat_avatar_for_role(msg["role"])):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 Sources"):
                source_lines = []
                for s in msg["sources"]:
                    parts = s.rsplit(" — ", 1)
                    title_label = parts[0]
                    if title_label.startswith("[") and "] " in title_label:
                        title_clean = title_label.split("] ")[-1]
                    else:
                        title_clean = title_label
                    url = parts[1] if len(parts) > 1 else None
                    if url:
                        source_lines.append(f"- [{title_clean}]({url})")
                    else:
                        source_lines.append(f"- {title_clean}")
                st.markdown("\n".join(source_lines))

# Handle example question click
if st.session_state.pending_question:
    query = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    query = st.chat_input("Ask a question about AI/ML...")

# Process query
if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Generate answer
    with st.status("Thinking...", expanded=True) as status:
        st.write("Running hybrid retrieval (BM25 + vector search)...")
        st.write("Re-ranking chunks with Cohere...")
        st.write("Generating answer with Groq LLaMA 3.1...")
        answer, sources = answer_question(query)
        status.update(label="✅ Done!", state="complete", expanded=False)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })

    st.rerun()