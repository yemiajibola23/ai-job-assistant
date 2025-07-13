from typing import List, Dict, Optional

ESSAY_PROMPT = """
You are a job applicant. Based on the job at {company_name} for a {job_title} and your background, write {length_hint} answer to the following application question:
“{question}”
🏢 Job Description (summary):
{job_description}
👤 Your Resume:
Summary: {summary}
Skills: {skills}
Experience Highlights: {experience}
"""


def get_essay_prompt(company: str, job_title: str, question: str, job_description: str, summary: str, skills: List[str], experience: Dict[str, str], max_length:Optional[int]) -> str:
    length_hint = f"no more than {max_length} characters" if max_length else "a short answer"
    return ESSAY_PROMPT.format(company_name=company, job_title=job_title,  question=question, job_description=job_description, summary=summary, skills=skills, experience=experience, length_hint=length_hint)