import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import json

load_dotenv()
api_key = os.getenv("SERP_API_KEY")

def build_query_string(job_title, location=None, work_type=None, level=None):
    parts = [level, job_title, work_type, location]
    return " ".join([p.strip() for p in parts if p])

def job_fetcher(job_title, location=None, work_type=None, level=None) -> list[dict]:
    query = build_query_string(job_title, location, work_type, level)
    print(f"Query string: {query}")
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs_results = results.get("jobs_results", [])
    print(f"🔍 Received {len(jobs_results)} raw job results from SerpAPI.")
    print("🔎 Previewing first 2 jobs:")
    print(json.dumps(jobs_results[:2], indent=2))

    jobs = []
    for job in results.get("jobs_results", []):
        job_id = job.get("job_id")

        if not job_id:
            print("⚠️ Skipping job without job_id")
            continue
        
        print(f"Looking at job from: {job.get('company_name')}")
        jobs.append({
            "id": job.get("job_id"),
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "url": job.get("share_link"),
            "description": job.get("description"),
            "score": None
        })

    return jobs