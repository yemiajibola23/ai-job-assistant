from backend.utils.logging import get_logger
from typing import Any

logger = get_logger(__name__)
class BaseAutofiller:
    def __init__(self, page: Any, application_data: dict[str, Any], result_log: dict[str, Any], dry_run: bool=True) -> None:
        self.page = page
        self.application_data = application_data
        self.result_log = result_log
        self.dry_run = dry_run
    
    def fill(self):
        raise NotImplementedError("Subclasses must implement fill().")

    def _upload_resume(self, resume_path: str) -> None:
        raise NotImplementedError("Subclasses must implement resume upload logic.")

    def _upload_cover_letter(self, cover_letter_path: str) -> None:
        raise NotImplementedError("Subclasses must implement cover letter upload logic.")

    
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