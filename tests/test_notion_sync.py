from backend.db.connection import get_connection
from backend.db.schema import init_db
from backend.db.application_dao import add_application
from backend.enums.application_status import ApplicationStatus
from backend.notion.sync import sync_applications_to_notion

def set_synced_at(conn, job_url: str, synced_at: str):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE applications SET synced_at = ? WHERE job_url = ?",
        (synced_at, job_url)
    )
    conn.commit()

def test_sync_only_interview_applications(monkeypatch):
    synced_jobs = []
    def mock_push_to_notion(jobs:list[dict])  -> dict:
        for job in jobs:
            synced_jobs.append(job["job_url"])
        return {}

    # 1. Get a test DB connection
    conn = get_connection(":memory:")
    init_db(conn)
    # 2. Insert 4 jobs:
    #    - A: Interview, not synced yet → should be pushed
    jobA = {
    "job_title": "Test Job A",
    "company_name": "A Inc",
    "location": "Remote",
    "job_url": "https://job.a",
    "status": ApplicationStatus.INTERVIEW
    }
    add_application(conn, jobA)

    jobB = {
    "job_title": "Test Job B",
    "company_name": "B Inc",
    "location": "Seattle, WA",
    "job_url": "https://job.b",
    "status": ApplicationStatus.INTERVIEW,
    }

    add_application(conn, jobB)

    synced_yesterday = "2025-06-24T10:00:00"
    set_synced_at(conn, "https://job.b", synced_yesterday)


    jobC = {
    "job_title": "Test Job C",
    "company_name": "C Inc",
    "location": "Remote",
    "job_url": "https://job.c",
    "status": ApplicationStatus.APPLIED,
    }

    add_application(conn, jobC)

    jobD = {
    "job_title": "Test Job D",
    "company_name": "D Inc",
    "location": "Remote",
    "job_url": "https://job.d",
    "status": ApplicationStatus.INTERVIEW,
    }

    add_application(conn, jobD)
    synced_in_the_future = "2026-07-01T10:00:00"
    set_synced_at(conn, "https://job.d", synced_in_the_future)

    monkeypatch.setattr("backend.notion.sync.push_to_notion", mock_push_to_notion)
    sync_applications_to_notion(conn)

    assert "https://job.a" in synced_jobs
    assert "https://job.b" in synced_jobs
    assert "https://job.c" not in synced_jobs
    assert "https://job.d" not in synced_jobs

    cursor = conn.cursor()
    cursor.execute("SELECT synced_at from applications WHERE job_url=?", ("https://job.a",))
    row = cursor.fetchone()

    assert row is not None
    assert row["synced_at"] is not None