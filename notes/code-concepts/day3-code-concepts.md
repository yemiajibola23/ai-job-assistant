# 🧠 Code Concepts – Day 3

### 1. Cosine Similarity
- Measures the directional similarity between two vectors, ignoring magnitude.
- Used for comparing embeddings like resumes and job descriptions.

### 2. np.vstack()
- Combines a list of 1D vectors into a single 2D array for batch similarity comparisons.

### 3. INSERT OR IGNORE (SQLite)
- Allows safe insertion without throwing errors when primary keys already exist.
- Used to prevent duplicate job entries based on ID.

### 4. PyTorch Tensor Detection
- Use `isinstance(obj, torch.Tensor)` instead of `hasattr(obj, "detach")` for safety and clarity.

### 5. Pytest + Path Configuration
- `pytest.ini` with `pythonpath = .` ensures root-relative imports work in test files.
