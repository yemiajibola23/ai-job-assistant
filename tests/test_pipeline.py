import os
import sqlite3
import numpy as np
from backend.matcher.filtering import filter_jobs
from backend.db.db import init_db, save_jobs_to_db

DB_PATH = "test_jobs.db"

def setup_module(module):
    """Setup test DB and ensure clean state."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db(DB_PATH)

def test_filter_and_store_pipeline():
    resume_embedding = np.array([1.0, 0.0])

    jobs = [
        {
            "id": "job1",
            "title": "Data Scientist",
            "company": "Company A",
            "location": "Remote",
            "url": "https://example.com/job1",
            "description": "Do data things",
            "embedding": np.array([0.9, 0.1]),
        },
        {
            "id": "job2",
            "title": "Backend Engineer",
            "company": "Company B",
            "location": "Remote",
            "url": "https://example.com/job2",
            "description": "Build APIs",
            "embedding": np.array([0.1, 0.9]),
        },
        {
            "id": "job3",
            "title": "ML Engineer",
            "company": "Company C",
            "location": "NYC",
            "url": "https://example.com/job3",
            "description": "Train models",
            "embedding": np.array([1.0, 0.0]),
        },
    ]

    # Filter top 2 jobs
    top_jobs = filter_jobs(jobs, resume_embedding, top_n=2)
    assert len(top_jobs) == 2
    assert top_jobs[0]["id"] == "job3"  # Highest match

    # Save to test DB
    save_jobs_to_db(top_jobs, db_path=DB_PATH)

    # Verify in DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, score FROM jobs")
    results = cursor.fetchall()
    conn.close()

    assert len(results) == 2
    ids = [row[0] for row in results]
    assert "job3" in ids
    assert "job1" in ids
