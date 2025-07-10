from .base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
class GreenhouseAutofiller(BaseAutofiller):
    async def fill_basic_info(self, page: Page, data: Dict[str, Any]):
        pass

    async def upload_documents(self, page: Page, data: Dict[str, Any]):
        pass

    async def fill_voluntary_self_id(self, page: Page, data: Dict[str, Any]):
        pass

    async def fill_custom_questions(self, page: Page, data: Dict[str, Any]):
        pass

    async def click_submit_if_valid(self, page: Page, data: Dict[str, Any]):
        pass
