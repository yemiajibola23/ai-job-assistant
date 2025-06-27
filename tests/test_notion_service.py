from backend.notion.service import pull_from_notion

def test_pull_from_notion_returns_normalized_data(monkeypatch):
    fake_response = {
        "results": [
            {
                "properties": {
                    "Name": {
                        "title": [{"text": {"content": "Flock Safety"}}]
                    },
                    "Position Title": {
                        "rich_text": [{"text": {"content": "iOS Engineer"}}]
                    },
                    "Location": {
                        "multi_select": [{"name": "Remote"}, {"name": "Atlanta"}]
                    },
                    "Job Link": {
                        "url": "https://jobs.flocksafety.com"
                    },
                    "Status": {
                        "status": {"name": "Interview"}
                    },
                    "Interview Stage": {
                        "select": {"name": "Technical Interview"}
                    }
                }
            },
            {
                "properties": {
                    "Name": {
                        "title": [{"text": {"content": "Doist"}}]
                    },
                    "Position Title": {
                        "rich_text": [{"text": {"content": "Mobile Developer"}}]
                    },
                    "Location": {
                        "multi_select": [{"name": "Remote"}]
                    },
                    "Job Link": {
                        "url": "https://jobs.doist.com"
                    },
                    "Status": {
                        "status": {"name": "Applied"}
                    },
                    "Interview Stage": {
                        "select": {"name": "Recruiter Call"}
                    }
                }
            }
        ]
    }
    class FakeClient:
        class databases:
            @staticmethod
            def query(*args, **kwargs):
                return fake_response

       # Monkeypatch the get_notion_client function to return FakeClient
    monkeypatch.setattr("backend.notion.service.get_notion_client", lambda: FakeClient())

    results = pull_from_notion()

    assert len(results) == 2

    first = results[0]
    assert first["company_name"] == "Flock Safety"
    assert first["job_title"] == "iOS Engineer"
    assert first["location"] == "Remote, Atlanta"
    assert first["job_url"] == "https://jobs.flocksafety.com"
    assert first["status"] == "Interview"
    assert first["interview_stage"] == "Technical Interview"