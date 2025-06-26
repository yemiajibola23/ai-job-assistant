from typing import Union
import sqlite3
from backend.enums.application_status import ApplicationStatus
from typing import Optional
from datetime import datetime


def add_application(conn: sqlite3.Connection, data: dict[str, Union[str, float, ApplicationStatus]]) -> int:
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

    return last_row_id

def get_application_by_id(conn: sqlite3.Connection, id: int) -> dict[str, Union[str, float]]:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications WHERE id = ?', (id, ))
    return cursor.fetchone()

def get_all_applications(conn: sqlite3.Connection,) -> list[dict[str, Union[str, float]]]:
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM applications')
    rows = [dict(row) for row in cursor.fetchall()]
    
    
    return rows

def get_applications_by_status(conn: sqlite3.Connection, status: ApplicationStatus) -> list[dict[str, Union[str, float]]]:
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM applications WHERE status = ?', (status.value, ))

    rows = [dict(row) for row in cursor.fetchall()]
    

    return rows

def delete_application(conn: sqlite3.Connection, application_id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute('DELETE FROM applications WHERE id = ?', (application_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    

    return deleted

def update_application_status_and_notes(conn: sqlite3.Connection, id: int, status: str, notes: str, updated_at: Optional[str]=None):
    updated_at = updated_at or datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE applications
            SET status = ?, notes = ?, updated_at = ?
            WHERE id = ?
            """,(status, notes, updated_at, id))
    conn.commit()

    return cursor.rowcount > 0

def update_application_synced_at(conn: sqlite3.Connection, application_id: int):
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE applications
            SET synced_at = ?
            WHERE id = ?
                   """, (datetime.utcnow().isoformat(), application_id))
    
    conn.commit()