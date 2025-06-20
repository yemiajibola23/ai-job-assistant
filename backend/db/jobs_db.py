import sqlite3
from typing import List, Dict, Any
from pathlib import Path
from backend.db.schema import create_jobs_table
DB_PATH = Path(__file__).parent / "jobs.db"

def init_db(db_path: Path):
    """
    Initializes the job database and creates the jobs table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(create_jobs_table)
    conn.commit()
    conn.close()

def save_jobs_to_db(jobs: List[Dict[str, Any]], db_path: Path = DB_PATH):
    """
    Saves a list of job dicts into the SQLite database.

    Args:
        jobs: List of job dicts (each must contain id, title, etc.)
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_sql = """
    INSERT OR IGNORE INTO jobs (
        id, title, company, location, url, description, score
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    for job in jobs:
        print(f"📝 Saving job: {job['id']} – {job.get('title')}")
        cursor.execute(insert_sql, (
            job["id"],
            job.get("title"),
            job.get("company"),
            job.get("location"),
            job.get("url"),
            job.get("description"),
            job.get("score"),
        ))

    conn.commit()
    print(f"✅ Committed {len(jobs)} jobs to DB")
    conn.close()

if __name__ == "__main__":
    init_db(DB_PATH)
    print("✅ DB initialized and 'jobs' table ensured.")