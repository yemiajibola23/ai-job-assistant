# backend/generation/export/tailored_resume_exporter.py

from pathlib import Path
from backend.generation.prompts.tailored_resume_prompt import tailor_resume_data
from backend.generation.generators.cover_letter_generator import CoverLetterGenerator
from backend.generation.client.openai_client import client
from backend.generation.templates.jinja_env import get_jinja_env
from backend.generation.save.file_saver import save_to_file
from backend.generation.export.pdf_exporter import convert_markdown_to_pdf

def generate_and_render_tailored_cover_letter(job_id: str, resume_data: dict, job_description: str) -> Path:
    tailored_data = tailor_resume_data(resume_data, job_description)
    
    jinja_env = get_jinja_env()
    generator = CoverLetterGenerator(jinja_env=jinja_env, gpt_client=client)
    markdown = generator.generate(tailored_data)

    md_path = f"output/cover_letters/tailored_cover_letter_{job_id}.md"
    save_to_file(markdown, md_path)

    pdf_path = convert_markdown_to_pdf(md_path)
    return Path(pdf_path)
