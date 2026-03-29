from sentence_transformers import SentenceTransformer
import os
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

folder = "/mnt/HelloMaster/llm-project/documents"

def split_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# Load all chunks
all_chunks = []

# Verify path exists before running
if not os.path.exists(folder):
    print(f"Error: The path {folder} was not found. Check your mount!")
else:
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            chunks = split_text(text)
            all_chunks.extend(chunks)

    if not all_chunks:
        print("No .txt files found in the directory.")
    else:
        # Ask a question
        question = input("Ask a question: ")
        question_embedding = model.encode(question)

        # OPTIMIZATION: Encode all chunks in one batch (much faster)
        print("Encoding documents, please wait...")
        chunk_embeddings = model.encode(all_chunks)

        # Use dot product (cosine similarity if vectors are normalized)
        scores = np.dot(chunk_embeddings, question_embedding)
        best_idx = np.argmax(scores)

        print("\nMost relevant result:\n")
        print(all_chunks[best_idx])
