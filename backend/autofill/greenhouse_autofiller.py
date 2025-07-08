from backend.autofill.base_autofiller import BaseAutofiller
from backend.utils.logging import get_logger
from typing import Any

logger = get_logger(__name__)

class GreenhouseAutofiller(BaseAutofiller):
    def fill(self) -> dict[str, Any]:
        result_log= {
            "filled_fields": [],
            "skipped_fields": [],
            "uploaded_files": {},
            "errors": [],
            "clicked_submit": False,
            "confirmation_found": False
        }
        logger.info("[autofill] 🚦 Starting Greenhouse autofill...")

        for field, key in self._match_fields():
            tag = field.evaluate("el => el.tagName.toLowerCase()")
            field_type = field.get_attribute("type") or ""

            try:
                if tag == "select":
                    self._fill_select_field(field, key, result_log)

                elif tag == "textarea" or field_type == "text":
                    self._fill_text_field(field, key, result_log)

                elif field_type == "file":
                    logger.debug(f"[autofill] 📂 Skipping file input '{key}' in generic loop")

                else:
                    logger.warning(f"[autofill] 🤷‍♂️ Unknown field type: tag={tag}, type={field_type}")

            except Exception as e:
                logger.error(f"[autofill] ❌ Failed to fill '{key}': {e}")

        # File uploads — handled explicitly
        if (resume := self.application_data.get("resume_path")):
            self._upload_file_field("resume", resume, result_log)
        if (cover := self.application_data.get("cover_letter_path")):
            self._upload_file_field("cover_letter", cover, result_log)

        # Voluntary self-identification fields
        # self._fill_voluntary_demographics()

        # Handle multi-step “Next” buttons until final page
        while self._click_next_if_available():
            pass

        self._submit_application()
        return result_log

    def _fill_text_field(self, field: Any, key: str, result_log: dict[str, Any]):
        value = self.application_data.get(key)
        if not value:
            logger.debug(f"[autofill] ⚠️ No value for text field '{key}'")
            return
        if not self.dry_run:
            field.fill(value)
        logger.info(f"[autofill] 📝 Filled '{key}' with '{value}'")
        result_log[key] = "filled"

    def _fill_select_field(self, field: Any, key: str, result_log: dict[str, Any]):
        value = self.application_data.get(key)
        if not value:
            logger.debug(f"[autofill] ⚠️ No value for select field '{key}'")
            return
        if not self.dry_run:
            field.select_option(label=value)
        logger.info(f"[autofill] ✅ Selected '{value}' for '{key}'")
        result_log[key] = "selected"

    def _upload_file_field(self, data_key: str, path: str, result_log: dict[str, Any]):
        file_input = (
            self.page.query_selector(f"input[type='file'][name='{data_key}']")
            or self.page.query_selector(f"input[type='file'][id*='{data_key}']")
        )
        if file_input:
            if not self.dry_run:
                file_input.set_input_files(path)
            logger.info(f"[Greenhouse] Uploaded {data_key} from {path}")
            result_log[data_key] = "uploaded"
        else:
            logger.warning(f"[Greenhouse] File input for {data_key} not found")

    # def _fill_voluntary_demographics(self):
    #     voluntary_fields = {
    #         "gender": "gender",
    #         "race": "race",
    #         "disability_status": "disability_status",
    #         "veteran_status": "veteran_status",
    #     }

    #     for field_name, key in voluntary_fields.items():
    #         value = self.application_data.get(key)
    #         if not value:
    #             logger.debug(f"[Greenhouse] No value for voluntary field '{key}'")
    #             continue

    #         selector = f"select[name='{field_name}']"
    #         select_elem = self.page.query_selector(selector)
    #         if select_elem:
    #             if not self.dry_run:
    #                 select_elem.select_option(label=value)
    #             logger.info(f"[Greenhouse] Selected {field_name}: {value}")
    #             self.result_log[key] = "selected"
    #         else:
    #             logger.warning(f"[Greenhouse] Could not find selector for '{field_name}'")
