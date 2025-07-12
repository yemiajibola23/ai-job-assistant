from typing import List, Dict

ESSAY_PROMPT = """
You are a job applicant. Based on the job at {company_name} for a {job_title} and your background, write a short (~100 words) answer to the following application question:
“{question}”
🏢 Job Description (summary):
{job_description}
👤 Your Resume:
Summary: {summary}
Skills: {skills}
Experience Highlights: {experience}
"""

def get_essay_prompt(company: str, job_title: str, question: str, job_description: str, summary: str, skills: List[str], experience: Dict[str, str]) -> str:
    return ESSAY_PROMPT.format(company_name=company, job_title=job_title,  question=question, job_description=job_description, summary=summary, skills=skills, experience=experience)