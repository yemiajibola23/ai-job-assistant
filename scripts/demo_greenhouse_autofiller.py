from playwright.sync_api import sync_playwright
from backend.autofill.autofill_router import autofill_router

application_data = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "555-123-4567",
    "resume_path": "/Users/yourname/Desktop/resume.pdf",  # replace path
    "cover_letter_path": "/Users/yourname/Desktop/cover.pdf",  # replace path
    "gender": "I don't wish to answer",
    "race": "Black or African American",
    "veteran_status": "I am not a veteran",
    "disability_status": "Yes, I have a disability",
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