import fitz
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page in doc:
        full_text += page.get_text() # type: ignore
    
    return full_text

def parse_resume_text(text: str) -> dict:
    parsed = {}

    # Extract email using regex
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    parsed["email"] = email_match.group(0) if email_match else None
    
    # Extract phone number (US Format)
    phone_match = re.search(r"(\+?\d{1,2}[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}", text)
    parsed["phone"] = phone_match.group(0) if phone_match else None
    
    # Include full resume text
    parsed["raw_text"] = text.strip()

    return parsed