# - Import scraper_manager
from backend.job_search import scraper_manager
# - Mock lever_scraper, greenhouse_scraper, and serpapi_fetcher
def mock_lever_fetch_jobs(query):
    return [{
        "job_title": "Senior iOS Engineer", 
        "company_name": "Flock Safety", 
        "location": "Remote", 
        "url": "https://jobs.lever.co/flocksafety/7810dce1-c1bf-4f28-b5d9-800c5a7e1289",
        "source": "Lever"
    }]

def mock_greenhouse_fetch_jobs(query):
    return []

def mock_ashby_fetch_jobs(query):
    return []

def mock_serpapi_fetch_jobs(query):
    raise AssertionError("Fallback to SerpAPI was triggered even though a scraper returned jobs.")




def test_scraper_success(monkeypatch):
    monkeypatch.setattr("backend.job_search.lever_scraper.fetch_jobs", mock_lever_fetch_jobs)
    monkeypatch.setattr("backend.job_search.greenhouse_scraper.fetch_jobs", mock_greenhouse_fetch_jobs)
    monkeypatch.setattr("backend.job_search.ashby_scraper.fetch_jobs", mock_ashby_fetch_jobs)
    monkeypatch.setattr("backend.job_search.serpapi_fetcher.job_fetcher", mock_serpapi_fetch_jobs)
#     - lever returns jobs, greenhouse does not
    result = scraper_manager.get_jobs("software engineer")
#     - assert returned jobs match lever output
    assert len(result) == 1
    assert result[0]["job_title"] == "Senior iOS Engineer"
    assert result[0]["source"] == "Lever"


# - Test: test_scraper_fail_fallback_serpapi
#     - lever and greenhouse both raise exceptions
#     - serpapi returns jobs
#     - assert returned jobs match serpapi output

# - Test: test_all_scrapers_empty_then_fallback
#     - lever and greenhouse return empty
#     - serpapi returns jobs
#     - assert returned jobs match serpapi output