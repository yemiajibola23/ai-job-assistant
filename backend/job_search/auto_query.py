from backend.resume.resume_parser import parse_resume_text, load_resume_text
import sqlite3
from backend.ranking.pipeline import fetch_and_score_jobs, build_query_string
from backend.db.job_dao import save_jobs_to_db
from backend.job_search.query_utils import extract_query_fields

def run_auto_query(resume_path: str, conn: sqlite3.Connection) -> dict:
    resume_text = load_resume_text(resume_path)
    parsed_resume_dict = parse_resume_text(resume_text)
    query_fields = extract_query_fields(parsed_resume_dict)
    matches = fetch_and_score_jobs(query_fields, resume_path)
    query_str = build_query_string(**query_fields)
    saved_count = save_jobs_to_db(conn, matches)

    return {
        "query": query_str,
        "matches": matches,
        "saved_count": saved_count
    }