from backend.notion.service import push_to_notion, pull_from_notion
from backend.db.application_dao import get_all_applications
from backend.enums.application_status import ApplicationStatus
from datetime import datetime

__all__ = ["push_to_notion", "pull_from_notion"]

def sync_jobs_to_notion(conn):
    jobs = get_all_applications(conn)
    jobs_to_sync = []

    for job in jobs:
        if job["status"] != ApplicationStatus.INTERVIEW.value:
            continue

        if job["synced_at"] is None:
            jobs_to_sync.append(job)
            continue

        updated_at_raw = job["updated_at"]
        synced_at_raw = job["synced_at"]

        if not isinstance(updated_at_raw, str):
            continue  # or raise an error if this is unexpected

        if not isinstance(synced_at_raw, str):
            continue # or raise an error if this is unexpected

        updated_at = datetime.fromisoformat(updated_at_raw)
        synced_at = datetime.fromisoformat(synced_at_raw)

        if updated_at > synced_at:
            jobs_to_sync.append(job)
        
    if jobs_to_sync:
        push_to_notion(jobs_to_sync)
