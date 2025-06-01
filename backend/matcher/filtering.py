from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch

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