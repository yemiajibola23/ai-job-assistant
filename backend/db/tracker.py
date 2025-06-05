import sqlite3
from datetime import datetime
from backend.enums.application_status import ApplicationStatus
from typing import Union, Optional
from backend.db.app_db import get_connection, get_dict_cursor

def create_table(conn: Optional[sqlite3.Connection] = None):
    should_close = False

    if conn is None:
        conn = get_connection()
        should_close = True

    cursor = conn.cursor()

    applications_sql = """
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        company_name TEXT,
        location TEXT,
        job_url TEXT,
        match_score REAL,
        resume_used TEXT,
        cover_letter_used TEXT,
        status TEXT DEFAULT 'Applied',
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
    )
    """

    cursor.execute(applications_sql)
    conn.commit()

    if should_close:
        conn.close()

def add_application(data: dict[str, Union[str, float, ApplicationStatus]]) -> int:
    conn = get_connection()
    current_time = datetime.now().isoformat()

    raw_status = data.get("status")
    if isinstance(raw_status, str):
        try:
            status = ApplicationStatus.from_value(raw_status)
        except ValueError:
            raise ValueError(f"Invalid application status: {raw_status}")
    elif isinstance(raw_status, ApplicationStatus):
        status = raw_status
    else:
        raise TypeError("status must be a string or ApplicationStatus enum")

    data["status"] = status.value  # Normalize

    fields = [
        "job_title",
        "company_name",
        "location",
        "job_url",
        "match_score",
        "resume_used",
        "cover_letter_used",
        "status",
        "notes",
        "created_at",
        "updated_at"
    ]

    values = [data.get(field) for field in fields[:-2]] + [current_time, current_time]
    placeholders = ", ".join(["?"] * len(fields))

    sql = f"INSERT INTO applications({','.join(fields)}) VALUES({placeholders})"
    
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_row_id = cursor.lastrowid
    if last_row_id is None:
        raise ValueError("Failed to insert application, no row ID returned.")
    conn.close()

    return last_row_id

def get_all_applications() -> list[dict[str, Union[str, float]]]:
    conn, cursor = get_dict_cursor()

    cursor.execute('SELECT * FROM applications')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return rows

def get_applications_by_status(status: ApplicationStatus) -> list[dict[str, Union[str, float]]]:
    conn, cursor = get_dict_cursor()

    cursor.execute('SELECT * FROM applications WHERE status = ?', (status.value, ))

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return rows

def delete_application(application_id: int) -> bool:
    conn, cursor = get_dict_cursor()

    cursor.execute('DELETE FROM applications WHERE id = ?', (application_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted