# 🤖 AskML — Production-Grade RAG Chatbot

🔗 **[Live Demo](https://askml-assistant.streamlit.app)**

A domain-specific question-answering system built over AI/ML Wikipedia articles.
Ask any question about machine learning concepts and get cited, grounded answers — or paste any URL to expand the knowledge base on the fly.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--store-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.1-purple)

---

## 🏗️ Architecture

```
User Question
│
▼
Hybrid Retrieval
├── BM25 Keyword Search
└── Vector Similarity Search
│
│  top 8 chunks
▼
Cohere Re-ranker
│
│  top 3 chunks
▼
Groq LLaMA 3.1 8B
└── Citation-enforced prompt
│
▼
Answer + Sources

```
---

## ✨ Features

- **Hybrid Retrieval** — combines BM25 keyword search with semantic vector search for better recall
- **Re-ranking** — Cohere cross-encoder re-ranks retrieved chunks by relevance
- **Citation Enforcement** — LLM is prompted to cite every claim; declines if evidence is missing
- **Live URL Ingestion** — paste any webpage and it's scraped, chunked, and added to the knowledge base in real time
- **20 AI/ML Articles** — covers transformers, backpropagation, CNNs, RAG, fine-tuning, and more
- **Editorial UI** — clean, warm Streamlit chat interface with persistent history

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Chunking | LangChain RecursiveCharacterTextSplitter |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB (local, persistent) |
| Keyword Search | BM25 (rank-bm25) |
| Re-ranker | Cohere `rerank-english-v3.0` |
| LLM | Groq LLaMA 3.1 8B Instant |
| Web Scraping | trafilatura |
| UI | Streamlit |
| Hosting | Streamlit Community Cloud |

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the repo
```bash
git clone https://github.com/muskish/askml.git
cd askml
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file:

GROQ_API_KEY=your_groq_key_here
COHERE_API_KEY=your_cohere_key_here

### 5. Ingest documents
```bash
python src/ingest.py
```

### 6. Run the app
```bash
PYTHONPATH=. streamlit run src/app.py   # Mac/Linux/Git Bash
$env:PYTHONPATH="."; streamlit run src/app.py   # PowerShell
```

---

## 📁 Project Structure

| File | Purpose |
|---|---|
| `src/ingest.py` | Document ingestion, chunking, embedding |
| `src/retrieve.py` | Hybrid retrieval + Cohere re-ranking |
| `src/generate.py` | Prompt building + LLM answer generation |
| `src/scraper.py` | Live URL ingestion (trafilatura) |
| `src/app.py` | Streamlit chat UI |
| `startup.py` | Builds knowledge base on first cloud launch |
| `data/` | Downloaded Wikipedia articles |
| `vectorstore/` | ChromaDB persistent storage + BM25 cache |

## 💡 Why Hybrid Retrieval?

Pure vector search misses exact keyword matches. Pure BM25 misses semantic similarity.
Combining both gives significantly better recall:

| Method | Good at |
|---|---|
| Vector Search | "What is similar to gradient descent?" |
| BM25 | "What is LSTM?" (exact term match) |
| **Hybrid** | **Both** |

---

## ⚠️ Known Limitations

- On Streamlit Cloud's free tier, the vectorstore is rebuilt from scratch whenever the server restarts (no persistent disk storage), causing a ~2 minute delay on first load after inactivity.
- Production fix: migrate to a managed vector database (Pinecone/Weaviate) for true persistence.

---

## 🔮 Roadmap

- [ ] Evaluation pipeline — golden Q&A dataset with faithfulness scoring
- [ ] Observability — request tracing with Langfuse
- [ ] PDF/PPT upload support
