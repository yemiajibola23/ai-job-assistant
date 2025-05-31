# 🧠 Code Concepts – Day 2

---

### 1. Sentence Embeddings
- Sentence embeddings are high-dimensional vector representations of text that capture semantic meaning.
- Generated using pre-trained models like `SentenceTransformer("all-MiniLM-L6-v2")`.

### 2. Cosine Similarity
- Measures the angle between two vectors to determine semantic similarity.
- Values range from 0 (unrelated) to 1 (identical).

### 3. `sentence-transformers`
- A Python library that wraps popular Transformer models to easily compute sentence-level embeddings.
- Useful for tasks like semantic search, clustering, and matching.

### 4. Ranking by Similarity
- Pairwise cosine similarity scores between a resume and job descriptions are sorted in descending order.
- Top matches are selected based on highest semantic similarity.

### 5. Import Path Management in Python
- When running test files directly, Python may not recognize local project folders as importable modules.
- Workaround: modify `sys.path` to include the project root using `os.path` and `sys`.

