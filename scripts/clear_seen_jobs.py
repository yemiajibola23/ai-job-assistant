import sqlite3

conn = sqlite3.connect("backend/db/applications.db")  # adjust path if needed
cursor = conn.cursor()

cursor.execute("DELETE FROM seen_jobs")
conn.commit()
conn.close()

print("🧹 Cleared seen_jobs table.")