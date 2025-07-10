from backend.autofill.base_autofiller import BaseAutofiller
from backend.utils.logging import get_logger
from typing import Any, Optional
from backend.autofill.xpath_utils import get_labeled_field_xpath, resolve_greenhouse_field_xpath
from backend.autofill.field_matcher_config import VALUE_NORMALIZATION
from backend.autofill.field_matcher import match_label_to_key
import json

logger = get_logger(__name__)

class GreenhouseAutofiller(BaseAutofiller):
    def fill(self) -> dict[str, Any]:
        logger.info("[autofill] 🚦 Starting Greenhouse autofill...")
        print("\n=== Application Data ===")
        print(json.dumps(self.application_data, indent=2))
        print("========================\n")

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
            if not key:
                logger.error(f"[autofill] ❌ Could not match label: '{label_text}'")
                self.result_log["errors"].append(f"Unmatched label: '{label_text}'")
                continue
            
            if key not in self.application_data:
                logger.debug(f"[autofill] ⚠️ Matched '{label_text}' → key '{key}', but no value provided in application_data. Skipping.")
                self.result_log["skipped_fields"].append(key)
                continue

            raw_value = self.application_data.get(key)
            value = raw_value
            if isinstance(raw_value, str):
                value = VALUE_NORMALIZATION.get(key, {}).get(raw_value.lower(), raw_value)
            
            
            logger.debug(f"[autofill] 🧠 Matched label '{label_text}' → key: '{key}'")
            logger.debug(f"[autofill] 📌 Using value '{value}' for key '{key}'")

            if not isinstance(value, str):
                self.result_log["skipped_fields"].append(key)
                continue
            
            field_type = "select" if key == "location" else "input"
            filled = self._fill_field_by_xpath(label_text, value, field_type)
            if filled:
                self.result_log["filled_fields"].append(key)
            else:
                self.result_log["skipped_fields"].append(key)

        return self.result_log
    
    def _select_react_dropdown_by_label_id(self, label_id: str, value: str) -> bool:
        field_id = label_id.removesuffix("-label")
        container_xpath = f'//*[@id="{field_id}"]'
        try:
            container = self.page.locator(f"xpath={container_xpath}")
            # Inside _select_react_dropdown_by_label_id
            logger.debug(container.inner_html())

            if container.count() == 0:
                self.result_log["skipped_fields"].append(field_id)
                logger.warning(f"[react-select] 🚫 No container found for label ID: {label_id}")
                return False

            dropdown_input = dropdown_input = container.locator("xpath=.//div[contains(@class, 'select__input') or contains(@class, 'select__control')]")
            logger.debug(f"[react-select] Found {dropdown_input.count()} dropdown inputs inside {container_xpath}")

            if dropdown_input.count() == 0:
                self.result_log["skipped_fields"].append(field_id)
                logger.warning(f"[react-select] 🚫 No dropdown input found inside: {container_xpath}")
                return False

            dropdown_input.first.click()
            self.page.wait_for_timeout(500)
            
            options = self.page.locator(".select__option")
            for i in range(options.count()):
                option = options.nth(i)
                option_text = option.inner_text().strip().lower()
                if option_text == value.strip().lower():
                    option.click()
                    logger.info(f"[react-select] ✅ Selected option '{option_text}' for label '{label_id}'")
                    self.result_log["filled_fields"].append(field_id)
                    return True
            
            logger.warning(f"[react-select] 🚫 No matching option found for '{value}'")
            self.result_log["skipped_fields"].append(field_id)
            return False
        except Exception as e:
            logger.error(f"[react-select] ❌ Failed to fill dropdown for '{label_id}': {e}")
            self.result_log["errors"].append(f"[react-select] {label_id}: {e}")
            return False
        
    def _fill_field_by_xpath(self, label_text: str, value: str, field_type: str = "input") -> bool:
        """
        Fills a form field identified by its label using XPath. Supports fallback for React-style select fields.
        The field_type is overridden internally for known select-style fields like demographic dropdowns.
        """
        # 🧠 Override field_type based on known keys
        key_override_map = {
            "location",
            "gender",
            "ethnicity",
            "veteran_status",
            "disability_status"
        }

        normalized_key = match_label_to_key(label_text)
        if normalized_key in key_override_map:
            field_type = "select"

        alt_xpath = resolve_greenhouse_field_xpath(self.page, label_text, field_type)
        locator = self.page.locator(f"xpath={alt_xpath}") if alt_xpath else self.page.locator(
            f"xpath={get_labeled_field_xpath(label_text, field_type)}"
        )

        try:
            if locator.count() == 0:
                # 🛠️ React Select Fallback
                if field_type == "select":
                    label_id = self._find_label_id_by_text(label_text)
                    if label_id:
                        return self._select_react_dropdown_by_label_id(label_id, value)

                logger.warning(f"[xpath-fill] 🚫 No field found for label '{label_text}'")
                return False

            if field_type == "select":
                locator.first.select_option(value)
            else:
                locator.first.fill(value)

            logger.info(f"[xpath-fill] ✅ Filled '{label_text}' with '{value}' via label → id")
            return True

        except Exception as e:
            self.result_log["errors"].append(f"{label_text}': {e}")
            logger.error(f"[xpath-fill] ❌ Failed to fill field for label '{label_text}': {e}")
            return False

    def _find_label_id_by_text(self, label_text: str) -> Optional[str]:
        """
        Finds the label element matching the given text and returns its 'id' attribute.
        """
        for label in self.page.query_selector_all("label"):
            if label.inner_text().strip() == label_text.strip():
                return label.get_attribute("id")
        return None

    
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
        except Exception as e:
            logger.error(f"[autofill] ❌ Failed to fill dropdown '{key}': {e}")
            result_log["errors"].append(f"{key}: {str(e)}")
            

    def _fill_fields(self) -> None:
        fields = self.page.query_selector_all("input, textarea, select")
    
        for field in fields:
            label_text = self._extract_label(field)
            if not label_text:
                continue
            
            key, strategy = self.field_matcher.match(label_text, debug=True)
            if not key:
                logger.warning(f"[autofill] ❌ Could not match label: '{label_text}'")
                self.result_log["unmatched_labels"].append(label_text)
                continue

            if key not in self.application_data:
                logger.info(f"[autofill] ⚠️ No value for matched key '{key}'")
                self.result_log["skipped_fields"].append(key)
                continue

            value = self.application_data[key]
            if not isinstance(value, str):
                logger.debug(f"[autofill] ⚠️ Skipping non-string value for key '{key}': {value}")
                self.result_log["skipped_fields"].append(key)
                continue
                
            success = self._fill_field_by_label(label_text, value)

            if success:
                self.result_log["filled_fields"].append(key)
            else:
                self.result_log["skipped_fields"].append(key)
    
    
    def _fill_field_by_label(self, label_text: str, value: str) -> bool:
        """
        Attempts to fill a form field using label[for] matching.
        Falls back to other strategies if label-for is missing or invalid.
        """
        try:
            labels = self.page.query_selector_all("label")
            for label in labels:
                label_inner = label.inner_text().strip()
                if label_inner.lower() != label_text.lower():
                    continue

                label_for = label.get_attribute("for")
                if label_for:
                    field = self.page.query_selector(f"#{label_for}")
                    if field:
                        tag = field.evaluate("el => el.tagName").lower()
                        if tag == "select":
                            field.select_option(value)
                        else:
                            field.fill(value)
                        logger.info(f"[label-fill] ✅ Filled '{label_text}' via #{label_for} with '{value}'")
                        return True
                    else:
                        logger.warning(f"[label-fill] 🚫 No field found for id '{label_for}'")

                # 🧪 Fallback: label wraps input/select/textarea
                fallback_field = label.query_selector("input, select, textarea")
                if fallback_field:
                    tag = fallback_field.evaluate("el => el.tagName").lower()
                    if tag == "select":
                        fallback_field.select_option(value)
                    else:
                        fallback_field.fill(value)
                    logger.info(f"[label-fill] ✅ Filled '{label_text}' via label-wrapped field")
                    return True
                
                # 🧱 Fallback: sibling field inside same container
                container_handle = label.evaluate_handle("el => el.parentElement")
                container = container_handle.as_element()
                if container:
                    sibling_field = container.query_selector("input, select, textarea")
                    if sibling_field:
                        tag = sibling_field.evaluate("el => el.tagName").lower()
                        if tag == "select":
                            sibling_field.select_option(value)
                        else:
                            sibling_field.fill(value)
                        logger.info(f"[label-fill] ✅ Filled '{label_text}' via sibling in container")
                        return True
                    
                # 🧪 Fallback: React-select dropdown via label id
                label_id = label.get_attribute("id")
                if label_id and label_id.endswith("-label"):
                    success = self._select_react_dropdown_by_label_id(label_id, value)
                    if success:
                        logger.info(f"[label-fill] ✅ Filled '{label_text}' via React-select fallback")
                        return True
                        
            logger.warning(f"[label-fill] 🚫 Could not match any label to '{label_text}'")
            return False

        except Exception as e:
            logger.error(f"[label-fill] ❌ Error filling '{label_text}': {e}")
            self.result_log["errors"].append(f"{label_text}: {e}")
            return False
