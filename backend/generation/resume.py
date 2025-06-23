from pathlib import Path
from backend.generation.openai_client import get_openai_response
from backend.generation.prompts import SUMMARY_PROMPT, BULLETS_PROMPT
import re

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
