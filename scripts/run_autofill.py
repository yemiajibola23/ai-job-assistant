from playwright.sync_api import sync_playwright
from backend.autofill.autofill import autofill_form

def run():
    field_map = {
        "input[name='custname']": "Yemi Ajibola",
        "input[name='custemail']": "yemi@example.com",
        "textarea[name='comments']": "Excited to apply!"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        page.goto("https://httpbin.org/forms/post")

        autofill_form(page, field_map)

        input("✅ Press Enter to submit the form...")

        page.evaluate("document.querySelector('form').submit()")

        input("✅ Press Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    run()