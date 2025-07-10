from backend.autofill.base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any
import logging
from backend.autofill.xpath_utils import try_fill_by_id
from pathlib import Path

logger = logging.getLogger(__name__)
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
        await self.upload_file(page, "resume", data, '//*[@id="application-form"]/div[1]/div[5]/div/div[2]/div/div[1]/div/button', result_log)
        await self.upload_file(page, "cover_letter", data, '//*[@id="application-form"]/div[1]/div[6]/div/div[2]/div/div[1]/div/button', result_log)    
    
    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def fill_custom_questions(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
