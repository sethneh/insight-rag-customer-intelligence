from data_loader import load_data
from embedder import get_embedding
from vector_store import VectorStore
from chunker import chunk_text
from tqdm import tqdm

def build():

    texts = load_data()

    all_chunks = []
    embeddings = []

    print("Chunking + embedding...")

    for t in tqdm(texts):
        chunks = chunk_text(t)

        for c in chunks:
            all_chunks.append(c)
            emb = get_embedding(c)
            embeddings.append(emb)

    dim = len(embeddings[0])

    store = VectorStore(dim)
    store.add(embeddings, all_chunks)

    store.save()

    print("✅ Index built and saved!")

if __name__ == "__main__":
    build()