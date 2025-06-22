import sqlite3
from pathlib import Path

from backend.db.schema import (
    create_jobs_table,
    create_seen_jobs_table,
    create_applications_table
)


BASE_DIR = Path(__file__).parent
DB_PATH  = BASE_DIR / "job_assistant.db"

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_dict_cursor():
    conn =  get_connection()
    cursor = conn.cursor()

    return conn, cursor

def _init_db(path: Path=DB_PATH):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Check if any table exists that matches schema
    for table_name in ["jobs", "seen_jobs", "applications"]:
        schema_sql = ""
        if table_name == "jobs":
            schema_sql = create_jobs_table
        elif table_name == "seen_jobs":
            schema_sql = create_seen_jobs_table
        else:
            schema_sql = create_applications_table
    

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"🛠️ Creating table '{table_name}' in {path.name}...")
            cursor.execute(schema_sql)
            conn.commit()
        else:
            print(f"✅ Table '{table_name}' already exists in {path.name}")

   

    conn.close()
