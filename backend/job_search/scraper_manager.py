from backend.job_search import lever_scraper, ashby_scraper, greenhouse_scraper, serpapi_fetcher
def get_jobs(query: str) -> list[dict]:
    jobs = []
    for scraper in [lever_scraper, greenhouse_scraper, ashby_scraper]:
        try:
            results = scraper.fetch_jobs(query)
            jobs.extend(results)
        except Exception as e:
            print(f"⚠️ {scraper.__name__} failed: {e}")

    
    if not jobs:
        try:
            results = serpapi_fetcher.fetch_jobs(query)
            jobs = results
        except Exception as e:
            print(f"⚠️ SerpAPI fallback failed: {e}")

    
    return jobs