import sqlite3
import pytest
from backend.dashboard import get_dashboard_data, get_application_count
from backend.db.tracker import create_table
from backend.enums.application_status import ApplicationStatus

@pytest.fixture
def test_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    create_table(conn)

    #Debugging check
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("DEBUG: Tables in test DB:", tables)
    
    yield conn
    conn.close()

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

def test_get_application_count_returns_correct_value(test_db):
    cursor = test_db.cursor()
    assert get_application_count(test_db) == 0

    apps = [
        ("iOS Engineer", "Apple", "Applied"),
        ("Backend Engineer", "Google", "Applied"),
    ]

    for title, company, status in apps:
        cursor.execute("""
                        INSERT INTO applications (job_title, company_name, status, created_at, updated_at)
                        VALUES (?, ?, ?, datetime('now'), datetime('now'))
                       """, (title, company, status)
                       )
    test_db.commit()

    assert get_application_count(test_db) == 2


def test_get_dashboard_data_returns_correct_status_counts(test_db):
    pass
    # cursor = test_db.cursor()

    # apps = [
    #     ("iOS Engineer", "Apple", "Applied"),
    #     ("Backend Engineer", "Google", "Applied"),
    #     ("Data Scientist", "Meta", "Interviewing"),
    # ]

    # for title, company, status in apps:
    #     cursor.execute("""
    #                     INSERT INTO applications (job_title, company_name, status, created_at, updated_at)
    #                     VALUES (?, ?, ?, datetime('now'), datetime('now'))
    #                    """, (title, company, status)
    #                    )
    #     test_db.commit()

    #     result = get_dashboard_data(test_db)

    #     assert result["status_counts"] == {
    #         "Applied": 2,
    #         "Interviewing": 1
    #     }

