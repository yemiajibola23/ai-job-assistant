import openai

def generate_cover_letter(resume_summary: str, job_description: str, user_notes: str = "") -> str:
    """
    Generates a cover letter tailored to a job description and resume summary.

    Args:
        resume_summary (str): Extracted or summarized resume text.
        job_description (str): Full job posting or relevant excerpt.
        user_notes (str, optional): Any extra instructions (e.g., tone, specific experiences to mention).

    Returns:
        str: Generated cover letter.
    """
    
    prompt = f"""
You are an expert career coach and professional writer. Given a resume and a job description, your task is to generate a tailored, compelling, and concise cover letter. The tone should be professional but warm, and show genuine interest in the company.

### Job Description:
{job_description}

### Resume Summary:
{resume_summary}

### Notes (optional):
{user_notes}

Write a cover letter that:
- Is addressed to the hiring manager
- Introduces the applicant and their interest in the role
- Highlights relevant experience and skills
- Reflects the tone of the company
- Ends with a brief call to action or next step

Please return only the letter — no preamble, no formatting.
"""

