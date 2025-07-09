from backend.autofill.base_autofiller import BaseAutofiller
from backend.utils.logging import get_logger
from typing import Any, Optional
from backend.autofill.xpath_utils import get_labeled_field_xpath, resolve_greenhouse_field_xpath
import json

logger = get_logger(__name__)

class GreenhouseAutofiller(BaseAutofiller):
    def fill(self) -> dict[str, Any]:
        logger.info("[autofill] 🚦 Starting Greenhouse autofill...")
        print("\n=== Application Data ===")
        print(json.dumps(self.application_data, indent=2))
        print("========================\n")

        result_log = {
            "filled_fields": [],
            "skipped_fields": [],
            "uploaded_files": {},
            "errors": [],
            "clicked_submit": False,
            "confirmation_found": False
        }

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

        labels = self.page.query_selector_all("label")
        logger.debug(f"[autofill] 🏷️ Found {len(labels)} labels on the page")

        for label in labels:
            label_text = label.inner_text().strip()
            if not label_text:
                continue

            logger.debug(f"[autofill] 🔍 Found label: '{label_text}'")
            key, strategy = self.field_matcher.match(label_text, debug=True)
            if not key or key not in self.application_data:
                continue

            value = self.application_data[key]
            logger.debug(f"[autofill] 🧠 Matched label '{label_text}' → key: '{key}'")
            logger.debug(f"[autofill] 📌 Using value '{value}' for key '{key}'")

            field_type = "select" if key == "location" else "input"
            filled = self._fill_field_by_xpath(label_text, value, field_type)
            if filled:
                result_log["filled_fields"].append(key)
            else:
                result_log["skipped_fields"].append(key)

        return result_log
    
    def _fill_field_by_xpath(self, label_text: str, value: str, field_type: str = "input") -> bool:
        """
        Fills a form field identified by its label using XPath. Supports fallback for React-style select fields.
        """
        alt_xpath = resolve_greenhouse_field_xpath(self.page, label_text, field_type)
        locator = None

        if alt_xpath:
            logger.debug(f"[xpath-fill] 🧭 Using Greenhouse ID XPath: {alt_xpath}")
            locator = self.page.locator(f"xpath={alt_xpath}")
        else:
            xpath = get_labeled_field_xpath(label_text, field_type)
            logger.debug(f"[xpath-fill] 🧭 Generated XPath for '{label_text}' ({field_type}): {xpath}")
            locator = self.page.locator(f"xpath={xpath}")

        try:
            if locator.count() == 0:
                # 🛠️ React Select Fallback
                if field_type == "select":
                    logger.debug("[xpath-fill] 🛠️ Trying React Select fallback for dropdown...")
                    react_dropdowns = self.page.locator(".select__input")
                    if react_dropdowns.count() > 0:
                        react_dropdowns.first.click()
                        self.page.keyboard.type(value)
                        self.page.keyboard.press("Enter")
                        logger.info(f"[xpath-fill] ✅ Filled React dropdown '{label_text}' with '{value}'")
                        return True

                logger.warning(f"[xpath-fill] 🚫 No field found for label '{label_text}'")
                return False

            if field_type == "select":
                locator.first.select_option(value)
            else:
                locator.first.fill(value)

            logger.info(f"[xpath-fill] ✅ Filled '{label_text}' with '{value}' using {field_type}")
            return True

        except Exception as e:
            logger.error(f"[xpath-fill] ❌ Failed to fill field for label '{label_text}': {e}")
            return False

    def _fill_text_field(self, field: Any, key: str, result_log: dict[str, Any]):
        value = self.application_data.get(key)
        
        if key == "name":
            label_text_raw = self._extract_label(field)
            label_text = label_text_raw.lower() if label_text_raw else ""
            full_name = self.application_data.get("name") or ""
            if not full_name:
                logger.debug("[autofill] ⚠️ Cannot disambiguate 'name' – no full name in data")
                result_log["skipped_fields"].append("name")
                return
            
            parts = full_name.strip().split()
            if "first" in label_text:
                if parts:
                    value = parts[0]
                    key = "first_name"
                else:
                    result_log["skipped_fields"].append("first_name")
                    return
                
            elif "last" in label_text:
                if len(parts) > 1:
                    value = parts[1]
                    key = "last_name"
                else:
                    result_log["skipped_fields"].append("last_name")
                    return
        if not value:
            logger.debug(f"[autofill] ⚠️ No value for text field '{key}'")
            if not key in result_log["skipped_fields"]:
                result_log["skipped_fields"].append(key)
            return
        try:
            field.fill(value)
            logger.info(f"[autofill] 📝 Filled '{key}' with '{value}'")
            result_log["filled_fields"].append(key)
        except Exception as e:
            logger.error(f"[autofill] ❌ Failed to fill '{key}': {e}")
            result_log["errors"].append(f"{key}: {str(e)}")

    def _upload_file_field(self, key: str, path: Optional[str], result_log: dict[str, Any]):
        if not path:
            logger.warning(f"[autofill] ⚠️ No file path provided for '{key}'")
            if key not in result_log["skipped_fields"]:
                result_log["skipped_fields"].append(key)
            return
        file_input = (
            self.page.query_selector(f"input[type='file'][name='{key}']")
            or self.page.query_selector(f"input[type='file'][id*='{key}']")
        )
        if file_input:
            try:
                file_input.set_input_files(path)
                logger.info(f"[Greenhouse] Uploaded {key} from {path}")
                result_log["uploaded_files"][key] = [path]
                result_log["filled_fields"].append(key)
            except Exception as e:
               logger.warning(f"[Greenhouse] ❌ Upload failed for {key}: {e}")
               result_log["errors"].append(f"{key}: {str(e)}")
        else:
            logger.warning(f"[Greenhouse] File input for {key} not found")
            result_log["skipped_fields"].append(key)
    
    def _match_fields(self) -> list[tuple[Any, str, str]]:
        input_fields = self.page.query_selector_all("input, textarea, select")
        xpath = "//div[.//label and .//div[contains(@class, 'select__control')]]"
        dropdown_containers = self.page.query_selector_all(xpath)
        logger.debug(f"[field-match] 🧪 Found {len(dropdown_containers)} potential dropdown containers")

        matched_fields = []
        for field in input_fields:
            label = self._extract_label(field)
            if not label:
                logger.debug("[field-match] ❌ No label found for field")
                continue
            
            logger.debug(f"[field-match] 🔎 Found label: '{label}'")
            
            key = self.field_matcher.match(label)
            if key and key in self.application_data:
                logger.info(f"[field-match] ✅ Matched '{label}' → '{key}'")
                matched_fields.append((field, key, "text"))
            
        for container in dropdown_containers:
            input_elem = container.query_selector("input")
            field_id = input_elem.get_attribute("id") if input_elem else None
            aria_controls = input_elem.get_attribute("aria-controls")
            if not field_id:
                continue
                
            label_elem = container.query_selector("label")
            label_text = label_elem.inner_text().strip() if label_elem else None
            if not label_text:
                    continue
            
            logger.debug(f"[field-match] 🔎 Found dropdown label: '{label_text}'")
            logger.debug(f"[dropdown-xpath] Label found: '{label_text}' for container {container}")

            key = self.field_matcher.match(label_text)
            if key and key in self.application_data:
                logger.info(f"[field-match] ✅ Matched dropdown '{label_text}' → '{key}'")
                matched_fields.append((container, key, "dropdown"))
                
        logger.info(f"[field-match] Matched {len(matched_fields)} total fields: "
            f"{sum(1 for _, _, t in matched_fields if t == 'text')} text, "
            f"{sum(1 for _, _, t in matched_fields if t == 'dropdown')} dropdown")
            
        return matched_fields
    
    
    def _fill_custom_dropdown_field(self, container: Any, key: str, result_log: dict[str, Any]):
        value = self.application_data.get(key)
        if not value:
            logger.debug(f"[autofill] ⚠️ No value for dropdown field '{key}'")
            result_log["skipped_fields"].append(key)
            return

        try:
            if not self.dry_run:
                container.click()  # Open dropdown
                self.page.wait_for_selector("div.select__menu", timeout=3000)
                options = self.page.query_selector_all("div.select__menu div")

                normalized_value = value.lower().strip()
                matched = False

                for option in options:
                    option_text = option.inner_text().strip().lower()
                    if normalized_value in option_text:
                        option.click()
                        matched = True
                        break

                if matched:
                    logger.info(f"[autofill] ✅ Selected '{value}' for '{key}'")
                    result_log["filled_fields"].append(key)
                else:
                    available_options = [option.inner_text().strip() for option in options]
                    logger.warning(
                        f"[autofill] ⚠️ No matching dropdown option for '{key}': '{value}'\n"
                        f"[autofill]    Available options: {available_options}"
                    )
                    result_log["skipped_fields"].append(key)

            else:
                logger.info(f"[autofill] 🧪 Dry run: would select '{value}' for '{key}'")
                result_log["filled_fields"].append(key)

        except Exception as e:
            logger.error(f"[autofill] ❌ Failed to fill dropdown '{key}': {e}")
            result_log["errors"].append(f"{key}: {str(e)}")