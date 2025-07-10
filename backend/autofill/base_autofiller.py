from abc import ABC, abstractmethod
from typing import Dict, Any
from playwright.async_api import Page
from backend.utils.logging import get_logger

logger = get_logger(__name__)
class BaseAutofiller(ABC):
    
    @abstractmethod
    async def fill_basic_info(self, page: Page, data: Dict[str, Any]):
        pass
    @abstractmethod
    async def upload_documents(self, page: Page, data: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_custom_questions(self, page: Page, data: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any]):
        pass
    
    async def autofill(self, page: Page, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "filled_fields": [],
            "skipped_fields": [],
            "uploaded_files": {},
            "errors": [],
            "clicked_submit": False,
            "confirmation_found": False
        }

        try:
            logger.info("🧾 Filling basic info...")
            await self.fill_basic_info(page, data)

            logger.info("📄 Uploading documents...")
            await self.upload_documents(page, data)

            logger.info("🧬 Filling voluntary self-ID...")
            await self.fill_voluntary_self_id(page, data)

            logger.info("❓ Filling custom questions...")
            await self.fill_custom_questions(page, data)

            logger.info("🚀 Submitting if valid...")
            await self.click_submit_if_valid(page, data)

        except Exception as e:
            logger.exception(f"❌ Autofill failed: {e}")
            result["errors"].append(str(e))

        return result
        
        