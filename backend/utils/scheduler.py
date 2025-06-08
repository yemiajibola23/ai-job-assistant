def find_new_jobs(current_jobs, seen_ids):
    return [job for job in current_jobs if job["job_id"] not in seen_ids]

def run_scheduler_job(job_fetcher, handler, seen_ids):
    current_jobs = job_fetcher()

    new_jobs = find_new_jobs(current_jobs, seen_ids)

    if new_jobs:
        handler(new_jobs)