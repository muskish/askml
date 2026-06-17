import cohere
from dotenv import load_dotenv
load_dotenv()
import os
import pickle
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi
import streamlit as st

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BM25_CACHE = "vectorstore/bm25_index.pkl"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    return db

def build_bm25_index(db):
    """Build BM25 index from all chunks in ChromaDB and cache it"""
    print("⏳ Building BM25 index...")
    all_data = db._collection.get()
    documents = all_data["documents"]
    metadatas = all_data["metadatas"]

    tokenized = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized)

    # Cache to disk so we don't rebuild every time
    with open(BM25_CACHE, "wb") as f:
        pickle.dump((bm25, documents, metadatas), f)

    print(f"✅ BM25 index built with {len(documents)} chunks")
    return bm25, documents, metadatas

def load_bm25_index(db):
    """Load BM25 index from cache or build fresh"""
    if os.path.exists(BM25_CACHE):
        with open(BM25_CACHE, "rb") as f:
            bm25, documents, metadatas = pickle.load(f)
        return bm25, documents, metadatas
    return build_bm25_index(db)

def retrieve_chunks(query, k=5):
    """Hybrid retrieval: combine BM25 + vector search results"""
    db = load_vectorstore()
    bm25, documents, metadatas = load_bm25_index(db)

    # ── Vector search ──────────────────────────────────
    vector_results = db.similarity_search(query, k=k)
    vector_chunks = {
        r.page_content: {
            "text": r.page_content,
            "title": r.metadata["title"],
            "url": r.metadata["url"],
            "score": 1.0,  # vector results get high base score
        }
        for r in vector_results
    }

    # ── BM25 keyword search ─────────────────────────────
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    top_bm25_indices = sorted(
        range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True
    )[:k]

    bm25_chunks = {
        documents[i]: {
            "text": documents[i],
            "title": metadatas[i]["title"],
            "url": metadatas[i]["url"],
            "score": float(bm25_scores[i]),
        }
        for i in top_bm25_indices
    }

    # ── Merge both results (deduplicate by text) ────────
    merged = {**bm25_chunks, **vector_chunks}  # vector results take priority on overlap
    final_chunks = list(merged.values())[:k]

    return final_chunks

def rerank_chunks(query, chunks, top_n=3):
    """Re-rank chunks using Cohere for better precision"""
    cohere_key = os.getenv("COHERE_API_KEY") or st.secrets.get("COHERE_API_KEY")
    co = cohere.Client(cohere_key)

    documents = [c["text"] for c in chunks]

    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=top_n,
    )

    reranked = []
    for r in response.results:
        chunk = chunks[r.index]
        chunk["rerank_score"] = r.relevance_score
        reranked.append(chunk)

    return reranked

if __name__ == "__main__":
    query = "How does backpropagation work?"
    print(f"\nQuery: {query}\n")

    chunks = retrieve_chunks(query, k=5)
    print("Before re-ranking:")
    for i, c in enumerate(chunks):
        print(f"  [{i+1}] {c['title']} | {c['text'][:100]}...")

    reranked = rerank_chunks(query, chunks, top_n=3)
    print("\nAfter re-ranking (top 3):")
    for i, c in enumerate(reranked):
        print(f"  [{i+1}] {c['title']} | score: {c['rerank_score']:.3f} | {c['text'][:100]}...")
