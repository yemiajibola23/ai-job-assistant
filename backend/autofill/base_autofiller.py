from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from playwright.async_api import Page, async_playwright
from backend.utils.logging import get_logger
from backend.utils.constants import EMPTY_RESULT_DICT
from backend.utils.screenshot import take_screenshot
from backend.generation.generators.essay_generator import EssayResponseGenerator
from pathlib import Path
import copy
from backend.resume.resume_parser import load_resume_text, parse_resume_text

logger = get_logger(__name__)

ESSAY_KEYWORDS = ["why", "describe", "tell", "biggest", "strength", "challenge", "experience", "words", "example"]

class BaseAutofiller(ABC):
    def __init__(self, page: Page, profile_data: Dict[str, Any], resume_path: str, cover_letter_path: str, job_details: Dict[str, Any], essay_generator: Optional[EssayResponseGenerator]=None) -> None:
        self.page = page
        self.profile_data = profile_data
        self.resume_path = resume_path
        self.cover_letter_path = cover_letter_path
        self.job_details = job_details
        self.result_log = copy.deepcopy(EMPTY_RESULT_DICT)
        self.essay_generator = essay_generator
        
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: resume='{self.resume_path}', "
            f"job='{self.job_details.get('job_title', 'N/A')} at {self.job_details.get('company', 'N/A')}'>"
        )
    
    async def try_fill_by_id(self, field_id: str, value: str) -> bool:
        """
        Attempts to fill a field by ID using either a regular input or React Select.
        Returns True if successful, False otherwise.
        """
        xpath = f'//*[@id="{field_id}"]'
        selector = f'xpath={xpath}'

        try:
            await self.page.click(selector)
            await self.page.fill(selector, value)
            # await page.wait_for_timeout(200)
            await self.page.keyboard.press("Enter")
            # await page.wait_for_timeout(200)

            logger.info(f"✅ React Select filled {field_id} with value: {value}")            
            # Optional: Verify value locked in
            verified = await self.verify_filled_value(field_id, value)
            if verified:
                self.result_log["filled_fields"].append(field_id)
                logger.info(f"✅ Field '{field_id}' filled and verified.")
                return True
            else:
                logger.warning(f"⚠️ Field '{field_id}' may not have retained the filled value.")
                return False
        except Exception as e2:
            logger.error(f"❌ Failed to fill {field_id} via both methods: {e2}")
            self.result_log["errors"].append({field_id: str(e2)})
            return False
    
    # Optional: Verify value locked in (if react-select)
    # element = await page.query_selector(selector)
    # selected_text = await element.input_value()
    # if selected_text and value.lower() not in selected_text.lower():
    #     logger.warning(f"⚠️ Field '{field_id}' may not have been locked in. Found: '{selected_text}'")
    
    async def try_fill_text_field(self, field_id: str, value: str) -> bool:
        """
        Attempts to fill a text input or textarea by ID.
        Uses page.fill and simulates Enter key to trigger dropdowns if needed.
        Logs result.
        """
        return await self.try_fill_by_id(field_id, value)

    async def verify_filled_value(self, field_id: str, expected_value: str) -> bool:
        """
        Verifies that the value of a field matches the expected input.
        Useful for React-select or dynamic inputs where .fill may not persist.
        """
        xpath = f'//*[@id="{field_id}"]'
        element = await self.page.query_selector(f'xpath={xpath}')
        
        if not element:
            logger.warning(f"⚠️ Could not find field '{field_id}' for verification.")
            return False
        
        actual_value = await element.input_value()
        filled_correctly = actual_value.lower() in expected_value.lower()
        
        if not filled_correctly:
            logger.debug(
                f"⚠️ Field '{field_id}' may not have been filled correctly. "
                f"Expected: '{expected_value}', Found: '{actual_value}'"
            )

        return filled_correctly
    
    async def upload_documents(self, resume_path: str, cover_letter_path: str, resume_xpath: str, cover_letter_xpath: str):
        await self.upload_file("resume", resume_path, resume_xpath)
        await self.upload_file("cover_letter", cover_letter_path, cover_letter_xpath)   
    
    async def upload_file(self, field_key: str, file_path: str, fallback_xpath: str):        
        if not file_path or not Path(file_path).exists():
            logger.warning(f"⚠️ No valid {field_key} path provided. Skipping {field_key} upload.")
            self.result_log["skipped_fields"].append(field_key)
            return
        
        try:
            await self.page.set_input_files(f"input#{field_key}", file_path)
            logger.info(f"📄 Uploaded {field_key} using direct file input: {file_path}")
            self.result_log["filled_fields"].append(field_key)
            self.result_log["uploaded_files"][field_key] = file_path
            return 
        except Exception as e1:
            logger.warning(f"❌ Direct {field_key} upload failed: {e1}")
            
        if fallback_xpath:
            try:
                # Fallback: Click the upload button
                upload_button_xpath = fallback_xpath
                await self.page.click(f"xpath={upload_button_xpath}")
                # Wait and retry input after modal/dialog appears
                await self.page.set_input_files('input[type="file"]', file_path)
                logger.info(f"📄 Uploaded {field_key} using fallback file dialog method: {file_path}")
                self.result_log["uploaded_files"][field_key] = file_path
            except Exception as e2:
                logger.error(f"❌ {field_key} upload failed entirely: {e2}")
                self.result_log["errors"].append({f"{field_key}": str(e2)})
                
    def is_essay_question(self, label_text: str, tag: str, attrs: Dict[str, Any]) -> bool:
        """
        Determines whether a field is an essay question based on label and element attributes.
        """
        text = label_text.lower()

        # 🔍 Step 1: Check label keywords
        if any(word in text for word in ESSAY_KEYWORDS):
            return True

        # 🧠 Step 2: Check tag and attrs
        if tag == "textarea":
            return True

        # Get attributes safely
        maxlength = int(attrs.get("maxlength", 0) or 0)
        rows = int(attrs.get("rows", 0) or 0)
        cols = int(attrs.get("cols", 0) or 0)

        # 🧪 Heuristic-based
        if maxlength >= 200:
            return True
        if rows >= 3:
            return True
        if cols >= 40:
            return True

        return False
    
    async def handle_essay_question(self, label_text: str, field_id: str):
        try:
            selector = f'xpath=//*[@id="{field_id}"]'
            input_el = await self.page.query_selector(selector)
            maxlength_raw = await input_el.get_attribute("maxlength") if input_el else None
            maxlength = int(maxlength_raw) if maxlength_raw and maxlength_raw.isdigit() else None
            
            essay_data = self.get_essay_data(label_text, maxlength)
            if not self.essay_generator:
                raise RuntimeError("No essay generator configured. Cannot fill essay questions.")

            # 1. Generate response using GPT
            response =  self.essay_generator.generate(essay_data)
            if not response or len(response.strip()) < 10:
                raise ValueError("GPT returned empty or insufficient response")
            
            # 2. Fill the field
            selector = f'xpath=//*[@id="{field_id}"]'
            await self.page.fill(selector, response)
            await self.page.keyboard.press("Enter")

            # 3. Log success
            self.result_log["essays_filled"].append({
                "field_id": field_id,
                "essay_question": label_text,
                "response": response
            })

            logger.info(f"✍️ Essay filled for {label_text[:40]}...")
        except Exception as e:
            logger.error(f"❌ Error filling essay question '{label_text}': {e}")
            self.result_log["skipped_fields"].append(label_text)
            self.result_log["errors"].append({
                "field_id": field_id,
                "label": label_text,
                "error": str(e),
                "source": "essay_gpt"
            })
            
    def get_essay_data(self, label_text: str, max_length: Optional[int]) -> Dict[str, Any]:
        resume_text = load_resume_text(self.resume_path)
        resume_data = parse_resume_text(resume_text)

        summary = resume_data.get("raw_text", "")[:400]  # truncate if needed
        skills = ", ".join(resume_data.get("skills", []))
        experience = resume_data.get("experience", [])
        top_bullets = [b for e in experience for b in e.get("bullets", [])][:2]
        exp_str = "\n".join(f"- {b}" for b in top_bullets)
        
        return {
            "company": self.job_details.get("company_name", "this company"),
            "job_title": self.job_details.get("job_title", "this role"),
            "question": label_text,
            "job_description": self.job_details.get("description"),
            "summary": summary,
            "skills": skills,
            "experience": exp_str,
            "max_length": max_length
         }
        
    @abstractmethod
    async def submit_application(self) -> bool:
        """Subclasses must define how to submit the application form."""
        pass
    
    @abstractmethod
    async def autofill(self):
        pass
    
    