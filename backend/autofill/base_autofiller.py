from backend.utils.logging import get_logger
from typing import Any, Optional
from backend.autofill.field_matcher import FieldMatcher

logger = get_logger(__name__)
class BaseAutofiller:
    def __init__(self, page: Any, application_data: dict[str, Any], dry_run: bool=True) -> None:
        self.page = page
        self.application_data = application_data
        self.dry_run = dry_run
        self.field_matcher = FieldMatcher()
            
    def fill(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement fill().")

    def _upload_file_field(self, key: str, path: str, result_log: dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement resume upload logic.")

    def _submit_application(self) -> bool:
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
                button = self.page.query_selector(selector)
                if button:
                    if self.dry_run:
                        logger.info(f"[autofill] 🧪 Dry run: found submit button '{selector}' but not clicking.")
                        return False
                    button.click()
                    logger.info(f"[autofill] ✅ Clicked submit button '{selector}'")
                    return True
            except Exception as e:
                logger.debug(f"[autofill] ❌ Error searching for submit button with selector {selector}: {e}")

        logger.warning("[autofill] 🚫 No submit button found")
        return False
    
    def _click_next_if_available(self) -> bool:
        try:
            next_button = self.page.query_selector("button:text('Next'), button:text('Continue'), button:text('→')")
            
            if next_button:
                logger.debug("[multistep] ⏭ Clicking next/continue button")
                next_button.click()
                self.page.wait_for_timeout(10000)
                return True
        except Exception as e:
            logger.error(f"[multistep] ⚠️ Failed to click next: {e}")
        
        return False
    
    def _match_fields(self) -> list[tuple[Any, str]]:
        fields = self.page.query_selector_all("input, textarea, select")
        matched_fields = []
        for field in fields:
            label = self._extract_label(field)
            if not label:
                logger.debug("[field-match] ❌ No label found for field")
                continue
            
            logger.debug(f"[field-match] 🔎 Found label: '{label}'")
            
            key = self.field_matcher.match(label)
            if key:
                logger.info(f"[field-match] ✅ Matched '{label}' → '{key}'")
                matched_fields.append((field, key))
            else:
                logger.debug(f"[field-match] 🚫 No match for label '{label}'")
        return matched_fields
    
    def _extract_label(self, field: Any) -> Optional[str]:
        field_id = field.get_attribute("id")
        if field_id:
            label_elem = self.page.query_selector(f"label[for='{field_id}']")
            if label_elem:
                label_text = label_elem.inner_text().strip()
                logger.debug(f"[label-extract] 🏷 Found 'for' label: {label_text}")
                return label_text

        # fallback: look for closest preceding <label>
        label_handle = field.evaluate_handle("el => el.closest('label') || el.parentElement?.querySelector('label')")
        label_elem = label_handle.as_element()
        
        if label_elem:
            label_text = label_elem.inner_text().strip()
            logger.debug(f"[label-extract] 🪝 Found fallback label: {label_text}")
            return label_text
        
        logger.debug("[label-extract] ❌ No label found")
        return None
    
    def _check_for_submission_confirmation(self) -> bool:
        possible_texts = ["Thank you", "Application submitted", "We received", "Your application"]
        for text in possible_texts:
            if self.page.query_selector(f"text=/{text}/i"):
                return True
        return False
