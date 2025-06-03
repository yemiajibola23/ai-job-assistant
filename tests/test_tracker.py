import sqlite3
from backend.db.tracker import create_table

def test_create_table_structure():
    create_table("test-application.db")

    conn = sqlite3.connect('test-application.db')
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