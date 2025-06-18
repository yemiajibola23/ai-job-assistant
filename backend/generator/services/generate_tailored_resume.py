from .openai_client import get_openai_response
from generator.prompts.summary_prompt import SUMMARY_PROMPT
from generator.prompts.bullets_prompt import BULLETS_PROMPT
from pathlib import Path

def generate_tailored_summary(base_summary: str, job_description: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        base_summary=base_summary.strip(),
        job_description=job_description.strip()
    )
    
    return get_openai_response(prompt)

def generate_tailored_bullets(experience_bullets: list[str], job_description: str) -> list[str]:
    formatted_bullets = "\n".join(
        [f"{i}. {b}" for i, b in enumerate(experience_bullets, start=1)]
    )

    prompt = BULLETS_PROMPT.format(
        original_bullets=formatted_bullets,
        job_description=job_description.strip()
    )

    response = get_openai_response(prompt)
    return response.split("\n")

def generate_full_tailored_resume(job_id: str, resume_data: dict, job_description: str) -> str:
    resume_data = {
        "name": "Yemi Ajibola",
        "email": "yemi@example.com",
        "phone": "555-123-4567",
        "skills": ["Swift", "SwiftUI", "Xcode", "MVVM", "Combine"],
        "summary": "Experienced software engineer with a passion for mobile development and product quality.",
        "experience": [
            {
                "title": "iOS Engineer",
                "company": "Wayfair",
                "dates": "2019–2022",
                "bullets": [
                    "Built reusable SwiftUI components",
                    "Refactored legacy UIKit views into MVVM architecture",
                    "Collaborated with design on prototyping and performance"
                ]
            }
        ]   
    }
    
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