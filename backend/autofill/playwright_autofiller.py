from playwright.sync_api import sync_playwright
from backend.autofill.field_matcher import match_label_to_key
from typing import Optional, Any

class PlaywrightAutofiller:
    def __init__(self, job_url: str):
        self.job_url = job_url

    def fill_form(self, application_data: dict, page: Optional[Any]=None) -> None:
        if page is None:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context()
                page = context.new_page()
                page.goto(self.job_url)
                self._fill_fields(page, application_data)
        else:
            page.goto(self.job_url)
            self._fill_fields(page, application_data)
            
    def _fill_fields(self, page: Any, application_data: dict) -> None:
        fields = page.query_selector_all("input, textarea")
        for field in fields:
            label = self.extract_field_label(field, page)
            if not label:
                # TODO: Replace with logging
                print("No label found for field")
                continue
            key = match_label_to_key(label)
            if not key:
                print(f"Unrecognized label: {label}")
                continue
            value = application_data.get(key)
            if not value:
                print(f"No resume value found for key: {key}")
                continue
            field.fill(value)
                       
    def extract_field_label(self, field, page):
        try: 
            aria = field.get_attribute("aria-label")
            placeholder = field.get_attribute("placeholder")
            id = field.get_attribute("id")
            if aria:
                return aria
            if placeholder:
                return placeholder
            if id:
                label_element = page.query_selector(f"label[for='{id}']")
                if label_element:
                    return label_element.inner_text()
            
            return field.evaluate("node => node.parentElement?.innerText")
        except Exception as e:
            print(e) # TODO - Replace with proper logging.
