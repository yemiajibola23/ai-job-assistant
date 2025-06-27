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


def filter_and_match_jobs(jobs: list[dict], resume_text: str, threshold: float = DEFAULT_SCORE_THRESHOLD) -> list[dict]:
    """
    Filters job list by computing score and applying a similarity threshold.

    Returns:
        List of matched jobs (above threshold), each with a 'score' field.
    """
    descriptions = [job["description"] for job in jobs]
    ranked_scores = match_resume_to_jobs(resume_text, descriptions)

    desc_to_score = dict(ranked_scores)
    matched_jobs = []

    for job in jobs:
        score = desc_to_score.get(job["description"], 0.0)
        job["score"] = round(score, 3)
        if score >= threshold:
            job["matched"] = True
            matched_jobs.append(job)
        else:
            job["matched"] = False
            job["rejection_reason"] = "score below threshold"

    return matched_jobs
