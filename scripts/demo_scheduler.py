from backend.utils.scheduler import start_scheduler_loop
from backend.job_search.serpapi_fetcher import job_fetcher as serpapi_fetcher
from backend.db.job_dao import save_jobs_to_db
import sqlite3

TEST_DB_PATH = "test-job-assistant.db"

conn = sqlite3.connect(TEST_DB_PATH)

def job_fetcher():
    return serpapi_fetcher(job_title="iOS Engineer",
                           location="Remote",
                           work_type="remote",
                           level="Senior")

def handler(new_jobs):
    print(f"🆕 Found {len(new_jobs)} new job(s): {[job['job_id'] for job in new_jobs]}")
    save_jobs_to_db(conn, new_jobs)




def main():
    start_scheduler_loop(job_fetcher, handler, interval=5)

if __name__ == "__main__":
    main()

