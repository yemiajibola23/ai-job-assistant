import numpy as np
from backend.ranking.embedder import embed_texts

def embed_resume(resume_dict: dict) -> np.ndarray:
    raw_text = resume_dict.get("raw_text", "")
    return embed_texts([raw_text])[0]