from backend.autofill.base_autofiller import BaseAutofiller
from playwright.async_api import Page
from typing import Dict, Any, Literal, Optional
import logging
from backend.autofill.xpath_utils import try_fill_by_id, get_labeled_field_xpath
from pathlib import Path
from backend.autofill.field_matcher_config import LABEL_KEY_MAP, VALUE_NORMALIZATION
from backend.generation.client.openai_client import OpenAIClient
from backend.generation.generators.essay_generator import EssayResponseGenerator
from backend.resume.resume_parser import load_resume_text, parse_resume_text

logger = logging.getLogger(__name__)

RESUME_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[5]/div/div[2]/div/div[1]/div/button'
COVER_LETTER_UPLOAD_BUTTON_XPATH = '//*[@id="application-form"]/div[1]/div[6]/div/div[2]/div/div[1]/div/button'
BASIC_INFO_FIELDS = ["name", "first_name", "last_name", "email", "phone"]
VOLUNTARY_SELF_ID_FIELDS = ["gender", "hispanic_ethnicity", "veteran_status", "disability_status"]
ESSAY_KEYWORDS = ["why", "describe", "tell", "biggest", "strength", "challenge", "experience", "words", "example"]

class GreenhouseAutofiller(BaseAutofiller):
    async def fill_basic_info(self, page: Page, profile_data: Dict[str, Any], result_log: Dict[str, Any]):
        logger.info("🧾 Filling basic info...")
        
        for field in BASIC_INFO_FIELDS:
            if field == "name":
                await self.fill_name_fields(page, profile_data, result_log)
                continue  # Skip to next field after handling 'name'
            
            value = profile_data.get(field, "")
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
            
    async def fill_name_fields(self, page: Page, profile_data: Dict[str, Any], result_log: Dict[str, Any]):
         # ✅ Step 1: Check if both first_name and last_name exist in profile_data
                if "first_name" in profile_data and "last_name" in profile_data:
                    # Try to fill separate fields
                    for key in ["first_name", "last_name"]:
                        value = profile_data[key]
                        selector = f'xpath=//*[@id="{key}"]'
                        input_el = await page.query_selector(selector)
                        if input_el:
                            await input_el.fill(value)
                            logger.info(f"✅ Filled {key} field with value: {value}")
                            result_log["filled_fields"].append(key)
                        else:
                            logger.warning(f"⚠️ Could not find input field for '{key}'")
                            result_log["skipped_fields"].append(key)
                else:
                    # 👥 Step 2: Combine first + last and fill single full name field
                    first = profile_data.get("first_name", "")
                    last = profile_data.get("last_name", "")
                    full_name = f"{first} {last}".strip()

                    if full_name:
                        for full_name_id in ["full_name", "name", "candidate_name"]:
                            selector = f'xpath=//*[@id="{full_name_id}"]'
                            input_el = await page.query_selector(selector)
                            if input_el:
                                await input_el.fill(full_name)
                                logger.info(f"✅ Filled full name field '{full_name_id}' with value: {full_name}")
                                result_log["filled_fields"].append("name")
                                break
                            else:
                                logger.warning("⚠️ Could not locate any full name field (full_name, name, candidate_name)")
                                result_log["skipped_fields"].append("name")
                    else:
                        logger.warning("⚠️ No full name data available to fill.")
                        result_log["skipped_fields"].append("name")
        
    async def upload_file(self, page: Page, field_key: str, file_path, xpath: str, result_log: Dict[str, Any]):        
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
            
    async def upload_documents(self, page: Page, resume_path: str, cover_letter_path: str, result_log: Dict[str, Any]):
        await self.upload_file(page, "resume", resume_path, RESUME_UPLOAD_BUTTON_XPATH, result_log)
        await self.upload_file(page, "cover_letter", cover_letter_path, COVER_LETTER_UPLOAD_BUTTON_XPATH, result_log)    
    
    async def fill_voluntary_self_id(self, page: Page, profile_data: Dict[str, Any], result_log: Dict[str, Any]):        
        for field in VOLUNTARY_SELF_ID_FIELDS:
            await page.wait_for_timeout(5000)
            raw_value = profile_data.get(field)
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
            
            label_text = next(
                (label for label, canonical in LABEL_KEY_MAP.items() if canonical == field),
                field.replace("_", " ").title()
            )
            
            # 🪂 Fallback using label-based XPath
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


    async def fill_custom_questions(self, page: Page, profile_data: Dict[str, Any], job_data: Dict[str, Any], result_log: Dict[str, Any]):
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
                attrs = {
                    "maxlength": await input_element.get_attribute("maxlength"),
                    "rows": await input_element.get_attribute("rows"),
                    "cols": await input_element.get_attribute("cols"),
                    }

                # Dispatch
                if self.is_essay_question(label_text, tag_name, attrs):
                    await self.handle_essay_custom_question(page, label_text, field_id, job_data, result_log)
                elif label_text.strip().lower() in LABEL_KEY_MAP:
                    await self.handle_basic_custom_question(page, label_text, field_id, profile_data, result_log)
                else:
                    await self.handle_dropdown_custom_question(page, label_text, field_id, profile_data, result_log)

            except Exception as e:
                logger.error(f"❌ Error classifying custom question '{label_text}': {e}")
                result_log["errors"].append({label_text: str(e)})

    
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

    async def handle_essay_custom_question(self, page: Page, label_text: str, field_id: str, job_data: Dict[str, Any], result_log: Dict[str, Any]):
        try:
            selector = f'xpath=//*[@id="{field_id}"]'
            input_el = await page.query_selector(selector)
            maxlength_raw = await input_el.get_attribute("maxlength") if input_el else None
            maxlength = int(maxlength_raw) if maxlength_raw and maxlength_raw.isdigit() else None

            
            essay_data = self.get_esssay_data(job_data, label_text, maxlength)
            # 1. Generate response using GPT
            response =  self.essay_generator.generate(essay_data)
            if not response or len(response.strip()) < 10:
                raise ValueError("GPT returned empty or insufficient response")
            
            # 2. Fill the field
            selector = f'xpath=//*[@id="{field_id}"]'
            await page.fill(selector, response)
            await page.keyboard.press("Enter")

            # 3. Log success
            result_log["essays_filled"].append({
                "field_id": field_id,
                "essay_question": label_text,
                "response": response
            })

            logger.info(f"✍️ Essay filled for {label_text[:40]}...")
        except Exception as e:
            logger.error(f"❌ Error filling essay question '{label_text}': {e}")
            result_log["skipped_fields"].append(label_text)
            result_log["errors"].append({
                "field_id": field_id,
                "label": label_text,
                "error": str(e),
                "source": "essay_gpt"
            })
            
    def get_esssay_data(self, job_data: Dict[str, Any], label_text: str, max_length: Optional[int]) -> Dict[str, Any]:
        resume_path = job_data.get("resume_path", "tests/data/yemi_resume.pdf")
        resume_text = load_resume_text(resume_path)
        resume_data = parse_resume_text(resume_text)

        summary = resume_data.get("raw_text", "")[:400]  # truncate if needed
        skills = ", ".join(resume_data.get("skills", []))
        experience = resume_data.get("experience", [])
        top_bullets = [b for e in experience for b in e.get("bullets", [])][:2]
        exp_str = "\n".join(f"- {b}" for b in top_bullets)
        
        return {
            "company": job_data.get("company_name", "this company"),
            "job_title": job_data.get("job_title", "this role"),
            "question": label_text,
            "job_description": job_data.get("description"),
            "summary": summary,
            "skills": skills,
            "experience": exp_str,
            "max_length": max_length
         }

    async def click_submit_if_valid(self, page: Page, result_log: Dict[str, Any]):
        pass