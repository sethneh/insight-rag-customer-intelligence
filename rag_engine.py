from groq import Groq
from embedder import get_embedding
from vector_store import VectorStore

client = Groq()

class RAGEngine:
    def __init__(self):
        self.store = VectorStore(384)
        self.store.load()
    
    def filter_by_rating(self, data, min_rating=None, max_rating=None):
        if min_rating is None and max_rating is None:
            return data

        filtered = []

        for d in data:
            text = d["text"]

            # extract rating from structured text
            if "Rating:" in text:
                try:
                    rating_line = [line for line in text.split("\n") if "Rating:" in line][0]
                    rating = float(rating_line.split(":")[1].strip())

                    if min_rating is not None and rating < min_rating:
                        continue
                    if max_rating is not None and rating > max_rating:
                        continue

                    filtered.append(d)

                except:
                    continue

        return filtered


    def retrieve(self, query, top_k=5, threshold=None, min_rating=None):

        q_emb = get_embedding(query)
        results = self.store.search(q_emb, top_k, threshold)

        # fallback if no results
        if len(results) == 0:
            return [{
                "text": "No strong matches found. Try more specific query like product name or rating.",
                "score": 999,
                "id": -1
            }]

        if min_rating is not None:
            results = self.filter_by_rating(results, min_rating)

        return results


    def generate(self, query, docs):

        if not docs:
            return "No relevant results found. Try increasing Top-K or threshold."

        context = "\n\n".join(
            [f"[Source {i+1}] {d['text']}" for i, d in enumerate(docs)]
        )

        prompt = f"""
You are a customer intelligence analyst.

Use ONLY the context below.

Context:
{context}

Question:
{query}

Return:
- Answer
- Key insights
- Cite sources like [Source X]
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content