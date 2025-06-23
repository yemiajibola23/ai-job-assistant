# from backend.utils.scheduler import run_scheduler_job

# def test_run_scheduler_job_calls_handler_for_new_jobs():

#     flags = {"called": False}

#     def fake_handler(_):
#         flags["called"] = True

#     def fake_job_fetcher():
#         return [{"job_id": "2"}, {"job_id": "3"}]
    
#     seen_ids = { "1", "2" }


#     run_scheduler_job(fake_job_fetcher, fake_handler, seen_ids)

#     assert flags["called"] is True