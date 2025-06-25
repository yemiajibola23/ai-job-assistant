import schedule
import time
from backend.db.job_dao import has_seen_job, mark_job_as_seen
import sqlite3

def run_scheduler_job(conn, job_fetcher, handler, notify=None):
    current_jobs = job_fetcher()
    if not current_jobs:
        print("⚠️ No jobs fetched. Skipping...")
        return
    
    print(f"📦 Total jobs fetched: {len(current_jobs)}")

    new_jobs = []
    for job in current_jobs:
        job_id = job.get("id")
        if job_id and not has_seen_job(conn, job_id):
            new_jobs.append(job)
            mark_job_as_seen(conn, job_id)

    print(f"🧮 New unseen jobs: {len(new_jobs)}")
    if new_jobs:
        handler(new_jobs)
        if notify:
            notify(f"🆕 {len(new_jobs)} new jobs")

def start_scheduler_loop(conn, job_fetcher, handler, interval=10, notify=None):
    schedule.every(interval).seconds.do(lambda: run_scheduler_job(conn, job_fetcher, handler, notify))

    print(f"🔄 Scheduler started: checking every {interval} seconds...\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Scheduler stopped by user.")