import sqlite3
from pathlib import Path

from backend.db.schema import (
    create_jobs_table,
    create_seen_jobs_table,
    create_applications_table
)


BASE_DIR = Path(__file__).parent
DB_PATH  = BASE_DIR / "job_assistant.db"

def get_connection(path: str | Path=DB_PATH):
    if isinstance(path, Path):
        path = str(path)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def get_dict_cursor():
    conn =  get_connection()
    cursor = conn.cursor()

    return conn, cursor
