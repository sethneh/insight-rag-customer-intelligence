# InsightRAG: AI Customer Intelligence System

## Overview

InsightRAG is an AI-powered **Customer Intelligence Engine** built using Retrieval-Augmented Generation (RAG). It analyzes product reviews, ratings, and customer feedback to generate actionable business insights.

It allows users to ask natural language questions like:
- "What are customers complaining about?"
- "Show me bad products"
- "Which products have high satisfaction?"

---
## Problem Statement
Businesses receive thousands of customer reviews daily, but:

- ❌ Data is unstructured (text-heavy reviews)
- ❌ Hard to identify trends manually
- ❌ No easy way to extract insights at scale
- ❌ Sentiment is hidden inside text

### InsightRAG solves this by:
- Converting reviews into searchable embeddings
- Enabling semantic search over customer feedback
- Adding structured filters (rating-based analysis)
- Generating AI-powered insights with citations

---
##  Key Features

### 1. RAG-based Search
Uses FAISS vector database to retrieve semantically similar reviews.

### 2. Structured Filtering
Supports filters like:
- Minimum rating
- Maximum rating
- Sentiment-based grouping

### 3. Query Understanding Layer
Converts natural language into structured filters.

Example:
> "show me bad products"
→ converts to:
- rating ≤ 2
- negative sentiment query

### 4. Multi-turn Chat UI
Supports conversation history like ChatGPT.

### 5. Citation-based Answers
Every response is grounded in real review data.

---
## System Architecture
User Query
↓
Query Parser (intent detection)
↓
Embedding Model
↓
FAISS Vector Search
↓
Filtered Results (rating-based)
↓
LLM (Groq/OpenAI)
↓
Final Answer + Citations

---
## Tech Stack
- Python
- Streamlit (UI)
- FAISS (Vector Search)
- OpenAI / Groq (LLM)
- SentenceTransformers (Embeddings)
- Pandas (Data Processing)

---
## Key Concepts Explained

### Top-K Retrieval
Top-K defines how many closest documents are retrieved from the vector database.
- Higher K → more context (better recall)
- Lower K → more precise but limited context

---
### Similarity Score (FAISS Distance)
Measures how close a document is to the query in embedding space.
- Lower score = better match
- Used to rank results

---
### Minimum Rating Filter
Filters reviews based on product rating before or after retrieval.
Example:
- min_rating = 4 → only positive reviews
- min_rating = 1 → all reviews

This allows structured filtering on top of semantic search.

---
### Query Understanding Layer
Transforms natural language into structured filters.
Example:
"bad products"
→ min_rating ≤ 2
→ negative sentiment query



This improves:
- precision
- user experience
- business usability

---
## Business Value
- Understand customer sentiment at scale
- Identify product issues quickly
- Improve product decisions
- Reduce manual analysis effort

---
## Example Use Cases
- E-commerce product analysis
- SaaS customer feedback intelligence
- App review analysis
- Product quality monitoring

---
## Future Improvements
- Hybrid search (BM25 + FAISS)
- Real-time data ingestion (Reddit / APIs)
- Sentiment classification model
- Dashboard analytics view
- Automated executive reports

---
## Author
Built as a portfolio project to demonstrate:
- RAG systems
- LLM integration
- Data engineering
- Product intelligence systems