import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect('applications.db')

def create_table(db_path):
    conn = get_connection()
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

def add_application(data: dict):
    conn = get_connection()
    current_time = datetime.now().isoformat()

    fields = [
        "job_title",
        "company_name",
        "location",
        "job_url",
        "match_score",
        "resume_used",
        "cover_letter_used",
        "status",
        "notes",
        "created_at",
        "updated_at"
    ]

    values = [data.get(field) for field in fields[:-2]] + [current_time, current_time]
    placeholders = ", ".join(["?"] * len(fields))

    sql = f"INSERT INTO applications({','.join(fields)}) VALUES({placeholders})"
    
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_row_id = cursor.lastrowid
    conn.close()

    return last_row_id

def get_all_applications() -> list[dict]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM applications')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return rows