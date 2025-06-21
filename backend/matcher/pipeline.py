from backend.matcher.matcher import match_resume_to_jobs
from backend.resume.resume_parser import load_resume_text
from backend.job_search.serpapi_fetcher import job_fetcher

# def filter_and_match_jobs(jobs: list[dict], resume_text: str, threshold: float = 0.65) -> list[dict]:
#     print(f"🪵 Found {len(jobs)} jobs")
#     print(f"🪵 Descriptions extracted: {[job.get('description') for job in jobs]}")

#     #print(f"🧾 Resume preview:\n{resume_text[:250]}")

#     descriptions = [job["description"] for job in jobs]
#     ranked_scores = match_resume_to_jobs(resume_text, descriptions, 5)

#     desc_to_job = {job["description"]: job for job in jobs}
#     for desc, score in ranked_scores:
#             job = desc_to_job.get(desc)
#             if job:
#                 job["score"] = score
#                 job["matched"] = score >= threshold
#                 if not job["matched"]:
#                     job["rejection_reason"] = "score below threshold"
    
#     return [job for job in jobs if job.get("matched")]

def fetch_and_score_jobs(query_dict: dict, resume_path: str):
    resume_text = load_resume_text(resume_path)

    jobs = job_fetcher(
        query_dict["job_title"],
        query_dict["location"],
        query_dict["work_type"],
        query_dict["level"]
    )

    descriptions = [job["description"] for job in jobs]
    ranked_scores = match_resume_to_jobs(resume_text, descriptions)
     
    for job in jobs:
        match = next((t for t in ranked_scores if t[0] == job["description"]), None)
        job["score"] = round(match[1], 3) if match else None
    return jobs