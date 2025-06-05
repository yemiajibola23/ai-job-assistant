import sqlite3


def get_application_count(db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM applications')
    row = cursor.fetchone()

    return row[0]


def get_dashboard_data(db):
    pass

    