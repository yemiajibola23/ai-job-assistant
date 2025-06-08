from backend.utils.scheduler import find_new_jobs, run_scheduler_job
def test_find_new_jobs_returns_only_unseen_jobs():
    seen_ids = { "1", "2" }
    current_jobs = [{"job_id" : "2"}, {"job_id" : "3"}]
    expected_new_jobs = [{"job_id" : "3"}]

    unseen_jobs = find_new_jobs(current_jobs, seen_ids)

    assert unseen_jobs == expected_new_jobs

def test_run_scheduler_job_calls_handler_for_new_jobs():

    flags = {"called": False}

    def fake_handler(_):
        flags["called"] = True

    def fake_job_fetcher():
        return [{"job_id": "2"}, {"job_id": "3"}]
    
    seen_ids = { "1", "2" }


    run_scheduler_job(fake_job_fetcher, fake_handler, seen_ids)

    assert flags["called"] is True