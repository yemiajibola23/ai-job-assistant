import sqlite3
import os
from backend.db.tracker import create_table, add_application, get_all_applications, get_applications_by_status
from backend.db import tracker
from backend.enums.application_status import ApplicationStatus
import pytest

TEST_DB_PATH = "test-application.db"
tracker.DEFAULT_DB_PATH = TEST_DB_PATH

def reset_test_db():    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    create_table()


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

def test_create_table_structure():
    create_table()

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    sql = "PRAGMA table_info(applications)"
    cursor.execute(sql)
    columns = cursor.fetchall()

    column_names = [col[1] for col in columns]

    expected_columns = [
    'id',
    'job_title',
    'company_name',
    'location',
    'job_url',
    'match_score',
    'resume_used',
    'cover_letter_used',
    'status',
    'notes',
    'created_at',
    'updated_at'
    ]

    assert column_names == expected_columns

    conn.close()

def test_add_application_inserts_data():
    data = get_test_application(status=ApplicationStatus.INTERVIEW)
    app_id = add_application(data)
    assert isinstance(app_id, int) and app_id > 0

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    
    assert cursor.fetchone()[1] == 'Senior iOS Engineer'

    conn.close()

def test_get_all_applications_returns_data():
    data = get_test_application(status=ApplicationStatus.INTERVIEW)
    
    app_id = add_application(data)

    apps = get_all_applications()
    
    assert isinstance(apps, list) and len(apps) > 0 
    assert apps[-1]["job_title"] == "Senior iOS Engineer"

    # Optional: delete test data to avoid build-up
    # delete_application(app_id)

def test_get_all_applications_by_status_filters_correctly():
    # Should return only applications with matching status
    applied_job = get_test_application()

    interviewing_job = get_test_application(ApplicationStatus.INTERVIEW, "Machine Learning Engineer")
    
    interviewing_id = add_application(interviewing_job)
    applied_id = add_application(applied_job)

    res_application = get_applications_by_status(ApplicationStatus.APPLIED)

    assert isinstance(res_application, list)
    assert len(res_application) == 1
    assert res_application[0]["job_title"] == "Senior iOS Engineer"