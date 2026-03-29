import pickle
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import MODEL_NAME, CACHE_PATH


class EuonoiaEngine:
    def __init__(self):
        # Load embedding model once
        self.model = SentenceTransformer(MODEL_NAME, device="cpu")
        self.index = None
        self.chunks = []
        self.metadata = []

    # --------------------------------------------------
    # BUILD INDEX
    # --------------------------------------------------
    def build_index(self, chunks, metadata):
        print(f"Encoding {len(chunks)} chunks into vector space...")

        embeddings = self.model.encode(
            chunks,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        embeddings = np.array(embeddings).astype("float32")

        # Save cache
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
        if os.path.exists(CACHE_PATH):
            print("Loading memory from cache...")

            with open(CACHE_PATH, "rb") as f:
                data = pickle.load(f)

            self._initialize_faiss(
                data["embeddings"],
                data["chunks"],
                data["metadata"]
            )
            return True

        return False

    # --------------------------------------------------
    # FAISS INITIALIZATION
    # --------------------------------------------------
    def _initialize_faiss(self, embeddings, chunks, metadata):
        self.chunks = chunks
        self.metadata = metadata

        dimension = embeddings.shape[1]

        # Cosine similarity (using normalized vectors)
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    # --------------------------------------------------
    # BASIC SEARCH (returns multiple results)
    # --------------------------------------------------
    def search(self, query, top_k=8):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for i, idx in enumerate(indices[0]):
            results.append({
                "source": self.metadata[idx],
                "score": float(distances[0][i]),
                "text": self.chunks[idx]
            })

        return results

    # --------------------------------------------------
    # HYBRID RE-RANKING
    # --------------------------------------------------
    def _rerank(self, query, results):
        """
        Improves accuracy using:
        - semantic similarity
        - keyword overlap
        - chunk precision (shorter = usually better)
        """

        query_words = set(query.lower().split())
        ranked = []

        for r in results:
            text = r["text"].lower()

            # keyword overlap bonus
            overlap = sum(word in text for word in query_words)

            # length penalty (long chunks are often noisy)
            length_penalty = len(text) / 600

            final_score = r["score"] + (overlap * 0.02) - (length_penalty * 0.01)

            ranked.append((final_score, r))

        ranked.sort(key=lambda x: x[0], reverse=True)

        return [r[1] for r in ranked]

    # --------------------------------------------------
    # BEST ANSWER SEARCH (main function you should use)
    # --------------------------------------------------
    def search_best(self, query):
        """
        Returns only the most relevant answer.
        If confidence is low, returns None.
        """

        candidates = self.search(query, top_k=8)
        ranked = self._rerank(query, candidates)

        if not ranked:
            return None

        best = ranked[0]

        # confidence threshold (prevents hallucination-style answers)
        if best["score"] < 0.45:
            return None

        return best