import streamlit as st
from app.ui_helpers import get_alert_status_message
from backend.utils.scheduler import run_scheduler_job

if "seen_ids" not in st.session_state:
    st.session_state.seen_ids = set()

def job_fetcher():
    return [{"job_id": "2"}, {"job_id": "3"}]

def handler(new_jobs):
    st.write(f"🆕 Found {len(new_jobs)} new job(s): {[job['job_id'] for job in new_jobs]}")
    st.session_state.seen_ids.update(job["job_id"] for job in new_jobs)

enabled = st.checkbox("Enable Alerts")
st.write(get_alert_status_message(enabled))

if enabled:
    run_scheduler_job(job_fetcher, handler, st.session_state.seen_ids)