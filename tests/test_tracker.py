import sqlite3
from backend.db.tracker import create_table, add_application

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

def test_add_application_inserts_data():
    data = {
        "job_title": "Senior iOS Engineer", 
            "company_name": "Flock Safety", 
            "location": "Remote", 
            "job_url": "https://www.flocksafety.com/careers?ashby_jid=7810dce1-c1bf-4f28-b5d9-800c5a7e1289#ashby_embed", 
            "match_score":0.7, 
            "resume_used": "yemi_ajibola.pdf", 
            "cover_letter_used": "yemi_ajibola_cover_letter.pdf", 
            "status": "Interviewing", 
            "notes":""
            }
    app_id = add_application(data)
    assert isinstance(app_id, int) and app_id > 0

    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    
    assert cursor.fetchone()[1] == 'Senior iOS Engineer'

    conn.close()