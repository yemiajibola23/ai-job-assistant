from playwright.sync_api import sync_playwright
from backend.autofill.autofill import autofill_application
from backend.resume.resume_parser import load_resume_text, parse_resume_text
from backend.utils.constants import TEST_RESUME_PATH

def run():
    resume_text = load_resume_text(TEST_RESUME_PATH)
    parsed_resume = parse_resume_text(resume_text)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        page.goto("https://httpbin.org/forms/post")

        autofill_application(page, parsed_resume)

        input("✅ Press Enter to submit the form...")

        # You can submit manually, or do:
        page.evaluate("document.querySelector('form').submit()")

        input("✅ Press Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    run()
