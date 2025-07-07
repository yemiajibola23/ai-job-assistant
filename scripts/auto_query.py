from backend.resume.resume_parser import parse_resume_text
import sqlite3
from backend.db.job_dao import save_jobs_to_db
from backend.job_search.query_utils import extract_query_fields
from backend.job_search.serpapi_fetcher import fetch_jobs
from backend.ranking.scoring import score_jobs
from backend.job_search.parse_query import build_query_string, parse_query
from typing import Optional
from backend.resume.resume_parser import load_resume_text

def run_auto_query(resume_path: str, conn: sqlite3.Connection, user_query: Optional[str] = None) -> dict:
    resume_text = load_resume_text(resume_path)
    
    if user_query and user_query.strip():
        user_query = user_query.strip()
        print(f"🧠 Parsing user query: {user_query}")
        parsed_query = parse_query(user_query)
        query = build_query_string(
            parsed_query.get("job_title"),
            parsed_query.get("location"),
            parsed_query.get("work_type"),
            parsed_query.get("level")
        )
    else:
        parsed_resume_dict = parse_resume_text(resume_text)
        query_fields = extract_query_fields(parsed_resume_dict)
        query = build_query_string(
            query_fields["job_title"],
            query_fields["location"],
            query_fields.get("work_type"),
            query_fields.get("inferred_level")
        )
    
    jobs = fetch_jobs(query)
    matches = score_jobs(jobs, resume_text)
    saved_count = save_jobs_to_db(conn, matches)

    return {
        "query": query,
        "matches": matches,
        "saved_count": saved_count
    }