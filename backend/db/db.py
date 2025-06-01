import sqlite3
from typing import List, Dict
def init_db(db_path: str = "jobs.db"):
    """
    Initializes the job database and creates the jobs table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Write your CREATE TABLE statement here
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT,
        location TEXT,
        url TEXT,
        description TEXT, 
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def save_jobs_to_db(jobs: List[Dict], db_path: str = "jobs.db"):
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
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ DB initialized and 'jobs' table ensured.")