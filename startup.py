import os
import time
import requests
import pickle
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi

VECTORSTORE_DIR = "vectorstore"
DATA_DIR = "data"
BM25_CACHE = "vectorstore/bm25_index.pkl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOPICS = [
    "Large language model", "Transformer (machine learning model)",
    "Retrieval-augmented generation", "Reinforcement learning",
    "Convolutional neural network", "Recurrent neural network",
    "Generative adversarial network", "Transfer learning",
    "BERT (language model)", "GPT (language model)",
    "Diffusion model", "Word2vec", "Backpropagation",
    "Gradient descent", "Overfitting", "Support vector machine",
    "Random forest", "Natural language processing",
    "Computer vision", "Prompt engineering",
]

def is_vectorstore_ready():
    """Check if vectorstore already exists and has data"""
    if not os.path.exists(VECTORSTORE_DIR):
        return False
    files = os.listdir(VECTORSTORE_DIR)
    return len(files) > 0

def download_article(topic):
    headers = {"User-Agent": "AskML-RAG-Project/1.0"}
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": topic, "prop": "extracts",
        "explaintext": True, "redirects": 1,
    }
    response = requests.get(url, params=params, headers=headers, timeout=15)
    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    if "extract" not in page or not page["extract"].strip():
        raise ValueError("Empty extract")
    return page["title"], page["extract"]

def build_knowledge_base():
    """Download articles, chunk, embed, store — full pipeline"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    # ── Download articles ────────────────────────────────
    print("📥 Downloading articles...")
    all_docs = []
    for topic in TOPICS:
        try:
            title, text = download_article(topic)
            all_docs.append({"title": title, "text": text,
                             "url": f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"})
            print(f"  ✅ {title}")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ {topic}: {e}")

    # ── Chunk ────────────────────────────────────────────
    print(f"\n✂️  Chunking {len(all_docs)} articles...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks, metadatas = [], []
    for doc in all_docs:
        splits = splitter.split_text(doc["text"])
        for i, chunk in enumerate(splits):
            chunks.append(chunk)
            metadatas.append({"title": doc["title"],
                              "url": doc["url"], "chunk_index": i})

    # ── Embed + Store ────────────────────────────────────
    print(f"⏳ Embedding {len(chunks)} chunks...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    Chroma.from_texts(
        texts=chunks, embedding=embeddings,
        metadatas=metadatas, persist_directory=VECTORSTORE_DIR,
    )

    # ── BM25 index ───────────────────────────────────────
    print("🔍 Building BM25 index...")
    tokenized = [c.lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized)
    with open(BM25_CACHE, "wb") as f:
        pickle.dump((bm25, chunks, metadatas), f)

    print(f"\n✅ Knowledge base ready! {len(chunks)} chunks stored.")

if __name__ == "__main__":
    build_knowledge_base()