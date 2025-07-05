from backend.resume.resume_parser import load_resume_text
from backend.job_search.serpapi_fetcher import fetch_jobs
from backend.ranking.scoring import match_resume_to_jobs
from backend.utils.constants import DEFAULT_SCORE_THRESHOLD

def build_query_string(job_title, location=None, work_type=None, level=None):
    parts = [level, job_title, work_type, location]
    return " ".join([p.strip() for p in parts if p])

def fetch_and_score_jobs(query_dict: dict, resume_path: str) -> list[dict]:
    """
    Fetches jobs using the query_dict, embeds and scores them against resume text.

    Returns:
        List of job dicts with 'score' field added.
    """
    resume_text = load_resume_text(resume_path)
    query = build_query_string(query_dict["job_title"], query_dict["location"], query_dict["work_type"], query_dict["level"])
    jobs = fetch_jobs(query)
    
    descriptions = [job["description"] for job in jobs]
    ranked_scores = match_resume_to_jobs(resume_text, descriptions)

    # Attach scores to job entries
    desc_to_score = dict(ranked_scores)
    for job in jobs:
        job["score"] = round(desc_to_score.get(job["description"], 0.0), 3)

    return jobs
