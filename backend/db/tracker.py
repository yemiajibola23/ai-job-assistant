import sqlite3
from datetime import datetime
from enums.application_status import ApplicationStatus
from typing import Union, Optional
from app_db import get_connection, get_dict_cursor
from schema import create_applications_table

def create_table(conn: Optional[sqlite3.Connection] = None):
    should_close = False

    if conn is None:
        conn = get_connection()
        should_close = True

    cursor = conn.cursor()
    cursor.execute(create_applications_table)
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

def has_seen_job(job_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seen_jobs WHERE job_id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()

    return result is not None

def mark_job_as_seen(job_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)", (job_id, ))
    conn.commit()
    conn.close()

