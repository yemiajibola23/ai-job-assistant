from backend.job_search.scrapers import lever_scraper, ashby_scraper, greenhouse_scraper
from backend.job_search.serpapi_fetcher import fetch_jobs as fetch_jobs_from_serpapi

def get_jobs(query: str) -> list[dict]:
    jobs = []
    try:
        jobs = fetch_jobs_from_serpapi(query)
    except Exception as e:
        print(f"⚠️ SerpAPI fetch failed: {e}")

    if not jobs:
        for scraper in [lever_scraper, greenhouse_scraper, ashby_scraper]:
            try:
                results = scraper.fetch_jobs(query)
                jobs.extend(results)
            except Exception as e:
                print(f"⚠️ {scraper.__name__} failed: {e}")
    
    return jobs