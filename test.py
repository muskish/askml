from src.retrieve import retrieve_chunks

chunks = retrieve_chunks('LSTM gates forget cell state', k=5)
for i, c in enumerate(chunks):
    print(f'[{i+1}] {c["title"]} | score: {c["score"]:.3f}')