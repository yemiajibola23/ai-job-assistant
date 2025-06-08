from backend.utils.scheduler import start_scheduler_loop

seen_ids = {"1", "2"}

def job_fetcher():
    return [{"job_id": "2"}, {"job_id": "3"}]

def handler(new_jobs):
    print(f"🆕 Found {len(new_jobs)} new job(s): {[job['job_id'] for job in new_jobs]}")

start_scheduler_loop(job_fetcher, handler, seen_ids, interval=5)
