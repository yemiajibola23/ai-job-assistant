from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from playwright.async_api import Page, async_playwright
from backend.utils.logging import get_logger
from backend.utils.constants import EMPTY_RESULT_DICT
from backend.utils.screenshot import take_screenshot
from backend.generation.client.openai_client import OpenAIClient

logger = get_logger(__name__)
class BaseAutofiller(ABC):
    def __init__(self, gpt_client: Optional[OpenAIClient] = None) -> None:
       self.gpt_client = gpt_client
    
    @abstractmethod
    async def fill_basic_info(self, page: Page, profile_data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    @abstractmethod
    async def upload_documents(self, page: Page, resume_path: str, cover_letter_path: str, result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_voluntary_self_id(self, page: Page, profile_data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_custom_questions(self, page: Page, profile_data: Dict[str, Any], job_data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def click_submit_if_valid(self, page: Page, result_log: Dict[str, Any]):
        pass
    
    async def _autofill_page(self, page: Page, profile_data: Dict[str, Any], resume_path: str, cover_letter_path: str, job_data: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
        result = EMPTY_RESULT_DICT
        try:
            await page.goto(job_data.get("url", ""))
            logger.info("🧾 Filling basic info...")
            await self.fill_basic_info(page, profile_data, result)

            logger.info("📄 Uploading documents...")
            await self.upload_documents(page, resume_path, cover_letter_path, result)
            
            logger.info("❓ Filling custom questions...")
            await self.fill_custom_questions(page, profile_data, job_data, result)

            logger.info("🧬 Filling voluntary self-ID...")
            await self.fill_voluntary_self_id(page, profile_data, result)
            
            if not dry_run:
                logger.info("🚀 Submitting if valid...")
                await self.click_submit_if_valid(page, result)
            else:
                await take_screenshot(page)
                logger.info("Dry run detected, not submitting...")

        except Exception as e:
            logger.exception(f"❌ Autofill failed: {e}")
            result["errors"].append(str(e))

        return result
    
    async def autofill(self, profile_data: Dict[str, Any], resume_path: str, cover_letter_path: str, job_data: Dict[str, Any], page: Optional[Page]=None, dry_run=True) -> Dict[str, Any]:
        if page is None: 
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                context = await browser.new_context()
                page = await context.new_page()
                
        return await self._autofill_page(page, profile_data, resume_path, cover_letter_path, job_data, dry_run)    
        
        