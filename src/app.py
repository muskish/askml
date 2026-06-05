import streamlit as st
from src.generate import answer_question

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

/* ── Background ── */
.stApp {
    background-color: #0a0a0f;
    background-image: 
        linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}

/* ── Main title ── */
h1 {
    font-family: 'Orbitron', monospace !important;
    color: #00ffff !important;
    text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
    letter-spacing: 4px;
}

/* ── Caption ── */
.stApp p, .stApp div[data-testid="stCaptionContainer"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #00ffaa !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0d0d1a !important;
    border-right: 1px solid #00ffff33;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    font-family: 'Orbitron', monospace !important;
    color: #ff00ff !important;
    text-shadow: 0 0 10px #ff00ff;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    color: #00ffaa !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Sidebar buttons (example questions) ── */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid #00ffff55 !important;
    color: #00ffff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    text-align: left !important;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton button:hover {
    border-color: #00ffff !important;
    box-shadow: 0 0 10px #00ffff55;
    color: #ffffff !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background-color: #0d0d1a !important;
    border: 1px solid #00ffff22 !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stChatMessage"] p {
    color: #e0e0ff !important;
}

/* ── User message ── */
[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: #ff00ff44 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background-color: #0d0d1a !important;
    border: 1px solid #00ffff !important;
    border-radius: 4px !important;
    box-shadow: 0 0 15px #00ffff33;
}

[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #00ffff !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Status box ── */
[data-testid="stStatus"] {
    background-color: #0d0d1a !important;
    border: 1px solid #ff00ff44 !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: #ff00ff !important;
}

/* ── Expander (Sources) ── */
[data-testid="stExpander"] {
    background-color: #0d0d1a !important;
    border: 1px solid #00ffff33 !important;
}

[data-testid="stExpander"] summary {
    color: #ff00ff !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stExpander"] a {
    color: #00ffff !important;
}

/* ── Divider ── */
hr {
    border-color: #00ffff33 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #00ffff55; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00ffff; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AskML",
    page_icon="🤖",
    layout="centered"
)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 AskML")
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
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main UI ───────────────────────────────────────────────
st.title("🤖 AskML")
st.caption("Ask anything about AI and Machine Learning — answers grounded in Wikipedia sources.")

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    parts = s.split(" — ")
                    title_clean = parts[0].split("] ")[-1]
                    url = parts[1] if len(parts) > 1 else "#"
                    st.markdown(f"- [{title_clean}]({url})")

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
        st.write("🔍 Running hybrid retrieval (BM25 + vector search)...")
        st.write("🎯 Re-ranking chunks with Cohere...")
        st.write("⚡ Generating answer with Groq LLaMA 3.1...")
        answer, sources = answer_question(query)
        status.update(label="✅ Done!", state="complete", expanded=False)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })

    st.rerun()