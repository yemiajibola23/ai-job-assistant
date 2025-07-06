from playwright.sync_api import sync_playwright
from backend.autofill.field_matcher import match_label_to_key
from typing import Optional, Any
import os
from backend.utils.logging import get_logger
from pathlib import Path
import json

logger = get_logger(__name__)
class PlaywrightAutofiller:
    def __init__(self, job_url: str):
        self.job_url = job_url
        self.uploaded_resume_path: Optional[Path] = None
        self.uploaded_cover_letter_path: Optional[Path] = None
        
    def _fill_multistep_form(self, page: Any, application_data: dict, result_log: dict) -> None:
        max_steps = 5
        for _ in range(max_steps):
            self._fill_fields(page, application_data, result_log)
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
    
    def _check_for_submission_confirmation(self, page) -> bool:
        possible_texts = ["Thank you", "Application submitted", "We received", "Your application"]
        for text in possible_texts:
            if page.query_selector(f"text=/{text}/i"):
                return True
        return False
        
        
    def fill_form(self, application_data: dict, page: Optional[Any]=None) -> dict:
        result_log = {
            "filled_fields": [],
            "skipped_fields": [],
            "uploaded_files": {},
            "errors": [],
            "clicked_submit": False,
            "confirmation_found": False
        }
        
        if page is None:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context()
                page = context.new_page()
                page.goto(self.job_url)
                self._fill_multistep_form(page, application_data, result_log)
                
                result_log["clicked_submit"] = self._click_next_if_available(page)
                
                page.wait_for_timeout(3000)
                result_log["confirmation_found"] = self._check_for_submission_confirmation(page)
        else:
            self._fill_multistep_form(page, application_data, result_log)
        
        logger.info(f"[autofill] 🧾 Autofill Result Log: {json.dumps(result_log, indent=2)}")

        return result_log
            
    def _fill_fields(self, page: Any, application_data: dict, result_log: dict) -> None:
        fields = page.query_selector_all("input, textarea")
        for field in fields:
            label = self.extract_field_label(field, page)
            if not label:
                logger.warning("No label found for field")
                result_log["skipped_fields"].append("unlabeled: unknown field")
                continue
            key = match_label_to_key(label)
            if not key:
                logger.warning(f"[matcher] ❌ Unrecognized label → '{label.strip()}'")
                result_log["skipped_fields"].append(f"unmatched: {label.strip()}")
                continue
            value = application_data.get(key)
            if not value:
                logger.warning(f"[matcher] ⚠️ No resume value found for key: '{key}' (matched from '{label.strip()}')")
                result_log["skipped_fields"].append(key)
                continue
            
            try:
                input_type = field.get_attribute("type") or ""
                tag_name = field.evaluate("el => el.tagName.toLowerCase()")
                
                if tag_name == "select":
                    field.select_option(value)
                    logger.debug(f"[autofill] ✅ Selected option for '{label.strip()}' as '{key}'")
                    result_log["filled_fields"].append(key)
                elif input_type == "radio":
                    radio_value = field.evaluate("el => el.value")
                    if radio_value == value:
                        field.check()
                        logger.debug(f"[autofill] ✅ Checked radio for '{label.strip()}' as '{key}'")
                        result_log["filled_fields"].append(key)
                elif input_type == "file":
                    if not os.path.isfile(value):
                        logger.warning(f"[autofill] ❌ File not found: {value}")
                        continue
                    field.set_input_files(value)
                    logger.debug(f"[autofill] ✅ Uploaded file for '{label.strip()}' as '{key}'")
                    result_log["uploaded_files"][key] = [value]
                    result_log["filled_fields"].append(key)
                    
                    if "resume" in label.lower():
                        self.uploaded_resume_path = value
                    elif "cover" in label.lower():
                        self.uploaded_cover_letter_path = value
                elif tag_name == "textarea" and self._is_essay_field(field):
                    essay_prompt = self.generate_essay_response(label, application_data)
                    if essay_prompt:
                        field.fill(essay_prompt)
                        result_log["filled_fields"].append(f"essay: {key}")
                    else:
                        result_log["skipped_fields"].append(f"essay-failed: {key}")
                    continue
                else:
                    field.fill(value)
                    logger.debug(f"[autofill] ✅ Filled '{label.strip()}' as '{key}' with type '{input_type or tag_name}'")
                    result_log["filled_fields"].append(key)
            except Exception as e:
                logger.error(f"[autofill] ⚠️ Failed to handle field '{label.strip()}': {e}")
                result_log["errors"].append(f"{label.strip()} → {str(e)}")

                
                       
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
    
    
    def _is_essay_field(self, field) -> bool:
        try:
            maxlength = field.get_attribute("maxlength")
            rows = field.get_attribute("rows")
            cols = field.get_attribute("cols")
            
            return (
                (maxlength and int(maxlength) >= 200) or
                (rows and int(rows) >= 4) or 
                (cols and int(cols) >= 40)
            )
        except Exception as e:
            logger.warning(f"[essay-check] Failed to evaluate textarea heuristics: {e}")
            return False
            
    def generate_essay_response(self, label, appplication_data) -> Optional[str]:
        return ""