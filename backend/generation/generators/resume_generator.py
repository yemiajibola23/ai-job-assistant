from backend.generation.generators.base_generator import BaseGenerator
from backend.generation.prompts.tailored_resume_prompt import get_resume_prompt, SUMMARY_PROMPT, BULLETS_PROMPT
import re
from pathlib import Path

class ResumeGenerator(BaseGenerator):
    def __init__(self, jinja_env, gpt_client):
        self.jinja_env = jinja_env
        self.gpt_client = gpt_client
    
    def generate(self, data: dict) -> str:
        try: 
            template = self.jinja_env.get_template('resume.md.j2')
            return template.render(data)
        except Exception as e:
            prompt = get_resume_prompt(data)
            print(e)
            return self.gpt_client.generate(prompt)
    
    def generate_tailored_summary(self, base_summary: str, job_description: str) -> str:
        prompt = SUMMARY_PROMPT.format(
            base_summary=base_summary.strip(),
            job_description=job_description.strip()
        )
    
        return self.gpt_client.generate(prompt)

    def generate_tailored_bullets(self, experience_bullets: list[str], job_description: str) -> list[str]:
        formatted_bullets = "\n".join(experience_bullets)

        prompt = BULLETS_PROMPT.format(
            original_bullets=formatted_bullets,
            job_description=job_description.strip()
        )
        
        response = self.gpt_client.generate(prompt)
        raw_bullets = response.split("\n")

        # Strip leading numbering like "1. ", "2. ", etc.
        clean_bullets = [re.sub(r"^\s*\d+\.\s*", "", b).strip() for b in raw_bullets if b.strip()]

        return clean_bullets

    def tailor_resume_data(self, data: dict, job_description: str) -> dict:
        tailored = data.copy()
    
        # Tailor summary
        tailored["summary"] = self.generate_tailored_summary(
            base_summary=data.get("summary", ""),
            job_description=job_description
        )

        # Tailor bullets for all experience entries
        all_bullets = []
        for job in data.get("experience", []):
            all_bullets.extend(job.get("bullets", []))

        new_bullets = self.generate_tailored_bullets(all_bullets, job_description)

        # Distribute tailored bullets evenly back into jobs
        jobs = data.get("experience", [])
        idx = 0
        for job in jobs:
            num = len(job.get("bullets", []))
            job["bullets"] = new_bullets[idx : idx + num]
            idx += num

        tailored["experience"] = jobs
        return tailored


    def generate_full_tailored_resume(self, job_id: str, resume_data: dict, job_description: str) -> str:
        all_bullets = [bullet for job in resume_data["experience"] for bullet in job["bullets"]]

        tailored_summary = self.generate_tailored_summary(resume_data["summary"], job_description)
        tailored_bullets = self.generate_tailored_bullets(all_bullets, job_description)
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
