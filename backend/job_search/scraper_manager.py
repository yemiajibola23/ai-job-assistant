from backend.job_search import lever_scraper
def get_jobs(query: str) -> list[dict]:
    return lever_scraper.fetch_jobs(query)