# schema.py

def init_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company_name TEXT,
            location TEXT,
            job_url TEXT,
            status TEXT DEFAULT 'interested',
            tailored_resume_path TEXT,
            tailored_resume_created_at TEXT DEFAULT (datetime('now'))
        )
    """)
