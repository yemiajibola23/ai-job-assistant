from typing import Optional
import re
from difflib import get_close_matches

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
    
    if key in LABEL_KEY_MAP:
        return LABEL_KEY_MAP[key]
    
    if "linkedin" in key:
        return "linkedin"
    
    if "resume" in key:
        return "resume"
    
    if "cover" in key and "letter" in key:
        return "cover_letter"
    
    matches = get_close_matches(key, LABEL_KEY_MAP.keys(), n=1, cutoff=0.85)
    if matches:
        print(f"[matcher] 🤏 Fuzzy matched '{label.strip()}' → '{matches[0]}'")
        return LABEL_KEY_MAP[matches[0]]
    
    return None
    