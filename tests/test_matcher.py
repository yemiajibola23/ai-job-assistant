import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.matcher.matcher import match_resume_to_jobs


resume_text = """
Senior iOS Developer with 6+ years of experience building Swift and SwiftUI apps. 
Led modularization and performance work in the NBA app. 
Proficient in async/await, clean architecture, and team collaboration.
"""
job_descriptions = [
    "Machine Learning Engineer for NLP and image models using PyTorch and Transformers.",
    "iOS Engineer for a live sports streaming app, using Swift and SwiftUI in a team of mobile developers.",
    "Backend Developer to build GraphQL APIs for a fintech platform using Node.js and PostgreSQL."
]

def test_resume_matching():
    matches = match_resume_to_jobs(resume_text, job_descriptions, top_k=3)

    print("\n🔍 Top Resume Matches:")
    for idx, (job, score) in enumerate(matches, 1):
        print(f"{idx}. Score: {score:.2f} | Job: {job[:80]}...")
    

if __name__ == "__main__":
    test_resume_matching()