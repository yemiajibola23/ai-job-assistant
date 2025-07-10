from backend.autofill.base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any
import logging
from backend.autofill.xpath_utils import try_fill_by_id

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
            
    async def upload_documents(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def fill_custom_questions(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass

    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
