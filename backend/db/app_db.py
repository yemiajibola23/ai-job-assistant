import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from backend.enums.application_status import ApplicationStatus
from typing import Union, Optional
from datetime import datetime
from backend.db.schema import insert_job_sql


from backend.db.schema import (
    create_applications_table,
    create_jobs_table,
    create_seen_jobs_table
)
BASE_DIR = Path(__file__).parent
DB_PATH  = BASE_DIR / "job_assistant.db"

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_dict_cursor():
    conn =  get_connection()
    cursor = conn.cursor()

    return conn, cursor

def _init_db(path: Path=DB_PATH):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Check if any table exists that matches schema
    for table_name in ["jobs", "seen_jobs", "applications"]:
        schema_sql = ""
        if table_name == "jobs":
            schema_sql = create_jobs_table
        elif table_name == "seen_jobs":
            schema_sql = create_seen_jobs_table
        else:
            schema_sql = create_applications_table
    

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"🛠️ Creating table '{table_name}' in {path.name}...")
            cursor.execute(schema_sql)
            conn.commit()
        else:
            print(f"✅ Table '{table_name}' already exists in {path.name}")

   

    conn.close()

def extract_table_name(sql: str) -> str:
    print(f"📝 SQL statement: {sql}")
    # very basic extractor assuming `CREATE TABLE IF NOT EXISTS table_name ...`
    return sql.split()[5]


def clear_table(db_path: Path = DB_PATH, table_name: str = "jobs"):
    if not db_path.exists():
        print("⚠️ Cannot clear jobs table — DB does not exist.")
        return

    # Ensure schema exists before attempting to clear
    _init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}.db")
    conn.commit()
    conn.close()
    print(f"🧹 Cleared all entries from {table_name}.db")

def save_jobs_to_db(jobs: List[Dict[str, Any]], db_path: Path = DB_PATH) -> int:
    """
    Saves a list of job dicts into the SQLite database.

    Args:
        jobs: List of job dicts (each must contain id, title, etc.)
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        saved_jobs = 0

        for job in jobs:
            print(f"📝 Saving job: {job['id']} – {job.get('title')}")
            row_count = cursor.execute(insert_job_sql, (
                job["id"],
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("url"),
                job.get("description"),
                job.get("score"),
            )).rowcount

            saved_jobs += row_count
        conn.commit()
        print(f"✅ Committed {saved_jobs} new jobs to DB")
        return saved_jobs
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"❌ Failed to save jobs to DB: {e}")
    finally:
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

def get_application_by_id(db: sqlite3.Connection, id: int) -> dict[str, Union[str, float]]:
    cursor = db.cursor()
    cursor.execute('SELECT * FROM applications WHERE id = ?', (id, ))
    return cursor.fetchone()

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

def update_application_status_and_notes(conn: sqlite3.Connection, id: int, status: str, notes: str):
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE applications
            SET status = ?, notes = ?
            WHERE id = ?
            """,(status, notes, id))
    conn.commit()

    return cursor.rowcount > 0

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


