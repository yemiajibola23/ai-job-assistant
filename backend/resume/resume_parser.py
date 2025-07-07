import fitz
import re
import json

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
    
    # Extract experience bullets
    parsed["experience"] = extract_experience_section(text)

    # Include full resume text
    parsed["raw_text"] = text.strip()

    return parsed

def extract_skills_from_text(text: str, skills=COMMON_SKILLS) -> list[str]:
    return [skill for skill in skills if skill.lower() in text.lower()]

def load_resume_text(path: str) -> str:
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def extract_experience_section(text: str) -> list[dict]:
    lines = text.splitlines()
    experience_section = []
    in_experience = False
    job_entry = None

    job_title_pattern = re.compile(r"^\s*(Senior|Lead|Junior)?\s*(iOS|Software|Mobile|Web|Data|Backend|Frontend)?\s*Developer|Engineer", re.IGNORECASE)
    bullet_pattern = re.compile(r"^\s*[-•]\s+")

    for line in lines:
        stripped = line.strip()

        # Toggle experience section on/off
        if re.match(r"^\s*Experience\s*$", stripped, re.IGNORECASE):
            in_experience = True
            continue
        if in_experience and re.match(r"^\s*(Education|Skills|Projects|Technical Skills)\s*$", stripped, re.IGNORECASE):
            break  # End of experience section

        if not in_experience:
            continue

        # New job title
        if job_title_pattern.match(stripped):
            if job_entry:
                experience_section.append(job_entry)
            job_entry = {"title": stripped, "bullets": []}
        elif bullet_pattern.match(stripped) and job_entry:
            job_entry["bullets"].append(stripped.lstrip("-•").strip())

    if job_entry:
        experience_section.append(job_entry)

    return experience_section
