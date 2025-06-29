from typing import Optional
import re
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.ranking.embedder import embed_texts

class FieldMatcher:
    def __init__(self, threshold: float=0.45) -> None:
        self.keys = ["name", "phone", "email", "linkedin", "resume", "skills"]
        self.key_embeddings = embed_texts(self.keys)
        self.threshold = threshold

    def match(self, label: str) -> str | None:
        label_embedding = np.array(embed_texts([label])[0])
        similarities = cosine_similarity(np.array([label_embedding]), self.key_embeddings)[0]

        best_index = np.argmax(similarities)
        best_score = similarities[best_index]
        best_key = self.keys[best_index]
        
        print(f"[matcher] Label: '{label}' → Best match: '{best_key}' (score: {best_score:.2f})")
        
        if best_score >= self.threshold:
            return best_key
        else:
            return None


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


_matcher = FieldMatcher()

def match_label_to_key(label: str) -> Optional[str]:
    embedding_match = _matcher.match(label)
    if embedding_match:
        return embedding_match
    
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
    