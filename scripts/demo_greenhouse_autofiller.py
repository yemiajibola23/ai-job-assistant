from playwright.sync_api import sync_playwright
from backend.autofill.autofill_router import autofill_router
from pathlib import Path
import json

def load_user_profile():
    path = Path("scripts/data/user_profile.json")
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
profile_data = load_user_profile()
application_data = {
    "name": "Yemi Ajibola",
    "email": "yemi@example.com",
    "phone": "555-123-4567",
    "location": "United States"
}

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        print("🌐 Navigating to Greenhouse job form...")
        page.goto("https://job-boards.greenhouse.io/speechify/jobs/5411578004")
        page.wait_for_load_state("networkidle")

        print("🤖 Running autofill (dry-run)...")
        autofill_router(page, application_data, dry_run=True)

        print("✅ Autofill complete. Observe the browser before it closes...")
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    run()