import sqlite3

def init_db(db_path: str = "jobs.db"):
    """
    Initializes the job database and creates the jobs table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Write your CREATE TABLE statement here
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT,
        location TEXT,
        url TEXT,
        description TEXT, 
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ DB initialized and 'jobs' table ensured.")