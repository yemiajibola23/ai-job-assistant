import sqlite3
import pytest
from backend.dashboard import get_dashboard_data, get_application_count, get_application_count_grouped_by_status
from backend.enums.application_status import ApplicationStatus
from backend.db.schema import create_applications_table

def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(create_applications_table)


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

def test_get_dashboard_data_returns_summary(test_db):
    cursor = test_db.cursor()

    apps = [
        ("iOS Engineer", "Apple", "Applied", "2024-01-01T10:00:00"),
        ("Backend Engineer", "Google", "Applied", "2024-01-03T11:00:00"),
        ("Data Scientist", "Meta", "Interviewing", "2024-01-02T10:21:00"),
    ]

    for title, company, status, created_at in apps:
        cursor.execute("""
                        INSERT INTO applications (job_title, company_name, status, created_at)
                        VALUES (?, ?, ?, ?)
                       """, (title, company, status, created_at)
                       )
        test_db.commit()
        
    result = get_dashboard_data(test_db)
    
    assert result["total_count"] == 3
    assert result["status_count"] == { ApplicationStatus.APPLIED : 2, ApplicationStatus.INTERVIEW: 1 }
    assert result["recent_apps"][0]["company_name"] == "Google"
    assert result["recent_apps"][-1]["company_name"] == "Apple"


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


# def test_get_dashboard_data_returns_correct_status_counts(test_db):
    
#     cursor = test_db.cursor()

#     apps = [
#         ("iOS Engineer", "Apple", "Applied"),
#         ("Backend Engineer", "Google", "Applied"),
#         ("Data Scientist", "Meta", "Interviewing"),
#     ]

#     for title, company, status in apps:
#         cursor.execute("""
#                         INSERT INTO applications (job_title, company_name, status, created_at, updated_at)
#                         VALUES (?, ?, ?, datetime('now'), datetime('now'))
#                        """, (title, company, status)
#                        )
#         test_db.commit()

#         result = get_application_count_grouped_by_status(test_db)

#         assert result == {
#             "Applied": 2,
#             "Interviewing": 1
#         }

