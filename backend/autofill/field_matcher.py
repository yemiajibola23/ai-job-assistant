from typing import Optional
import re
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.ranking.embedder import embed_texts
from backend.autofill.field_matcher_config import (
    CANONICAL_KEYS,
    LABEL_KEY_MAP,
    FUZZY_CUTOFF,
    EMBEDDING_THRESHOLD,
)


class FieldMatcher:
    def __init__(self, 
                 keys: list[str]=CANONICAL_KEYS, 
                 label_map: dict[str, str]=LABEL_KEY_MAP, 
                 fuzzy_cutoff: float=FUZZY_CUTOFF, 
                 embedding_threshold: float = EMBEDDING_THRESHOLD) -> None:
        self.keys = keys
        self.label_map = label_map
        self.fuzzy_cutoff = fuzzy_cutoff
        self.embedding_threshold = embedding_threshold
        self.key_embeddings = embed_texts(self.keys)

    def match(self, label: str, debug: bool=False) -> Optional[str]:
        normalized = normalize_label(label)
        
        match = (
            self._rule_based_match(normalized)
            or self._regex_heuristics(normalized)
            or self._embedding_match(normalized)
            or self._fuzzy_match(normalized)
        )
        
        if debug:
            if match:
                print(f"[matcher-debug] ✅ Matched '{label}' → '{match}'")
            else:
                print(f"[matcher-debug] ❌ No match found for '{label}'")
        
        return match
    
    def _rule_based_match(self, normalized: str) -> Optional[str]:
        return LABEL_KEY_MAP.get(normalized)

    def _regex_heuristics(self, normalized: str) -> Optional[str]:
        if "linkedin" in normalized:
            return "linkedin"
        if "resume" in normalized:
            return "resume"
        if "cover" in normalized and "letter" in normalized:
            return "cover_letter"
        return None

    def _embedding_match(self, label: str) -> Optional[str]:
        label_embedding = np.array(embed_texts([label])[0])
        similarities = cosine_similarity(
            np.array([label_embedding]), 
            np.array(self.key_embeddings)
        )[0]
        best_index = int(np.argmax(similarities))
        best_score = similarities[best_index]
        best_key = self.keys[best_index]

        if best_score >= self.embedding_threshold:
            return best_key
        return None

    def _fuzzy_match(self, normalized: str) -> Optional[str]:
        matches = get_close_matches(normalized, LABEL_KEY_MAP.keys(), n=1, cutoff=0.85)
        if matches:
            return LABEL_KEY_MAP[matches[0]]
        return None


_matcher = FieldMatcher()

def normalize_label(label: str) -> str:
    label = label.lower()
    label = re.sub(r"[^\w\s]", "", label)
    label = re.sub(r"\s+", " ", label)
    
    return label.strip()

def match_label_to_key(label: str, debug: bool = True) -> Optional[str]:
    return _matcher.match(label, debug)