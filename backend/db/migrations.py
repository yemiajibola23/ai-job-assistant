# migrations.py

import sqlite3
from pathlib import Path
from backend.db.schema import create_applications_table, create_jobs_table, create_seen_jobs_table
from backend.db.connection import DB_PATH

def init_schema(cursor):
    cursor.execute(create_applications_table)
    cursor.execute(create_jobs_table)
    cursor.execute(create_seen_jobs_table)

def run_migrations():
    print("📦 Running migrations...")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Initialize full schema if missing
        init_schema(cursor)

        # Run each migration idempotently
        add_tailored_resume_fields(cursor)

        conn.commit()

    print("✅ Migrations complete.")

def add_tailored_resume_fields(cursor):
    # Check if column already exists
    cursor.execute("PRAGMA table_info(applications)")
    columns = [col[1] for col in cursor.fetchall()]

    if "tailored_resume_path" not in columns:
        print("🔧 Adding 'tailored_resume_path' column...")
        cursor.execute("""
            ALTER TABLE applications ADD COLUMN tailored_resume_path TEXT
        """)

    if "tailored_resume_created_at" not in columns:
        print("🔧 Adding 'tailored_resume_created_at' column...")
        cursor.execute("""
            ALTER TABLE applications ADD COLUMN tailored_resume_created_at TEXT DEFAULT (datetime('now'))
        """)

if __name__ == "__main__":
    run_migrations()
