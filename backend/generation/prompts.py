BULLETS_PROMPT = """
You are an expert resume coach.

Rewrite the following experience bullet points so they align with the target job description. Emphasize relevant skills, technologies, and accomplishments using clear and concise language.

Return only the updated bullet points in a numbered list. Keep each bullet under 20 words.

---

Original Bullet Points:
{original_bullets}

---

Target Job Description:
{job_description}

---

Rewritten Bullet Points:
"""


COVER_LETTER_PROMPT = """You are an expert career coach and professional writer. Given a resume and a job description, your task is to generate a tailored, compelling, and concise cover letter. The tone should be professional but warm, and show genuine interest in the company.

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

SUMMARY_PROMPT = """
You are an expert technical resume writer.

Given the following original resume summary and job description, rewrite the summary so that it highlights the most relevant skills, technologies, and experiences for the job. Keep it professional, confident, and concise.

Be sure to:
- Use keywords and language from the job description
- Keep it under 4 sentences
- Maintain a natural human tone (not robotic)

---

Original Resume Summary:
{base_summary}

---

Target Job Description:
{job_description}

---

Rewritten Summary:
"""
