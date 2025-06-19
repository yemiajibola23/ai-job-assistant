import schedule
import time
from backend.db.tracker import has_seen_job, mark_job_as_seen

def run_scheduler_job(job_fetcher, handler):
    current_jobs = job_fetcher()

    new_jobs = []
    for job in current_jobs:
        job_id = job.get("job_id")
        if job and not has_seen_job(job_id):
            new_jobs.append(job)
            mark_job_as_seen(job_id)
    
    if new_jobs:
        handler(new_jobs)

def start_scheduler_loop(job_fetcher, handler, interval=10):
    schedule.every(interval).seconds.do(lambda: run_scheduler_job(job_fetcher, handler))

    print(f"🔄 Scheduler started: checking every {interval} seconds...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
