import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect('applications.db')

def create_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    applications_sql = """
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        company_name TEXT,
        location TEXT,
        job_url TEXT,
        match_score REAL,
        resume_used TEXT,
        cover_letter_used TEXT,
        status TEXT DEFAULT 'Interested',
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT
    )
    """

    cursor.execute(applications_sql)
    conn.commit()
    conn.close()