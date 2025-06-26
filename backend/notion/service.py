from backend.notion.notion_client import get_notion_client
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_DB_ID = os.getenv("NOTION_DB_ID")

def push_to_notion(jobs: list[dict], client=None) -> dict:
    if client is None:
        client = get_notion_client()
    
    synced = 0
    for job in jobs:
        try:
            create_page(job, client)
            synced += 1
        except Exception as e:
            print(f"❌ Failed to sync application: {job.get('job_title')} at {job.get('company_name')}")
            print(f"   Reason: {e}")
    return { "synced_applications": synced }
    

def pull_from_notion() -> list[dict]:
    print("⬇️ Pulling jobs from Notion (stub)")
    return []

def create_page(job: dict, client):
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