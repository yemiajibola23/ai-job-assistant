import numpy as np
from backend.ranking.scoring import filter_jobs, match_resume_to_jobs

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

resume_text = """
Senior iOS Developer with 6+ years of experience building Swift and SwiftUI apps. 
Led modularization and performance work in the NBA app. 
Proficient in async/await, clean architecture, and team collaboration.
"""
job_descriptions = [
    "Machine Learning Engineer for NLP and image models using PyTorch and Transformers.",
    "iOS Engineer for a live sports streaming app, using Swift and SwiftUI in a team of mobile developers.",
    "Backend Developer to build GraphQL APIs for a fintech platform using Node.js and PostgreSQL."
]

def test_resume_matching():
    matches = match_resume_to_jobs(resume_text, job_descriptions, top_k=3)

    print("\n🔍 Top Resume Matches:")
    for idx, (job, score) in enumerate(matches, 1):
        print(f"{idx}. Score: {score:.2f} | Job: {job[:80]}...")
    

if __name__ == "__main__":
    test_resume_matching()

if __name__ == "__main__":
    test_filter_jobs()
