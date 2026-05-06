import faiss
import numpy as np
import pickle

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

    def search(self, query_embedding, top_k=5, threshold=None):
        D, I = self.index.search(
            np.array([query_embedding]),
            top_k
        )

        results = []

        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue

            if threshold is None or score < threshold:
                results.append({
                    "text": self.texts[idx],
                    "score": float(score),
                    "id": idx
                })

        return results

    def save(self, index_path="faiss.index", meta_path="texts.pkl"):
        faiss.write_index(self.index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, index_path="faiss.index", meta_path="texts.pkl"):
        self.index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            self.texts = pickle.load(f)