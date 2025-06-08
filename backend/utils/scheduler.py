import schedule
import time
def find_new_jobs(current_jobs, seen_ids):
    return [job for job in current_jobs if job["job_id"] not in seen_ids]

def run_scheduler_job(job_fetcher, handler, seen_ids):
    current_jobs = job_fetcher()

    new_jobs = find_new_jobs(current_jobs, seen_ids)

    if new_jobs:
        seen_ids.update(job["job_id"] for job in new_jobs) 
        handler(new_jobs)

def start_scheduler_loop(job_fetcher, handler, seen_ids, interval=10):
    schedule.every(interval).seconds.do(lambda: run_scheduler_job(job_fetcher, handler, seen_ids))

    print(f"🔄 Scheduler started: checking every {interval} seconds...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
