import sqlite3
from backend.db.application_dao import add_application, get_all_applications, get_applications_by_status, get_application_by_id, get_application_by_id, update_application_status_and_notes, delete_application
from datetime import datetime
import time
from typing import Optional
from backend.enums.application_status import ApplicationStatus
import os
import pytest
from backend.db.schema import create_applications_table

TEST_DB_PATH = "test-job-assistant.db"

def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(create_applications_table)

def reset_test_db():    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    create_table(conn)


@pytest.fixture(autouse=True)
def reset_db_before_each_test():
    reset_test_db()

def get_test_application(status=ApplicationStatus.APPLIED, job_title="Senior iOS Engineer"):
    return {
        "job_title": job_title, 
        "company_name": "Flock Safety", 
        "location": "Remote", 
        "job_url": "https://www.flocksafety.com/careers?ashby_jid=7810dce1-c1bf-4f28-b5d9-800c5a7e1289#ashby_embed", 
        "match_score":0.7, 
        "resume_used": "yemi_ajibola.pdf", 
        "cover_letter_used": "yemi_ajibola_cover_letter.pdf", 
        "status": status, 
        "notes":""
    }

def test_add_application_inserts_data():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    data = get_test_application(status=ApplicationStatus.INTERVIEW)
    app_id = add_application(conn,data)
    assert isinstance(app_id, int) and app_id > 0
    
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    
    assert cursor.fetchone()[1] == 'Senior iOS Engineer'

    conn.close()

def test_get_all_applications_returns_data():
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    
    data = get_test_application(status=ApplicationStatus.INTERVIEW)
    
    app_id = add_application(conn, data)

    apps = get_all_applications(conn)
    
    assert isinstance(apps, list) and len(apps) > 0 
    assert apps[-1]["job_title"] == "Senior iOS Engineer"

    # Optional: delete test data to avoid build-up
    # delete_application(app_id)
    conn.close()

def test_get_all_applications_by_status_filters_correctly():
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row

    # Should return only applications with matching status
    applied_job = get_test_application()

    interviewing_job = get_test_application(ApplicationStatus.INTERVIEW, "Machine Learning Engineer")
    
    interviewing_id = add_application(conn, interviewing_job)
    applied_id = add_application(conn, applied_job)

    res_application = get_applications_by_status(conn, ApplicationStatus.APPLIED)

    assert isinstance(res_application, list)
    assert len(res_application) == 1
    assert res_application[0]["job_title"] == "Senior iOS Engineer"

    conn.close()

def test_delete_application_deletes_correct_application():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    applied_job = get_test_application()
    id = add_application(conn, applied_job)

    delete_application(conn, id)

    apps = get_all_applications(conn)
    assert all(app['id'] != id for app in apps)  

    conn.close()

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