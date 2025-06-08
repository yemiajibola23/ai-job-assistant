def find_new_jobs(current_jobs, seen_ids):
    return [job for job in current_jobs if job["job_id"] not in seen_ids]