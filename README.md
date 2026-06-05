# 🤖 AskML — Production-Grade RAG Chatbot

A domain-specific question-answering system built over AI/ML Wikipedia articles.
Ask any question about machine learning concepts and get cited, grounded answers.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--store-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.1-purple)

---

## 🏗️ Architecture

User Question
↓
┌─────────────────────────────────┐
│        Hybrid Retrieval         │
│  BM25 Keyword + Vector Search   │
│         (top 8 chunks)          │
└─────────────────────────────────┘

↓
┌─────────────────────────────────┐
│       Cohere Re-ranker          │
│    Narrows to top 3 chunks      │
└─────────────────────────────────┘

↓
┌─────────────────────────────────┐
│     Groq LLaMA 3.1 8B           │
│  Citation-enforced generation   │
└─────────────────────────────────┘

↓
Answer + Sources
---

## ✨ Features

- **Hybrid Retrieval** — combines BM25 keyword search with semantic vector search for better recall
- **Re-ranking** — Cohere cross-encoder re-ranks retrieved chunks by relevance
- **Citation Enforcement** — LLM is prompted to cite every claim; declines if evidence is missing
- **20 AI/ML Articles** — covers transformers, backpropagation, CNNs, RAG, fine-tuning, and more
- **Cyberpunk UI** — Streamlit chat interface with persistent history

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
| UI | Streamlit |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/askml.git
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
$env:PYTHONPATH="."; streamlit run src/app.py   # Windows
PYTHONPATH=. streamlit run src/app.py            # Mac/Linux
```

---

## 📁 Project Structure
askml/
├── data/              # Downloaded Wikipedia articles
├── vectorstore/       # ChromaDB persistent storage + BM25 cache
├── src/
│   ├── ingest.py      # Document ingestion, chunking, embedding
│   ├── retrieve.py    # Hybrid retrieval + Cohere re-ranking
│   ├── generate.py    # Prompt building + LLM answer generation
│   └── app.py         # Streamlit chat UI
├── .env               # API keys (never committed)
├── requirements.txt
└── README.md
---

## 💡 Why Hybrid Retrieval?

Pure vector search misses exact keyword matches. Pure BM25 misses semantic similarity.
Combining both gives significantly better recall:

| Method | Good at |
|---|---|
| Vector Search | "What is similar to gradient descent?" |
| BM25 | "What is LSTM?" (exact term match) |
| **Hybrid** | **Both** |

---

## 🔮 Roadmap

- [ ] URL ingestion — paste any webpage into the knowledge base
- [ ] Evaluation pipeline — golden Q&A dataset with faithfulness scoring
- [ ] Observability — request tracing with Langfuse
