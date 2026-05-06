import streamlit as st
from rag_engine import RAGEngine
from query_parser import parse_query

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="InsightRAG",
    layout="wide"
)

st.title("🧠 InsightRAG: Customer Intelligence Engine")
st.markdown("Ask questions about customer reviews, ratings, and product feedback.")

# -------------------------
# ENGINE (CACHE)
# -------------------------
@st.cache_resource
def load_engine():
    return RAGEngine()

engine = load_engine()

# -------------------------
# SESSION STATE (CHAT MEMORY)
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# SIDEBAR CONTROLS
# -------------------------
st.sidebar.header("⚙️ Retrieval Controls")

top_k = st.sidebar.slider("Top-K (Recall Control)", 1, 10, 5)
threshold = st.sidebar.slider("Similarity Threshold (Precision Control)", 0.0, 2.0, 1.0)
min_rating = st.sidebar.slider("Min Rating Filter", 1, 5, 1)

st.sidebar.markdown("---")
st.sidebar.info("""
📌 How it works:
- Lower threshold → higher precision
- Higher Top-K → higher recall
- Rating filter → structured filtering
""")

# -------------------------
# INPUT SECTION
# -------------------------
query = st.text_input(
    "💬 Ask a question",
    placeholder="e.g. What are common complaints about products with low ratings?"
)

col1, col2 = st.columns([1, 4])

with col1:
    run = st.button("🚀 Run RAG")

# -------------------------
# PROCESS QUERY
# -------------------------
if run and query.strip():

    parsed = parse_query(query)

    with st.spinner("🔍 Understanding query + retrieving insights..."):

        docs = engine.retrieve(
            parsed["clean_query"],
            top_k=top_k,
            threshold=threshold,
            min_rating=parsed["min_rating"]
        )

        answer = engine.generate(query, docs)

    st.session_state.chat_history.append({
        "query": query,
        "answer": answer,
        "docs": docs,
        "parsed": parsed
    })

# -------------------------
# DISPLAY CURRENT RESULT
# -------------------------
if st.session_state.chat_history:

    latest = st.session_state.chat_history[-1]

    st.markdown("---")

    st.subheader("🧠 AI Insights")

    st.write(latest["answer"])

    st.subheader("📚 Retrieved Evidence")

    for i, d in enumerate(latest["docs"]):
        st.markdown(f"""
        **Source {i+1} (ID: {d['id']})**
        - Score: `{d['score']:.4f}`
        - Text: {d['text'][:300]}...
        """)

    st.subheader("📊 Retrieval Metrics")

    st.metric("Documents Retrieved", len(latest["docs"]))

    avg_score = sum(d["score"] for d in latest["docs"]) / max(len(latest["docs"]), 1)
    st.metric("Avg Similarity Score", round(avg_score, 4))

# -------------------------
# CHAT HISTORY (MULTI-TURN UI)
# -------------------------
st.markdown("---")
st.subheader("💬 Conversation History")

for i, chat in enumerate(reversed(st.session_state.chat_history)):

    with st.expander(f"Q{len(st.session_state.chat_history)-i}: {chat['query']}"):

        st.markdown("### 🧠 Answer")
        st.write(chat["answer"])

        st.markdown("### 📚 Sources")
        for j, d in enumerate(chat["docs"]):
            st.write(f"Source {j+1}: {d['text'][:200]}...")