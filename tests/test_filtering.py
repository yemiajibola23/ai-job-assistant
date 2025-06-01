import numpy as np
from backend.matcher.filtering import filter_jobs

def test_filter_jobs():
    # Dummy resume embedding (normalized)
    resume_embedding = np.array([1.0, 0.0])

    # Dummy job embeddings
    jobs = [
        {"title": "Data Scientist", "embedding": np.array([0.9, 0.1])},
        {"title": "Backend Engineer", "embedding": np.array([0.2, 0.8])},
        {"title": "ML Engineer", "embedding": np.array([1.0, 0.0])},
    ]

    # Run filter
    top_jobs = filter_jobs(jobs, resume_embedding, top_n=2)

    # ✅ Test 1: Output length
    assert len(top_jobs) == 2

    # ✅ Test 2: Top result is the most similar one
    assert top_jobs[0]["title"] == "ML Engineer"
    assert top_jobs[0]["score"] > top_jobs[1]["score"]

    print("✅ test_filter_jobs passed!")

if __name__ == "__main__":
    test_filter_jobs()
