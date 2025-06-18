# bullets_prompt.py

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
