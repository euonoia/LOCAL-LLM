import pickle
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import MODEL_NAME, CACHE_PATH

class EuonoiaEngine:
    def __init__(self):
        # Initialize model once
        self.model = SentenceTransformer(MODEL_NAME, device="cpu")
        self.index = None
        self.chunks = []
        self.metadata = []

    def build_index(self, chunks, metadata):
        print(f"Encoding {len(chunks)} chunks into vector space...")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)
        
        # Save cache for faster loading next time
        with open(CACHE_PATH, "wb") as f:
            pickle.dump({"chunks": chunks, "embeddings": embeddings, "metadata": metadata}, f)
        
        self._initialize_faiss(embeddings, chunks, metadata)

    def load_existing_cache(self):
        if os.path.exists(CACHE_PATH):
            print("Loading memory from cache...")
            with open(CACHE_PATH, "rb") as f:
                data = pickle.load(f)
                self._initialize_faiss(data["embeddings"], data["chunks"], data["metadata"])
            return True
        return False

    def _initialize_faiss(self, embeddings, chunks, metadata):
        self.chunks = chunks
        self.metadata = metadata
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(self, query, top_k=2):
        query_embedding = self.model.encode([query]).astype("float32")
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "source": self.metadata[idx],
                "score": distances[0][i],
                "text": self.chunks[idx]
            })
        return results