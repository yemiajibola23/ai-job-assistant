from backend.notion.service import push_to_notion, pull_from_notion
from backend.db.application_dao import get_all_applications, update_application_synced_at
from backend.enums.application_status import ApplicationStatus
from datetime import datetime

def sync_applications_to_notion(conn):
    applications = get_all_applications(conn)
    applications_to_sync = []

    for application in applications:
        if application["status"] != ApplicationStatus.INTERVIEW.value:
            continue

        if application["synced_at"] is None:
            applications_to_sync.append(application)
            continue

        updated_at_raw = application["updated_at"]
        synced_at_raw = application["synced_at"]

        if not isinstance(updated_at_raw, str):
            continue  # or raise an error if this is unexpected

        if not isinstance(synced_at_raw, str):
            continue # or raise an error if this is unexpected

        updated_at = datetime.fromisoformat(updated_at_raw)
        synced_at = datetime.fromisoformat(synced_at_raw)

        if updated_at > synced_at:
            applications_to_sync.append(application)
        
    if applications_to_sync:
        push_to_notion(applications_to_sync)

    for application in applications_to_sync:
        update_application_synced_at(conn, application["id"])
