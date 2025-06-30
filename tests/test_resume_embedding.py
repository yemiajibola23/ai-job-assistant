import numpy as np
from backend.resume.resume_embeddings import embed_resume


def test_embed_resume_returns_vector():
    resume_dict = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-123-4567",
        "skills": ["python", "react"],
        "raw_text": "Experienced engineer skilled in Python and React."
    }

    vector = embed_resume(resume_dict)

    assert vector is not None
    assert isinstance(vector, np.ndarray)
    assert vector.shape == (384,)