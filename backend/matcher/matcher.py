from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_jobs(resume_text, job_descriptions, top_k=3):
     """
    Match resume text to job descriptions using semantic similarity.

    Args:
        resume_text (str): Combined resume content.
        job_descriptions (List[str]): A list of job description texts.
        top_k (int): Number of top matches to return.

    Returns:
        List[Tuple[str, float]]: Top matching job descriptions and similarity scores.
    """
     # Create embeddings
     resume_embedding = model.encode(resume_text, convert_to_tensor=True)
     job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

     # Compute cosine similarity
     scores = cosine_similarity(
          resume_embedding.cpu().reshape(1, -1),
          np.vstack([emb.cpu().numpy() for emb in job_embeddings])
     )[0]

     # Rank and return top matches
     ranked = sorted(
          zip(job_descriptions, scores),
          key=lambda x: x[1],
          reverse=True
     )
     
     return ranked[:top_k]