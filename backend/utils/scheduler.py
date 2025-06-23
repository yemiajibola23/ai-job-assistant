import schedule
import time
from backend.db.job_dao import has_seen_job, mark_job_as_seen
import sqlite3
conn = sqlite3.connect("job-assistant.db")
def run_scheduler_job(conn, job_fetcher, handler):
    current_jobs = job_fetcher()

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


def start_scheduler_loop(job_fetcher, handler, interval=10):
    schedule.every(interval).seconds.do(lambda: run_scheduler_job(conn, job_fetcher, handler))

    print(f"🔄 Scheduler started: checking every {interval} seconds...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
