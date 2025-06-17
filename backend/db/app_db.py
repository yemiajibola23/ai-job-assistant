import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent / "applications.db"

def get_connection():
    return sqlite3.connect(DEFAULT_DB_PATH)

def get_dict_cursor():
    conn =  get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    return conn, cursor