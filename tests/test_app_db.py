import sqlite3
from backend.db.app_db import get_application_by_id, update_application_status_and_notes
from datetime import datetime
import time
from typing import Optional

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

def test_update_application_status_and_notes_updates_updated_at_timestamp():
     # Arrange
    db = setup_test_db()
    original_time = datetime.now().isoformat()
    insert_mock_application(db, id=1, status="Interested", notes="Old notes", updated_at=original_time)

    # Act
    time.sleep(0.01)
    update_application_status_and_notes(db, 1, "Applied", "Sent application via site")

    # Assert
    updated = get_application_by_id(db, 1)
    assert updated["updated_at"] != original_time

def setup_test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY, status TEXT, notes TEXT, updated_at TEXT DEFAULT (datetime('now')))")

    return conn


def insert_mock_application(db: sqlite3.Connection, id: int, status: str, notes: str, updated_at: Optional[str] = None):
    cursor = db.cursor()
    updated_at = updated_at or datetime.now().isoformat()

    cursor.execute("INSERT INTO applications(id, status, notes, updated_at) VALUES(?,?,?,?)", [id, status, notes, updated_at])
    db.commit()