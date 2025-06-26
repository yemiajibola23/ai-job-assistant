import os
import pytest
from backend.notion.service import push_to_notion, find_page_by_job_url, delete_test_pages
from backend.notion.notion_client import get_notion_client

client = get_notion_client()

@pytest.mark.integration
def test_push_and_update_application_to_notion():
    # Initial push — should create the page
    job = {
        "job_title": "Integration iOS Engineer",
        "company_name": "NotionTestCo",
        "location": "Remote",
        "job_url": "https://integration.test/job-ios",
        "status": "Interviewing",
        "level": "Mid",
        "interview_stage": "Recruiter Call"
    }

    # First push should create
    result = push_to_notion([job], client=client)
    assert result["synced_applications"] == 1

    # Second push with updated fields — should update
    job["status"] = "Offer"
    job["interview_stage"] = "Technical Interview"

    result = push_to_notion([job], client=client)
    assert result["synced_applications"] == 1

    # Verify the page was updated
    page = find_page_by_job_url(job["job_url"], client)
    assert page is not None

    props = page["properties"]

    # Check if the updated status and stage were reflected
    assert props["Status"]["status"]["name"] == "Offer"
    assert props["Interview Stage"]["select"]["name"] == "Technical Interview"

    delete_test_pages(client)
