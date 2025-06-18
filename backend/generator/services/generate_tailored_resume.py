from generator.services.gpt_tailoring import generate_tailored_bullets, generate_tailored_summary
from pathlib import Path

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
    output_path = Path(f"tailored_resume_{job_id}.md")
    output_path.write_text(full_resume, encoding="utf-8")

    return str(output_path)