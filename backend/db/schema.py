# schema.py
import sqlite3

create_applications_table ="""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        company_name TEXT,
        location TEXT,
        job_url TEXT,
        match_score REAL,
        resume_used TEXT,
        cover_letter_used TEXT,
        status TEXT DEFAULT 'Applied',
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now')),
        synced_at TEXT DEFAULT NULL
    )
    """

# ✅ New table for tracking seen jobs
create_seen_jobs_table = """
CREATE TABLE IF NOT EXISTS seen_jobs (
    job_id TEXT PRIMARY KEY,
    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_jobs_table = """
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

insert_job_sql = """
    INSERT OR IGNORE INTO jobs (
        id, title, company, location, url, description, score
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """


def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()

    # Check if any table exists that matches schema
    for table_name, schema_sql in [
        ("jobs", create_jobs_table),
        ("seen_jobs", create_seen_jobs_table),
        ("applications", create_applications_table),
    ]:
    

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"🛠️ Creating table '{table_name}'...")
            cursor.execute(schema_sql)
            conn.commit()
        else:
            print(f"✅ Table '{table_name}' already exists.")


    conn.commit()