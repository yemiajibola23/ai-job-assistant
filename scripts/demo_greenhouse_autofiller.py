from playwright.async_api import async_playwright
from pathlib import Path
import json
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller
import asyncio

def load_user_profile():
    path = Path("scripts/data/user_profile.json")
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def test_job_dictionary():
    return {
            "job_title": "iOS Engineer",
            "company_name": "SerpAPI Co",
            "location": "Remote",
            "url": "https://jobs.lever.co/ios-engineer",
            "source": "Lever"
        }
    
profile_data = load_user_profile()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        print("🌐 Navigating to Greenhouse job form...")
        await page.goto("https://job-boards.greenhouse.io/speechify/jobs/5411578004")
        await page.wait_for_selector('input[type="file"]', state="visible")

        print("🤖 Running autofill (dry-run)...")
        autofiller = GreenhouseAutofiller()
        result = await autofiller.autofill(profile_data,"path/to/resume", "path/to/cover", test_job_dictionary(), page, dry_run=True)
        
        print("=== Result Log ===")
        for key, val in result.items():
            print(f"{key}: {val}")
        
        print("✅ Autofill complete. Observe the browser before it closes...")
        input("Press Enter to close browser...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())