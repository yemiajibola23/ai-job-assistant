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
            page = find_page_by_job_url(job["job_url"], client)
            if page:
                update_page(page["id"], job, client)
            else:
                create_page(job, client)
            synced += 1
        except Exception as e:
            print(f"❌ Failed to sync application: {job.get('job_title')} at {job.get('company_name')}")
            print(f"   Reason: {e}")
    return { "synced_applications": synced }
    

def pull_from_notion() -> list[dict]:
    print("⬇️ Pulling jobs from Notion (stub)")
    return []

def find_page_by_job_url(job_url: str, client) -> dict | None:
    query_result = client.databases.query(database_id=NOTION_DB_ID, filter={
        "property": "Job Link",
        "url": { "equals": job_url }
    })

    if query_result["results"]:
        return query_result["results"][0]
    else:
        return None
    
def update_page(page_id: str, job: dict, client):
    updated_properties = {
        "Status": {
            "status": { "name": job["status"] }
        },
        "Interview Stage": {
            "select": { "name": job.get("interview_stage", "Recruiter Call") }
        }
    }
    return client.pages.update(page_id=page_id, properties=updated_properties)

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

def delete_test_pages(client):
    pages = client.databases.query(
        database_id=os.getenv("NOTION_DB_ID"),
        filter={
            "property": "Job Link",
            "url": {
                "starts_with": "https://integration.test/"
            }
        }
    )["results"]

    for page in pages:
        try:
            client.pages.update(
                page_id=page["id"],
                archived=True
            )
        except Exception as e:
            print(f"❌ Failed to archive page {page['id']}: {e}")