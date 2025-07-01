def test_fetch_jobs_from_lever_returns_normalized_jobs(monkeypatch):
    mock_response = [
        {
            "text": "iOS Engineer",
            "categories": {
                "location": "Remote",
                "team": "Engineering"
            },
            "hostedUrl": "https://jobs.lever.co/flocksafety/abc123"
        }
    ]
    
    def mock_request_get(*args, **kwargs):
        class MockResponse:
            def json(self): return mock_response
            @property
            def status_code(self): return 200
        return MockResponse()
    
    
    monkeypatch.setattr("requests.get", mock_request_get)
    from backend.job_search.scrapers.lever_scraper import fetch_jobs
    jobs = fetch_jobs("ios")
    
    assert len(jobs) == 1
    assert jobs[0]["job_title"] == "iOS Engineer"
    assert jobs[0]["company_name"] == "Flock Safety"
    assert jobs[0]["location"] == "Remote"
    assert jobs[0]["url"].startswith("https://jobs.lever.co/")