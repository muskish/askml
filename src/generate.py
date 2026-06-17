import os
from groq import Groq
from src.retrieve import retrieve_chunks, rerank_chunks

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Works both locally (.env) and on cloud (st.secrets)
groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=groq_key)

MODEL = "llama-3.1-8b-instant"

def build_prompt(query, chunks):
    """Build a prompt that forces citation-grounded answers"""
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[{i+1}] (Source: {chunk['title']})\n{chunk['text']}\n\n"

    prompt = f"""You are a helpful AI assistant that answers questions about AI and ML.
Answer the question using ONLY the context provided below.
For every claim you make, cite the source using [1], [2], etc.
If the context does not contain enough information, say "I don't have enough information to answer this confidently."

CONTEXT:
{context}

QUESTION: {query}

ANSWER (with citations):"""
    return prompt

def answer_question(query):
    """Full pipeline: retrieve → re-rank → generate answer"""
    print(f"\n🔍 Retrieving and re-ranking chunks...")
    chunks = retrieve_chunks(query, k=8)
    chunks = rerank_chunks(query, chunks, top_n=3)

    print(f"✅ Using top {len(chunks)} re-ranked chunks from: {set(c['title'] for c in chunks)}")
    print(f"⏳ Generating answer...\n")

    prompt = build_prompt(query, chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    # Build sources list
    sources = []
    seen = set()
    for i, chunk in enumerate(chunks):
        if chunk["title"] not in seen:
            sources.append(f"[{i+1}] {chunk['title']} — {chunk['url']}")
            seen.add(chunk["title"])

    return answer, sources

if __name__ == "__main__":
    query = "How does backpropagation work?"
    answer, sources = answer_question(query)
    print("ANSWER:")
    print(answer)
    print("\nSOURCES:")
    for s in sources:
        print(s)