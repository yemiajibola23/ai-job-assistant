from typing import Dict

FUZZY_CUTOFF = 0.85
EMBEDDING_THRESHOLD = 0.45

# ✅ Canonical supported keys
CANONICAL_KEYS = [
    "name",
    "phone",
    "email",
    "linkedin",
    "resume",
    "cover_letter",
    "skills"
]

# 🧠 Rule-based string normalization map
LABEL_KEY_MAP: Dict[str, str] = {
    "name": "name",
    "full name": "name",
    "email": "email",
    "e mail": "email",
    "email address": "email",
    "e-mail address": "email",
    "contact email": "email",
    "contactemail": "email",
    "phone": "phone",
    "phone number": "phone",
    "linkedin": "linkedin",
    "linked in": "linkedin",
    "linkedin profile": "linkedin",
    "resume": "resume",
    "upload resume": "resume",
    "attach resume": "resume",
    "cover letter": "cover_letter",
    "upload cover letter": "cover_letter",
    "attach cover letter": "cover_letter",
    "skills": "skills",
    "skillset": "skills",
}
