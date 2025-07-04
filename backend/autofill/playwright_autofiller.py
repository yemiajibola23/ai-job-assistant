from playwright.sync_api import sync_playwright
from backend.autofill.field_matcher import match_label_to_key
from typing import Optional, Any
import os
from backend.utils.logging import get_logger
from backend.generation.export.tailored_resume_exporter import generate_and_render_tailored_resume
from pathlib import Path

logger = get_logger(__name__)
class PlaywrightAutofiller:
    def __init__(self, job_url: str, job_id: str, job_description: str, resume_data: dict):
        self.job_url = job_url
        self.job_id = job_id
        self.job_description = job_description
        self.resume_data = resume_data
        self.uploaded_resume_path: Optional[Path] = None
        
    def _fill_multistep_form(self, page: Any, application_data: dict) -> None:
        max_steps = 5
        for _ in range(max_steps):
            self._fill_fields(page, application_data)
            if not self._click_next_if_available(page):
                break

    def _click_next_if_available(self, page: Any) -> bool:
        try:
            next_button = page.query_selector("button:text('Next'), button:text('Continue'), button:text('→')")
            
            if next_button:
                logger.debug("[multistep] ⏭ Clicking next/continue button")
                next_button.click()
                page.wait_for_timeout(10000)
                return True
        except Exception as e:
            logger.error(f"[multistep] ⚠️ Failed to click next: {e}")
        
        return False
        
    def fill_form(self, application_data: dict, page: Optional[Any]=None) -> dict:
        if page is None:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context()
                page = context.new_page()
                page.goto(self.job_url)
                self._fill_multistep_form(page, application_data)
        else:
            # page.goto(self.job_url)
            self._fill_multistep_form(page, application_data)
        
        return {
            "status": "submitted",
            "resume_used": str(self.uploaded_resume_path)
        }
            
    def _fill_fields(self, page: Any, application_data: dict) -> None:
        fields = page.query_selector_all("input, textarea")
        for field in fields:
            label = self.extract_field_label(field, page)
            if not label:
                logger.warning("No label found for field")
                continue
            key = match_label_to_key(label)
            if not key:
                logger.warning(f"[matcher] ❌ Unrecognized label → '{label.strip()}'")
                continue
            value = application_data.get(key)
            if not value:
                logger.warning(f"[matcher] ⚠️ No resume value found for key: '{key}' (matched from '{label.strip()}')")
                continue
            
            try:
                input_type = field.get_attribute("type") or ""
                tag_name = field.evaluate("el => el.tagName.toLowerCase()")
                
                if tag_name == "select":
                    field.select_option(value)
                    logger.debug(f"[autofill] ✅ Selected option for '{label.strip()}' as '{key}'")
                elif input_type == "radio":
                    radio_value = field.evaluate("el => el.value")
                    if radio_value == value:
                        field.check()
                        logger.debug(f"[autofill] ✅ Checked radio for '{label.strip()}' as '{key}'")
                elif input_type == "file":
                    if "resume" == label.lower():
                        self.uploaded_resume_path = generate_and_render_tailored_resume(job_id=self.job_id, resume_data=self.resume_data, job_description=self.job_description)
                    if not os.path.isfile(value):
                        logger.warning(f"[autofill] ❌ File not found: {value}")
                        continue
                    
                    field.set_input_files(value)
                    logger.debug(f"[autofill] ✅ Uploaded file for '{label.strip()}' as '{key}'")
                else:
                    field.fill(value)
                    logger.debug(f"[autofill] ✅ Filled '{label.strip()}' as '{key}' with type '{input_type or tag_name}'")
            except Exception as e:
                logger.error(f"[autofill] ⚠️ Failed to handle field '{label.strip()}': {e}")
                
                       
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
            
            return field.evaluate("node => node.parentElement?.innerText") or ""
        except Exception as e:
            logger.error(e)