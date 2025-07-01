# - Import scraper_manager
from backend.job_search import scraper_manager

def test_scraper_success_fetches_from_serpapi(monkeypatch):
    def mock_lever_fetch_jobs(query):
        raise AssertionError("Should fetch from SerpAPI")
    def mock_greenhouse_fetch_jobs(query):
        raise AssertionError("Should fetch from SerpAPI")

    def mock_ashby_fetch_jobs(query):
        raise AssertionError("Should fetch from SerpAPI")

    def mock_serpapi_fetch_jobs(query):
        return [{
            "job_title": "Senior iOS Engineer", 
            "company_name": "Flock Safety", 
            "location": "Remote", 
            "url": "https://jobs.lever.co/flocksafety/7810dce1-c1bf-4f28-b5d9-800c5a7e1289",
            "source": "Lever"
        }]

    monkeypatch.setattr("backend.job_search.scrapers.lever_scraper.fetch_jobs", mock_lever_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scrapers.greenhouse_scraper.fetch_jobs", mock_greenhouse_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scrapers.ashby_scraper.fetch_jobs", mock_ashby_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scraper_manager.fetch_jobs_from_serpapi", mock_serpapi_fetch_jobs)
    
    result = scraper_manager.get_jobs("software engineer")
    
    assert len(result) == 1
    assert result[0]["job_title"] == "Senior iOS Engineer"
    assert result[0]["source"] == "Lever"


def test_serpapi_fail_fallback_to_scrapers(monkeypatch):
    def mock_serpapi_failure_fetch_jobs(query):
        raise RuntimeError("SerpAPI should not be called in fallback test.")

    def mock_lever_fetch_jobs(query):
        return [{
            "job_title": "iOS Engineer",
            "company_name": "SerpAPI Co",
            "location": "Remote",
            "url": "https://jobs.lever.co/ios-engineer",
            "source": "Lever"
        }]
    def mock_greenhouse_fetch_jobs(query):
        return []
        
    def mock_ashby_fetch_jobs(query):
        return []
    

    monkeypatch.setattr("backend.job_search.scrapers.lever_scraper.fetch_jobs", mock_lever_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scrapers.greenhouse_scraper.fetch_jobs", mock_greenhouse_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scrapers.ashby_scraper.fetch_jobs", mock_ashby_fetch_jobs)
    monkeypatch.setattr("backend.job_search.scraper_manager.fetch_jobs_from_serpapi", mock_serpapi_failure_fetch_jobs)

    result = scraper_manager.get_jobs("ios engineer")
    assert len(result) == 1
    assert result[0]["job_title"] == "iOS Engineer"
    assert result[0]["source"] == "Lever"