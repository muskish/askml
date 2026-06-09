import os
import trafilatura
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import pickle
import requests

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BM25_CACHE = "vectorstore/bm25_index.pkl"

def scrape_url(url):
    """Scrape clean text from any URL"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: {response.status_code}")

    text = trafilatura.extract(
        response.text,
        include_tables=False,
        no_fallback=False,
    )

    if not text or len(text.strip()) < 200:
        raise ValueError("Could not extract meaningful content from this URL")

    return text

def ingest_url(url):
    """Scrape URL, chunk, embed, and add to existing vectorstore"""

    # ── Scrape ──────────────────────────────────────────
    print(f"🌐 Scraping {url}...")
    text = scrape_url(url)
    print(f"✅ Extracted {len(text)} characters")

    # ── Chunk ───────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_text(text)
    metadatas = [{"title": url, "url": url, "chunk_index": i} for i, _ in enumerate(chunks)]
    print(f"✂️  Created {len(chunks)} chunks")

    # ── Embed + Add to ChromaDB ──────────────────────────
    print(f"⏳ Embedding and adding to vectorstore...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    db.add_texts(texts=chunks, metadatas=metadatas)
    print(f"✅ Added {len(chunks)} chunks to vectorstore")

    # ── Rebuild BM25 index ───────────────────────────────
    print(f"🔄 Rebuilding BM25 index...")
    from rank_bm25 import BM25Okapi
    all_data = db._collection.get()
    documents = all_data["documents"]
    metadatas_all = all_data["metadatas"]
    tokenized = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized)

    with open(BM25_CACHE, "wb") as f:
        pickle.dump((bm25, documents, metadatas_all), f)
    print(f"✅ BM25 index rebuilt with {len(documents)} total chunks")

    return len(chunks)

if __name__ == "__main__":
    # Test it
    url = "https://en.wikipedia.org/wiki/Llama_(language_model)"
    count = ingest_url(url)
    print(f"\nDone! Added {count} chunks from {url}")