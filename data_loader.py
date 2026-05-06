import pandas as pd

def load_data(path="data/amazon_reviews.csv", max_rows=2000):
    df = pd.read_csv(path)

    required_cols = ["product_name", "rating", "review"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}. Found: {df.columns}")

    texts = []

    for _, row in df.iterrows():
        text = f"""
Product: {row['product_name']}
Rating: {row['rating']}
Review: {row['review']}
"""
        texts.append(text.strip())

    return texts[:max_rows]