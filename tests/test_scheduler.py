from backend.utils.scheduler import find_new_jobs
def test_find_new_jobs_returns_only_unseen_jobs():
    seen_ids = { "1", "2" }
    current_jobs = [{"job_id" : "2"}, {"job_id" : "3"}]
    expected_new_jobs = [{"job_id" : "3"}]

    unseen_jobs = find_new_jobs(current_jobs, seen_ids)

    assert unseen_jobs == expected_new_jobs