from backend.autofill.base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any, Literal
import logging
from backend.autofill.xpath_utils import try_fill_by_id, get_labeled_field_xpath
from pathlib import Path
from backend.autofill.field_matcher_config import LABEL_KEY_MAP, VALUE_NORMALIZATION

logger = logging.getLogger(__name__)

RESUME_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[5]/div/div[2]/div/div[1]/div/button'
COVER_LETTER_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[6]/div/div[2]/div/div[1]/div/button'
BASIC_INFO_FIELDS = ["name", "first_name", "last_name", "email", "phone", "location"]

class GreenhouseAutofiller(BaseAutofiller):
    async def fill_basic_info(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        logger.info("🧾 Filling basic info...")
        
        for field in BASIC_INFO_FIELDS:
            if field == "name":
                if "first_name" in data and "last_name" in data:
                    value = f"{data['first_name']} {data['last_name']}"
                    logger.info(f"🔍 Attempting to fill full name using: {value}")

                    for full_name_id in ["name", "full_name", "candidate_name"]:
                        try:
                            await page.fill(f'xpath=//*[@id="{full_name_id}"]', value)
                            logger.info(f"✅ Filled full name field '{full_name_id}' with value: {value}")
                            result_log["filled_fields"].append("name")
                            break
                        except Exception as e:
                            logger.debug(f"🕳️ Could not fill '{full_name_id}' as full name field: {e}")
                continue  # Skip to next field after attempting full name
            else:
                logger.warning("⚠️ Could not locate a suitable full name field. Skipping 'name'.")
                result_log["skipped_fields"].append("name")
            
            value = data.get(field)
            if not value:
                logger.warning(f"⚠️ No data found for {field}. Skipping.")
                result_log["skipped_fields"].append(field)
                continue

            await try_fill_by_id(page, field, value, result_log)
        
                       
          
             #//*[@id="first_name-label"]
             #//*[@id="first_name"]
             
             #//*[@id="email-label"]
             
             #//*[@id="question_12382250004-label"]
             #//*[@id="question_12382250004"]
             
            #  //*[@id="question_12382258004-label"]
            # //*[@id="question_12382258004"]
            
            # //*[@id="question_12382257004"]
            
            # //*[@id="question_12382252004"]
            
            #//*[@id="upload-label-resume"]
            # //*[@id="application-form"]/div[1]/div[5]/div/div[2]/div/div[1]/div/button
            
            #//*[@id="upload-label-cover_letter"] 
            # //*[@id="application-form"]/div[1]/div[6]/div/div[2]/div/div[1]/div/button
            
            # //*[@id="gender-label"]
            # //*[@id="application-form"]/div[3]/div[3]/div/div/div/div/div
            
            
    async def upload_file(self, page: Page, field_key: str, data: Dict[str, Any], xpath: str, result_log: Dict[str, Any]):
        file_path = data.get(f"{field_key}_path")
        
        if not file_path or not Path(file_path).exists():
            logger.warning(f"⚠️ No valid {field_key} path provided. Skipping {field_key} upload.")
            result_log["skipped_fields"].append(field_key)
            return
        
        try:
            await page.set_input_files(f"input#{field_key}", file_path)
            logger.info(f"📄 Uploaded {field_key} using direct file input: {file_path}")
            result_log["filled_fields"].append(field_key)
            result_log["uploaded_files"][field_key] = file_path
            return 
        except Exception as e1:
            logger.warning(f"❌ Direct {field_key} upload failed: {e1}")
            
        
        try:
            # Fallback: Click the upload button
            upload_button_xpath = xpath
            await page.click(f"xpath={upload_button_xpath}")
            # Wait and retry input after modal/dialog appears
            await page.set_input_files('input[type="file"]', file_path)
            logger.info(f"📄 Uploaded {field_key} using fallback file dialog method: {file_path}")
            result_log["uploaded_files"][field_key] = file_path
        except Exception as e2:
            logger.error(f"❌ {field_key} upload failed entirely: {e2}")
            result_log["errors"].append({f"{field_key}": str(e2)})
            
    async def upload_documents(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        await self.upload_file(page, "resume", data, RESUME_UPLOAD_BUTTON_XPATH, result_log)
        await self.upload_file(page, "cover_letter", data, COVER_LETTER_UPLOAD_BUTTON_XPATH, result_log)    
    
    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        fields = ["gender", "veteran_status", "disability_status", "hispanic_ethnicity"]
        
        for field in fields:
            raw_value = data.get(field)
            if not raw_value:
                logger.warning(f"⚠️ No value provided for {field}. Skipping.")
                result_log["skipped_fields"].append(field)
                continue
            
            value = VALUE_NORMALIZATION.get(field, {}).get(raw_value.lower(), raw_value)
            if not value:
                logger.warning(f"⚠️ Normalized value for {field} is empty. Skipping.")
                result_log["skipped_fields"].append(field)
                continue

            success = await try_fill_by_id(page, field, value, result_log)
            if success:
                continue  # ✅ done
            
            # 🪂 Fallback using label-based XPath
            label_text = next(
                (label for label, canonical in LABEL_KEY_MAP.items() if canonical == field),
                field.replace("_", " ").title()
            )
            fallback_xpath = get_labeled_field_xpath(label_text, "input")
            
            if not fallback_xpath:
                logger.error(f"❌ No fallback XPath generated for {field}")
                result_log["errors"].append({field: "Missing fallback XPath"})
                continue
            
            try:
                await page.fill(f"xpath={fallback_xpath}", value)
                logger.info(f"✅ Fallback filled {field} using label '{label_text}'.")
                result_log["filled_fields"].append(field)
            except Exception as e:
                logger.error(f"❌ Fallback failed for {field}: {e}")
                result_log["errors"].append({field: str(e)})
        
    
    def classify_question_type(self, label_text: str, input_tag: str) -> Literal["basic", "essay", "dropdown"]:
        if "why" in label_text.lower() or "describe" in label_text.lower() or input_tag == "textarea":
            return "essay"
        elif label_text.strip().lower() in LABEL_KEY_MAP:
            return "basic"
        else:
            return "dropdown"


    async def fill_custom_questions(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        label_elements = await page.query_selector_all("xpath=//*[starts-with(@id, 'question_') and contains(@id, '-label')]")

        for label in label_elements:
            label_text = ""
            try:
                label_id = await label.get_attribute("id")
                if not label_id or not label_id.endswith("-label"):
                    continue

                field_id = label_id.replace("-label", "")
                label_text = (await label.inner_text()).strip()

                # Find input type by tag name
                input_element = await page.query_selector(f'xpath=//*[@id="{field_id}"]')
                if not input_element:
                    logger.warning(f"⚠️ Could not find input field for {field_id}. Skipping.")
                    result_log["skipped_fields"].append(field_id)
                    continue
                
                tag_name = await input_element.evaluate("el => el.tagName.toLowerCase()")

                # Dispatch
                if "why" in label_text.lower() or "describe" in label_text.lower() or tag_name == "textarea":
                    await self.handle_essay_custom_question(page, label_text, field_id, result_log)
                elif label_text.strip().lower() in LABEL_KEY_MAP:
                    await self.handle_basic_custom_question(page, label_text, field_id, data, result_log)
                else:
                    await self.handle_dropdown_custom_question(page, label_text, field_id, data, result_log)

            except Exception as e:
                logger.error(f"❌ Error classifying custom question '{label_text}': {e}")
                result_log["errors"].append({label_text: str(e)})


    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    async def handle_basic_custom_question(self, page: Page, label_text: str, field_id: str, data: Dict[str, Any], result_log: Dict[str, Any]):
        key = LABEL_KEY_MAP.get(label_text.strip().lower())
        if not key:
            logger.warning(f"⚠️ No canonical key found for label '{label_text}'. Skipping.")
            result_log["skipped_fields"].append(label_text.strip())
            return

        value = data.get(key)
        if not value:
            logger.warning(f"⚠️ No value provided for key '{key}' (from label '{label_text}'). Skipping.")
            result_log["skipped_fields"].append(key)
            return

        success = await try_fill_by_id(page, field_id, value, result_log)
        if success:
            result_log["filled_fields"].append(key)
            return

        # fallback
        fallback_xpath = get_labeled_field_xpath(label_text, "input")
        try:
            await page.fill(f"xpath={fallback_xpath}", value)
            logger.info(f"✅ Fallback filled basic question '{label_text}' with value: {value}")
            result_log["filled_fields"].append(key)
        except Exception as e:
            logger.error(f"❌ Fallback failed for basic question '{label_text}': {e}")
            result_log["errors"].append({key: str(e)})

    async def handle_dropdown_custom_question(self, page: Page, label_text: str, field_id: str, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def handle_essay_custom_question( self, page: Page, label_text: str, field_id: str, result_log: Dict[str, Any]):
        pass
