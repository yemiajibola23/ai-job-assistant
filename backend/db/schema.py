# schema.py

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
        updated_at TEXT DEFAULT (datetime('now'))
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