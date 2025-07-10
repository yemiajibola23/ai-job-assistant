from backend.autofill.base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any
import logging
from backend.autofill.xpath_utils import try_fill_by_id, get_labeled_field_xpath
from pathlib import Path
from backend.autofill.field_matcher_config import LABEL_KEY_MAP, VALUE_NORMALIZATION

logger = logging.getLogger(__name__)

RESUME_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[5]/div/div[2]/div/div[1]/div/button'
COVER_LETTER_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[6]/div/div[2]/div/div[1]/div/button'
class GreenhouseAutofiller(BaseAutofiller):
    async def fill_basic_info(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        fields = ["first_name", "last_name", "phone", "email"]
        
        for field in fields:
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
        
        

    async def fill_custom_questions(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
