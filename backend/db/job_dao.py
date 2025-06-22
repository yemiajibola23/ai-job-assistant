import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from backend.db.schema import insert_job_sql

def save_jobs_to_db(conn: sqlite3.Connection, jobs: List[Dict[str, Any]]) -> int:
    """
    Saves a list of job dicts into the SQLite database.

    Args:
        jobs: List of job dicts (each must contain id, title, etc.)
    """
    cursor = conn.cursor()
    try:
        saved_jobs = 0

        for job in jobs:
            print(f"📝 Saving job: {job['id']} – {job.get('title')}")
            row_count = cursor.execute(insert_job_sql, (
                job["id"],
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("url"),
                job.get("description"),
                job.get("score"),
            )).rowcount

            saved_jobs += row_count
        conn.commit()
        print(f"✅ Committed {saved_jobs} new jobs to DB")
        return saved_jobs
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"❌ Failed to save jobs to DB: {e}")



def has_seen_job(conn: sqlite3.Connection, job_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seen_jobs WHERE job_id = ?", (job_id,))

    return cursor.fetchone() is not None

def mark_job_as_seen(conn: sqlite3.Connection, job_id: str):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)", (job_id, ))
    conn.commit()

    return cursor.rowcount > 0
