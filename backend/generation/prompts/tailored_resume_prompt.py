from pathlib import Path
from backend.generation.client.openai_client import get_openai_response
import re

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

def tailor_resume_data(data: dict, job_description: str) -> dict:
    tailored = data.copy()
    
    # Tailor summary
    tailored["summary"] = generate_tailored_summary(
        base_summary=data.get("summary", ""),
        job_description=job_description
    )

    # Tailor bullets for all experience entries
    all_bullets = []
    for job in data.get("experience", []):
        all_bullets.extend(job.get("bullets", []))

    new_bullets = generate_tailored_bullets(all_bullets, job_description)

    # Distribute tailored bullets evenly back into jobs
    jobs = data.get("experience", [])
    idx = 0
    for job in jobs:
        num = len(job.get("bullets", []))
        job["bullets"] = new_bullets[idx : idx + num]
        idx += num

    tailored["experience"] = jobs
    return tailored


def generate_full_tailored_resume(job_id: str, resume_data: dict, job_description: str) -> str:
    all_bullets = [bullet for job in resume_data["experience"] for bullet in job["bullets"]]

    tailored_summary = generate_tailored_summary(resume_data["summary"], job_description)
    tailored_bullets = generate_tailored_bullets(all_bullets, job_description)
    experience_section = "\n".join([f"- {bullet}" for bullet in tailored_bullets])
    skills_section = ", ".join(resume_data["skills"])

    full_resume = f"""# {resume_data['name']}

📧 {resume_data['email']}  
📞 {resume_data['phone']}

---

## Summary
{tailored_summary}

---

## Experience
{experience_section}

---

## Skills
{skills_section}
"""
    output_dir = Path("output/resumes")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"tailored_resume_{job_id}.md"
    output_path.write_text(full_resume, encoding="utf-8")

    return str(output_path)


def generate_tailored_summary(base_summary: str, job_description: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        base_summary=base_summary.strip(),
        job_description=job_description.strip()
    )
    
    return get_openai_response(prompt)

def generate_tailored_bullets(experience_bullets: list[str], job_description: str) -> list[str]:
    formatted_bullets = "\n".join(experience_bullets)

    prompt = BULLETS_PROMPT.format(
        original_bullets=formatted_bullets,
        job_description=job_description.strip()
    )

    response = get_openai_response(prompt)
    raw_bullets = response.split("\n")

    # Strip leading numbering like "1. ", "2. ", etc.
    clean_bullets = [re.sub(r"^\s*\d+\.\s*", "", b).strip() for b in raw_bullets if b.strip()]

    return clean_bullets


def get_resume_prompt(data: dict) -> str:
    summary = data.get("summary", "")
    experience = data.get("experience", [])
    skills = data.get("skills", [])
    
    bullets = []
    for job in experience:
        bullets.extend(job.get("bullets", []))
    bullet_block = "\n".join([f" - {b}" for b in bullets])
    
    return f"""
# {data.get('name', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}

## Summary
{summary}

## Experience
{bullet_block}

## Skills
{skills}
""".strip()
