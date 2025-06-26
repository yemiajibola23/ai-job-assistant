from backend.notion.notion_client import get_notion_client
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_DB_ID = os.getenv("NOTION_DB_ID")

def push_to_notion(jobs: list[dict]) -> dict:
    """Handles creating or updating a Notion page based on job_url."""
    print(f"🚀 Pushing {len(jobs)} jobs to Notion (stub)")
    return {}

def pull_from_notion() -> list[dict]:
    print("⬇️ Pulling jobs from Notion (stub)")
    return []

def create_page(job: dict, client=None):
    if client is None:
        client = get_notion_client()

    payload = {
        "parent": { "database_id": NOTION_DB_ID },
        "properties": {
            "Name": {
                "title": [{"text": {"content": job["company_name"]}}]
            },
            "Position Title": {
                "rich_text": [{"text": {"content": job["job_title"]}}]
            },
            "Location": {
                "multi_select": [{"name": loc.strip()} for loc in job["location"].split(",")]
            },
            "Job Link": {
                "url": job["job_url"]
            },
            "Level": {
                "select": { "name": job.get("level", "Senior") }
            },
            "Status": {
                "status": { "name": job["status"] }
            },
            "Interview Stage": {
                "select": { "name": job.get("interview_stage", "Recruiter Call") }
            }
        }
    }

    return client.pages.create(**payload)