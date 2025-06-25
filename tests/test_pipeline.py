import os
import sqlite3
import numpy as np
from backend.ranking.scoring import filter_jobs
from backend.db.schema import init_db
from backend.db.job_dao import save_jobs_to_db
from pathlib import Path
from backend.db.connection import get_connection

DB_PATH = Path(__file__).parent / "test_job.db"

def setup_module(module):
    """Setup test DB and ensure clean state."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection(DB_PATH)    
    init_db(conn)

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
    conn = sqlite3.connect(DB_PATH)
    save_jobs_to_db(conn, top_jobs)

    # Verify in DB
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, score FROM jobs")
    results = cursor.fetchall()
    conn.close()

    assert len(results) == 2
    ids = [row[0] for row in results]
    assert "job3" in ids
    assert "job1" in ids
