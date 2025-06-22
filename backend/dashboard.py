import sqlite3
from backend.enums.application_status import ApplicationStatus

def get_application_count(db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM applications')
    row = cursor.fetchone()

    return row[0]

def get_application_count_grouped_by_status(db:  sqlite3.Connection) -> dict:
    cursor = db.cursor()
    cursor.execute('SELECT status, COUNT(*) FROM applications GROUP BY status')
    
    return {
        ApplicationStatus.from_value(status): count 
        for status, count in cursor.fetchall()
        }

def get_all_applications_ordered_by_date_created(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute('SELECT job_title, company_name, status, location, match_score, created_at FROM applications ORDER BY created_at DESC')

    return [dict(row) for row in cursor.fetchall()]

def get_dashboard_data(db:  sqlite3.Connection):
    return {
        "total_count": get_application_count(db),
        "status_count": get_application_count_grouped_by_status(db),
        "recent_apps": get_all_applications_ordered_by_date_created(db),
    }

    