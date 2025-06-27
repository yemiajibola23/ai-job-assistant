from typing import Optional
import re

LABEL_KEY_MAP = {
    "name": "name",
    "full name": "name",
    "email": "email",
    "e mail": "email",
    "email address": "email",
    "e-mail address": "email",
    "skillset": "skills",
    "skills": "skills",
    "phone": "phone",
    "phone number": "phone",
    "contact email": "email",
    "contactemail": "email",
}

def normalize_label(label: str) -> str:
    label = label.lower()
    label = re.sub(r"[^\w\s]", "", label)
    label = re.sub(r"\s+", " ", label)
    
    return label.strip()

def match_label_to_key(label: str) -> Optional[str]:
    key = normalize_label(label)
    
    return LABEL_KEY_MAP.get(key)
    