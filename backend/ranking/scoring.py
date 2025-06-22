from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
from backend.ranking.embedder import embed_texts

def filter_jobs(jobs: List[Dict], resume_embedding: np.ndarray, top_n: int = 5) -> List[Dict]:
    """
    Filters a list of jobs based on cosine similarity to the resume embedding.
    
    Args:
        jobs: A list of job dicts, each containing an 'embedding' field.
        resume_embedding: A NumPy array representing the embedded resume.
        top_n: The number of top jobs to return.

    Returns:
        A list of top_n job dicts, each with an added 'score' key.
    """

    # Convert all job embeddings into a stacked NumPy array
    job_embeddings = np.vstack([
        job['embedding'].detach().cpu().numpy() if isinstance(job['embedding'], torch.Tensor)  else job['embedding']   
        for job in jobs
    ])

    # Ensure resume is also NumPy
    if isinstance(resume_embedding, torch.Tensor):
        resume_embedding = resume_embedding.detach().cpu().numpy()

    # Compute cosine similarity between resume and all jobs
    scores = cosine_similarity(resume_embedding.reshape(1, -1), job_embeddings)[0]

    # Attach score to each job
    scored_jobs = []
    for job, score in zip(jobs, scores):
        job_with_score = job.copy()
        job_with_score["score"] = float(score)
        scored_jobs.append(job_with_score)
    
    return sorted(scored_jobs, key=lambda x: x["score"], reverse=True)[:top_n]



def match_resume_to_jobs(resume_text, job_descriptions, top_k=None):
     """
    Match resume text to job descriptions using semantic similarity.

    Args:
        resume_text (str): Combined resume content.
        job_descriptions (List[str]): A list of job description texts.
        top_k (int): Number of top matches to return.

    Returns:
        List[Tuple[str, float]]: Top matching job descriptions and similarity scores.
    """
     # print(f"List of job_descriptions: {job_descriptions}")
     if not job_descriptions:
          print("⚠️ No job descriptions found!!!")
          return []

     # Create embeddings
     resume_embedding = embed_texts(resume_text, to_tensor=True)
     job_embeddings = embed_texts(job_descriptions, to_tensor=True)

     # Compute cosine similarity
     # print("Computing job scores...")
     scores = cosine_similarity(
          resume_embedding.cpu().reshape(1, -1),
          job_embeddings.cpu().numpy()
     )[0]

     # Rank and return top matches
     ranked = sorted(
          zip(job_descriptions, scores),
          key=lambda x: x[1],
          reverse=True
     )

     if top_k:
          return ranked[:top_k]
     return ranked