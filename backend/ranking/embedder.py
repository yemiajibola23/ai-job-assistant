from sentence_transformers import SentenceTransformer
from typing import Any
import numpy as np
import torch

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: list[str], to_tensor: bool = False) -> Any:
    model = get_model()
    return model.encode(texts, convert_to_tensor=to_tensor)