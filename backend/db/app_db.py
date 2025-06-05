import sqlite3

DEFAULT_DB_PATH = "applications.db"

def get_connection():
    return sqlite3.connect(DEFAULT_DB_PATH)

def get_dict_cursor():
    conn =  get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    return conn, cursor