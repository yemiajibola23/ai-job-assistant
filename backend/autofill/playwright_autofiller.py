from playwright.sync_api import sync_playwright

class PlaywrightAutofiller:
    def __init__(self, job_url: str):
        self.job_url = job_url

    def fill_form(self, application_data: dict) -> None:
       with sync_playwright() as p:
           browser = p.chromium.launch()
           context = browser.new_context()
           page = context.new_page()
           page.goto(self.job_url)
           
           fields =page.query_selector_all("input, textarea")
           for field in fields:
               field.fill("placeholder")  # TODO: replace with real matched value
               
    def extract_field_label(self, field, page):
        try: 
            aria = field.get_attribute("aria-label")
            placeholder = field.get_attribute("placeholder")
            if aria:
                return aria
            if placeholder:
                return placeholder
            return None
        except Exception as e:
            print(e) # TODO - Replace with proper logging.
