import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import json

load_dotenv()
api_key = os.getenv("SERP_API_KEY")

def build_query_string(job_title, location=None, work_type=None, level=None):
    parts = [level, job_title, work_type, location]
    return "".join([p for p in parts if p])

def job_fetcher(job_title, location=None, work_type=None, level=None) -> list[dict]:
    query = build_query_string(job_title, location, work_type, level)

    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    print("🔍 Raw jobs_results from SerpAPI:")
    print(json.dumps(results.get("jobs_results", []), indent=2))

    jobs = []

    for job in results.get("job_results", []):
        jobs.append({
            "id": job.get("job_id"),
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "url": job.get("job_google_link"),
            "description": job.get("description"),
            "score": None
        })

    return jobs