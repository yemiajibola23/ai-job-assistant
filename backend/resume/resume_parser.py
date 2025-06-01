import fitz
import re

COMMON_SKILLS = [
    "python", "java", "swift", "javascript", "react", "node.js", "sql", "swiftui",
    "git", "docker", "kubernetes", "linux", "aws", "gcp", "azure", "tensorflow",
    "pytorch", "machine learning", "data analysis", "project management", "communication",
    "leadership", "teamwork", "problem solving", "agile", "scrum"
]


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page in doc:
        full_text += page.get_text() # type: ignore
    
    return full_text

def parse_resume_text(text: str) -> dict:
    parsed = {}

    # Extract name
    lines = text.splitlines()
    name = None
    for line in lines:
        line = line.strip()
        if (line and not re.search(r"email|phone|linkedin|github|@|\d", line, re.I) and len(line.split()) <= 4):
            name = line
            break
    parsed["name"] = name

    # Extract email using regex
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    parsed["email"] = email_match.group(0) if email_match else None
    
    # Extract phone number (US Format)
    phone_match = re.search(r"(\+?\d{1,2}[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}", text)
    parsed["phone"] = phone_match.group(0) if phone_match else None
    
    # Extract skills
    parsed["skills"] = extract_skills_from_text(text)

    # Include full resume text
    parsed["raw_text"] = text.strip()

    return parsed

def extract_skills_from_text(text: str, skills=COMMON_SKILLS) -> list[str]:
    return [skill for skill in skills if skill.lower() in text.lower()]

