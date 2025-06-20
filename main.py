import streamlit as st
from app.ui_helpers import get_alert_status_message
from backend.utils.scheduler import run_scheduler_job
from backend.job_search.serpapi_fetcher import job_fetcher
from backend.db.tracker import has_seen_job, mark_job_as_seen
from backend.db.jobs_db import save_jobs_to_db

def streamlit_job_sync():
    st.info("🔎 Querying SerpAPI...")
    jobs = job_fetcher("iOS Engineer", "Remote", "remote", "Senior")
    new_jobs = []
    for job in jobs:
        job_id = job["id"]
        if not has_seen_job(job_id):
            mark_job_as_seen(job_id)
            new_jobs.append(job)
    
    save_jobs_to_db(new_jobs)

    if new_jobs:
        st.success(f"✅ Added {len(new_jobs)} jobs to db.")
    else:
        st.info("No new jobs found.")


if __name__ == "__main__":
    st.header("📄 Job Discovery")

    if st.button("🔁 Run Job Sync"):
        streamlit_job_sync()