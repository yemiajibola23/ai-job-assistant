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

def get_resume_prompt(data: dict) -> str:
    summary = data.get("summary", "")
    experience = data.get("experience", [])
    skills = data.get("skills", [])
    education = data.get("education", [])
    linkedin = data.get("linkedin", None)

    # Flatten and format experience bullets
    bullets = []
    for job in experience:
        bullets.extend(job.get("bullets", []))
    bullet_block = "\n".join([f"- {b}" for b in bullets])

    # Format education section
    education_block = "\n".join([f"- {degree}" for degree in education])

    return f"""
# {data.get('name', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
{f'LinkedIn: {linkedin}' if linkedin else ''}

## Summary
{summary}

## Experience
{bullet_block}

## Skills
{', '.join(skills)}

## Education
{education_block}
""".strip()
