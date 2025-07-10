from abc import ABC, abstractmethod
from typing import Dict, Any
from playwright.async_api import Page
from backend.utils.logging import get_logger
from backend.utils.constants import EMPTY_RESULT_DICT

logger = get_logger(__name__)
class BaseAutofiller(ABC):
    
    @abstractmethod
    async def fill_basic_info(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    @abstractmethod
    async def upload_documents(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def fill_custom_questions(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    @abstractmethod
    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any], result_log: Dict[str, Any]):
        pass
    
    async def autofill(self, page: Page, data: Dict[str, Any]) -> Dict[str, Any]:
        result = EMPTY_RESULT_DICT
        try:
            logger.info("🧾 Filling basic info...")
            await self.fill_basic_info(page, data, result)

            logger.info("📄 Uploading documents...")
            await self.upload_documents(page, data, result)

            logger.info("🧬 Filling voluntary self-ID...")
            await self.fill_voluntary_self_id(page, data, result)

            logger.info("❓ Filling custom questions...")
            await self.fill_custom_questions(page, data, result)

            logger.info("🚀 Submitting if valid...")
            await self.click_submit_if_valid(page, data, result)

        except Exception as e:
            logger.exception(f"❌ Autofill failed: {e}")
            result["errors"].append(str(e))

        return result
        
        