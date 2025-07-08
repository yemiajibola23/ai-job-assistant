from playwright.sync_api import sync_playwright
from backend.autofill.field_matcher import match_label_to_key
from typing import Optional, Any
import os
from backend.utils.logging import get_logger
from pathlib import Path
import json
from backend.generation.generators.essay_generator import EssayResponseGenerator
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

    def _click_submit_if_available(self, dry_run: bool, page: Any) -> bool:
        submit_selectors = [
            "button[type=submit]",
            "button:has-text('Submit')",
            "button:has-text('Apply')",
            "button:has-text('Review and Submit')",
            "input[type=submit]",
            "button[aria-label='Submit']",
        ]
        
        for selector in submit_selectors:
            try:
                button = page.query_selector(selector)
                if button:
                    if dry_run:
                        logger.info(f"[autofill] 🧪 Dry run: found submit button '{selector}' but not clicking.")
                        return False
                    button.click()
                    logger.info(f"[autofill] ✅ Clicked submit button '{selector}'")
                    return True
            except Exception as e:
                logger.debug(f"[autofill] ❌ Error searching for submit button with selector {selector}: {e}")

        logger.warning("[autofill] 🚫 No submit button found")
        return False
    
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
        
        
    def fill_form(self, application_data: dict, page: Optional[Any]=None, dry_run: bool=True) -> dict:
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
                
                clicked = self._click_submit_if_available(dry_run, page)
                result_log["clicked_submit"] = clicked
                
                page.wait_for_timeout(3000)
                result_log["confirmation_found"] = self._check_for_submission_confirmation(page)
        else:
            self._fill_multistep_form(page, application_data, result_log)
        
        logger.info(f"[autofill] 🧾 Autofill Result Log: {json.dumps(result_log, indent=2)}")

        return result_log
    
    def _extract_essay_fields(self, page) -> dict[str, Any]:
        for_labels = page.query_selector_all("label[for]")
        essay_fields: dict[str, Any] = {}
        for label in for_labels:
            try:
                label_text = label.inner_text().strip()
                for_attr = label.get_attribute("for")
                if not for_attr or not label_text:
                    continue
                field = page.query_selector(f"#{for_attr}")
                if field:
                    input_type = (field.get_attribute("type") or "").lower()
                    tag_name = field.evaluate("el => el.tagName.toLowerCase()")
                    
                    # Skip small fields
                    if tag_name == "input" and input_type in {"checkbox", "radio", "file", "email", "tel", "number"}:
                        continue
                    if tag_name == "select":
                        continue
                    
                    essay_fields[label_text] = field
                    
            except Exception as e:
                logger.warning(f"[essay-detect] Failed to process label: {e}")
            
        return essay_fields
    
    def _fill_fields(self, page: Any, application_data: dict, result_log: dict) -> None:
        fields = page.query_selector_all("input, textarea, [contenteditable=true], div[role='textbox'], .form-field, .form-control")
        logger.debug(f"[autofill] 🧪 Found {len(fields)} fields to scan")
        
        for field in fields:
            label = self.extract_field_label(field, page)
            label_text = (label or "").strip()
            tag_name = field.evaluate("el => el.tagName.toLowerCase()")
            input_type = (field.get_attribute("type") or "").strip()

            if not label:
                logger.warning("No label found for field")
                result_log["skipped_fields"].append("unlabeled: unknown field")
                continue

            logger.debug(f"[field-scan] tag={tag_name}, label={label_text}")
            
            if self._handle_attach_label(page, label_text, application_data, result_log):
                continue

            key = match_label_to_key(label, debug=True)
            value = application_data.get(key)

            if not key:
                # Fallback: treat as essay if essay-like
                if self._is_essay_field(field, label_text):
                    self._handle_essay_field(field, label_text, application_data, result_log)
                    continue

                logger.warning(f"[matcher] ❌ Unrecognized label → '{label_text}'")
                result_log["skipped_fields"].append(f"unmatched: {label_text}")
                continue
            

            # Special case: intelligently split name
            if not value and key == "name" and "name" in application_data:
                full_name = application_data["name"]
                name_parts = full_name.split()
                if "first" in label_text.lower() and name_parts:
                    value = name_parts[0]
                elif "last" in label_text.lower() and len(name_parts) > 1:
                    value = name_parts[-1]

            if not value:
                logger.warning(f"[matcher] ⚠️ No resume value found for key: '{key}' (matched from '{label_text}')")
                result_log["skipped_fields"].append(key)
                continue

            if input_type == "file":
                self._handle_file_field(field, value, label_text, key, result_log)
            else:
                self._handle_general_field(field, tag_name, input_type, value, label_text, key, result_log)

    def _handle_essay_field(self, field, label_text, application_data, result_log):
        essay_prompt = self.generate_essay_response(label_text, application_data)
        if essay_prompt:
            field.fill(essay_prompt)
            logger.debug(f"[essay-generation] ✅ Filled essay: {essay_prompt}")
            result_log["filled_fields"].append(f"essay: {label_text}")
        else:
            logger.warning(f"[essay-fill] ❌ Failed to generate essay for: '{label_text}'")
            result_log["skipped_fields"].append(f"essay-failed: {label_text}")
    
    def _handle_file_field(self, field, value, label_text, key, result_log):
        if not os.path.isfile(value):
            logger.warning(f"[autofill] ❌ File not found: {value}")
            return
        field.set_input_files(value)
        logger.debug(f"[autofill] ✅ Uploaded file for '{label_text}' as '{key}'")
        result_log["uploaded_files"][key] = [value]
        result_log["filled_fields"].append(key)

        if "resume" in label_text.lower():
            self.uploaded_resume_path = value
        elif "cover" in label_text.lower():
            self.uploaded_cover_letter_path = value
    
        return True
    
    def _handle_attach_label(self, page, label_text: str, application_data: dict, result_log: dict) -> bool:
        ATTACH_LABEL_KEYWORDS = [
            "attach", "upload", "drop your resume", "select file", "upload your resume", "choose file"
        ]
        label_text = label_text.lower().strip()

        if not any(keyword in label_text for keyword in ATTACH_LABEL_KEYWORDS):
            return False

        key = "cover_letter" if "cover" in label_text else "resume"
        file_path = application_data.get(key) or getattr(self, f"uploaded_{key}_path", None)

        if not file_path or not os.path.isfile(file_path):
            logger.warning(f"[autofill] ⚠️ {key.title()} file not found for attach label: '{label_text}'")
            result_log["skipped_fields"].append(f"attach-missing: {label_text}")
            return True  # Avoid reprocessing

        try:
            label_el = page.query_selector(f"label:text('{label_text}')")
            file_input = label_el.evaluate_handle("el => document.getElementById(el.getAttribute('for'))") if label_el else None

            if file_input:
                file_input.set_input_files(file_path)
                logger.debug(f"[autofill] ✅ Uploaded {key} via attach label: '{label_text}'")
                result_log["uploaded_files"][key] = [file_path]
                result_log["filled_fields"].append(key)
                setattr(self, f"uploaded_{key}_path", file_path)
                return True
            else:
                logger.warning(f"[autofill] ❌ Could not find file input for attach label '{label_text}'")
                result_log["skipped_fields"].append(f"attach-failed: {label_text}")
                return True
        except Exception as e:
            logger.error(f"[autofill] ❌ Failed to attach {key} for '{label_text}': {e}")
            result_log["errors"].append(f"{label_text} → {str(e)}")
            return True

        
    
    def _handle_general_field(self, field, tag_name, input_type, value, label_text, key, result_log):
        try:
            if tag_name == "select":
                logger.debug(f"[general] ⏳ Handling <select> for '{label_text}'")
                field.select_option(value)
                logger.debug(f"[autofill] ✅ Selected option for '{label_text}' as '{key}'")
            elif input_type == "radio":
                logger.debug(f"[general] ⏳ Handling radio for '{label_text}'")
                radio_value = field.evaluate("el => el.value")
                if radio_value == value:
                    field.check()
                    logger.debug(f"[autofill] ✅ Checked radio for '{label_text}' as '{key}'")
            else:
                logger.debug(f"[general] ⏳ Handling text input for '{label_text}'")
                field.fill(value)
                logger.debug(f"[autofill] ✅ Filled '{label_text}' as '{key}' with type '{input_type or tag_name}'")

            result_log["filled_fields"].append(key)
        except Exception as e:
            logger.error(f"[general] ⚠️ Failed to fill general field '{label_text}': {e}")
            result_log["errors"].append(f"{label_text} → {str(e)}")

    def extract_field_label(self, field, page):
        try: 
            id_attr = field.get_attribute("id")
            if id_attr:
                label_element = page.query_selector(f"label[for='{id_attr}']")
                if label_element:
                    return label_element.inner_text().strip()
            
            aria = field.get_attribute("aria-label")
            if aria:
                return aria.strip()
            
            placeholder = field.get_attribute("placeholder")
            if placeholder:
                return placeholder.strip()
            
            return (field.evaluate("node => node.parentElement?.innerText") or "").strip()
    
        except Exception as e:
            logger.error(e)
    
    def _is_essay_field(self, field, label_text:str) -> bool:
        tag_name = field.evaluate("el => el.tagName.toLowerCase()")
        input_type = (field.get_attribute("type") or "").lower()
        label_text = (label_text or "").strip().lower()
        
        logger.debug(f"[essay-check] Normalized label text = '{label_text}'")
        
        if tag_name == "select" or input_type in {"checkbox", "radio"}:
            logger.debug(f"[essay-check] ⛔ Excluded due to input type: {tag_name} / {input_type}")
            return False
        
        NON_ESSAY_TERMS = {
            "gender", "race", "ethnicity", "location", "veteran",
            "disability", "pronouns", "status", "hispanic", "latino"
        }

        logger.debug(f"[essay-check] Comparing against: {NON_ESSAY_TERMS}")

        try:
            label_text = (label_text or "").strip().lower().replace("?", "").replace("*", "")
            tokens = set(label_text.split())

            logger.debug(f"[essay-check] Tokens = {tokens}, Checking intersection with: {NON_ESSAY_TERMS}")
            logger.debug(f"[essay-check] Raw label_text passed in: {label_text}")

            if tokens & set(NON_ESSAY_TERMS):
                logger.debug(f"[essay-check] ⛔ Excluded due to token match: {tokens & set(NON_ESSAY_TERMS)} in label '{label_text}'")
                return False

            if any(keyword in label_text for keyword in ["why", "tell us", "describe", "motivate", "goals"]):
                logger.debug(f"[essay-check] ✅ Label keyword match: '{label_text}'")
                return True

            maxlength = field.get_attribute("maxlength")
            rows = field.get_attribute("rows")
            cols = field.get_attribute("cols")

            logger.debug(f"[essay-check] Checking structural heuristics → maxlength={maxlength}, rows={rows}, cols={cols}")

            return (
                (maxlength and int(maxlength) >= 200) or
                (rows and int(rows) >= 4) or 
                (cols and int(cols) >= 40)
            )
        except Exception as e:
            logger.warning(f"[essay-check] ⚠️ Failed to evaluate textarea heuristics: {e}")
            return False
            
    def generate_essay_response(self, label, application_data) -> Optional[str]:
        try:
            data = application_data.copy()
            data["label"] = label
            
            # Ensure required keys for prompt
            data.setdefault("job_title", application_data.get("job_title", "iOS Engineer"))
            data.setdefault("company", application_data.get("company", "the company"))
            data.setdefault("summary", application_data.get("summary", "Experienced iOS engineer with a strong background in Swift and building scalable mobile apps."))
            
            generator = EssayResponseGenerator()
            return  generator.generate(data)
        except Exception as e:
            logger.error(f"[essay-generation] GPT failed: {e}")
            return None
    def handle_voluntary_demographics(self, label: str) -> Optional[str]:
        keywords = {"gender", "veteran", "disability", "ethnicity", "race", "hispanic", "latino"}
        if any(word in label.lower() for word in keywords):
            logger.debug(f"[voluntary] 🚫 Skipping voluntary demographic field: '{label}'")
            return "skip"
        return None
