import requests
import os
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ── Config ──────────────────────────────────────────────
DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # small, fast, free

def load_documents():
    """Load all .txt files from data/ folder"""
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            # Extract title and URL from first 2 lines
            lines = content.split("\n")
            title = lines[0].replace("TITLE: ", "").strip()
            url = lines[1].replace("URL: ", "").strip()
            text = "\n".join(lines[3:])  # actual content starts line 4
            docs.append({"text": text, "title": title, "url": url})
    print(f"📄 Loaded {len(docs)} documents")
    return docs

def chunk_documents(docs):
    """Split documents into overlapping chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = []
    metadatas = []

    for doc in docs:
        splits = splitter.split_text(doc["text"])
        for i, chunk in enumerate(splits):
            chunks.append(chunk)
            metadatas.append({
                "title": doc["title"],
                "url": doc["url"],
                "chunk_index": i,
            })

    print(f"✂️  Created {len(chunks)} chunks from {len(docs)} documents")
    return chunks, metadatas

def build_vectorstore(chunks, metadatas):
    """Embed chunks and store in ChromaDB"""
    print("⏳ Loading embedding model (first time may take 1-2 mins to download)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("⏳ Embedding chunks and saving to ChromaDB...")
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=VECTORSTORE_DIR,
    )

    print(f"✅ Vectorstore built and saved to /{VECTORSTORE_DIR}")
    print(f"✅ Total chunks stored: {vectorstore._collection.count()}")
    return vectorstore

if __name__ == "__main__":
    docs = load_documents()
    chunks, metadatas = chunk_documents(docs)
    build_vectorstore(chunks, metadatas)