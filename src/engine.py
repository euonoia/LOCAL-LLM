import pickle
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import MODEL_NAME, CACHE_PATH

class EuonoiaEngine:
    def __init__(self):
        # Load embedding model once (Use 'cuda' if you have an NVIDIA GPU)
        self.model = SentenceTransformer(MODEL_NAME, device="cpu")
        self.index = None
        self.chunks = []
        self.metadata = []

    # --------------------------------------------------
    # BUILD INDEX
    # --------------------------------------------------
    def build_index(self, chunks, metadata):
        """Encodes text chunks and saves them to a FAISS index and local cache."""
        if not chunks:
            print("No chunks provided to build index.")
            return

        print(f"Encoding {len(chunks)} chunks into vector space...")

        # Convert text to numerical vectors
        embeddings = self.model.encode(
            chunks,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        embeddings = np.array(embeddings).astype("float32")

        # Save data to disk so we don't have to re-encode every time
        with open(CACHE_PATH, "wb") as f:
            pickle.dump({
                "chunks": chunks,
                "embeddings": embeddings,
                "metadata": metadata
            }, f)

        self._initialize_faiss(embeddings, chunks, metadata)

    # --------------------------------------------------
    # LOAD CACHE
    # --------------------------------------------------
    def load_existing_cache(self):
        """Attempts to load the pre-computed embeddings from the pickle file."""
        if os.path.exists(CACHE_PATH):
            print("Loading memory from cache...")
            try:
                with open(CACHE_PATH, "rb") as f:
                    data = pickle.load(f)

                self._initialize_faiss(
                    data["embeddings"],
                    data["chunks"],
                    data["metadata"]
                )
                return True
            except (pickle.UnpicklingError, KeyError) as e:
                print(f"Cache corrupted: {e}. Rebuilding required.")
                return False

        return False

    # --------------------------------------------------
    # FAISS INITIALIZATION
    # --------------------------------------------------
    def _initialize_faiss(self, embeddings, chunks, metadata):
        """Sets up the FAISS index for high-speed similarity search."""
        self.chunks = chunks
        self.metadata = metadata

        dimension = embeddings.shape[1]

        # Using Inner Product (IndexFlatIP) for Cosine Similarity 
        # because our embeddings are normalized.
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    # --------------------------------------------------
    # CORE SEARCH (Optimized for RAG)
    # --------------------------------------------------
    def search(self, query, top_k=5):
        """
        Main search function. 
        Returns top_k results after semantic search AND re-ranking.
        """
        if self.index is None:
            return []

        # 1. Encode the user query
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        # 2. Vector Search (Semantic)
        distances, indices = self.index.search(query_embedding, top_k * 2) # Grab extra for reranking

        candidates = []
        for i, idx in enumerate(indices[0]):
            if idx == -1: continue # FAISS returns -1 if not enough matches found
            candidates.append({
                "source": self.metadata[idx],
                "score": float(distances[0][i]),
                "text": self.chunks[idx]
            })

        # 3. Hybrid Re-Ranking (Keyword & Logic check)
        ranked_results = self._rerank(query, candidates)

        # Return only the requested top_k
        return ranked_results[:top_k]

    # --------------------------------------------------
    # HYBRID RE-RANKING
    # --------------------------------------------------
    def _rerank(self, query, results):
        """
        Senior Logic: Combines semantic score with keyword overlap 
        to ensure technical terms are prioritized.
        """
        query_words = set(query.lower().split())
        ranked = []

        for r in results:
            text_lower = r["text"].lower()

    
            overlap = sum(word in text_lower for word in query_words if len(word) > 2)

            # Length penalty (prevents the AI from getting 'lost' in huge chunks)
            length_penalty = len(r["text"]) / 1000

            # Final Score Calculation
            # We give high weight to the vector score, but adjust based on keywords
            final_score = r["score"] + (overlap * 0.05) - (length_penalty * 0.02)

            ranked.append((final_score, r))

        # Sort by the new custom score
        ranked.sort(key=lambda x: x[0], reverse=True)

        return [r[1] for r in ranked]

    # --------------------------------------------------
    # BEST SINGLE MATCH
    # --------------------------------------------------
    def search_best(self, query):
        """Convenience method for when you only want the #1 result."""
        results = self.search(query, top_k=1)
        
        if not results:
            return None
            
        # Threshold check: If the match is weak, return None to avoid nonsense
        if results[0]["score"] < 0.40:
            return None

        return results[0]