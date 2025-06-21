import streamlit as st
from app.ui_helpers import get_alert_status_message
from backend.utils.scheduler import run_scheduler_job
from backend.job_search.serpapi_fetcher import job_fetcher
from backend.matcher.pipeline import filter_and_match_jobs
from backend.db.app_db import _init_db, clear_table, save_jobs_to_db, has_seen_job, mark_job_as_seen
import fitz
from backend.job_search.parse_query import parse_query

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page_number in range(len(doc)):
        page = doc[page_number]
        text += page.get_textpage().extractText()
    return text

def load_resume_text(path: str) -> str:
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def streamlit_job_sync():
    resume_text = load_resume_text("tests/data/yemi_resume.pdf")

    st.info("🔎 Querying SerpAPI...")
    jobs = job_fetcher("iOS Engineer", "Remote", "remote", "Senior")
    new_jobs = []
    for job in jobs:
        print(f"Listing job: {job['id']} – {job.get('title')}")
        job_id = job["id"]
        if not has_seen_job(job_id):
            mark_job_as_seen(job_id)
            new_jobs.append(job)
        else:
            print(f"{job['title']} at {job['company']} has been seen before")

    matched_jobs = filter_and_match_jobs(new_jobs, resume_text)
    print(matched_jobs)
    
    save_jobs_to_db(matched_jobs)

    if matched_jobs:
        st.success(f"🧠 {len(matched_jobs)} matched jobs saved!")
    else:
        st.info("❌ No new jobs found.")

# _init_db()
# clear_table(table_name="seen_jobs")
st.header("📄 Job Discovery")

if st.button("🔁 Run Job Sync"):
    streamlit_job_sync()

query = st.text_input("Enter job search query")
if st.button("🔎 Search"):
   result = parse_query(query)
   st.json(result)

   job_results = job_fetcher(result["job_title"], result["location"], result["work_type"], result["level"])

   for job in job_results:
       st.text(f"{job['title']} at {job['company']}")
   