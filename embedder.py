from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    emb = model.encode(text)
    return np.array(emb, dtype=np.float32)