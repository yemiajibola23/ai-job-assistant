import sqlite3
from backend.db.app_db import get_application_by_id, update_application_status_and_notes, get_connection

def test_update_application_status_and_notes():
    # Arrange
    db = setup_test_db()
    insert_mock_application(db, id=1, status="Interested", notes="Old notes")

    # Act
    update_application_status_and_notes(db, 1, "Applied", "Sent application via site")

    # Assert
    updated = get_application_by_id(db, 1)
    assert updated["status"] == "Applied"
    assert updated["notes"] == "Sent application via site"

def setup_test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY, status TEXT, notes TEXT)')

    return conn


def insert_mock_application(db: sqlite3.Connection, id: int, status: str, notes: str):
    cursor = db.cursor()

    cursor.execute("INSERT INTO applications(id, status, notes) VALUES(?,?,?)", [id, status, notes])
    db.commit()
    last_row_id = cursor.lastrowid
    if last_row_id is None:
        raise ValueError("Failed to insert application, no row ID returned.")    