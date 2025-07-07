# backend/generation/export/tailored_resume_exporter.py

from pathlib import Path
from backend.generation.client.openai_client import client
from backend.generation.save.file_saver import save_to_file
from backend.generation.export.pdf_exporter import convert_markdown_to_pdf

def generate_and_render_tailored_resume(job_id: str, resume_data: dict, job_description: str, generator, tailored_data: dict) -> Path:    
    markdown = generator.generate(tailored_data)

    md_path = f"output/resumes/tailored_resume_{job_id}.md"
    save_to_file(markdown, md_path)

    pdf_path = convert_markdown_to_pdf(md_path)
    return Path(pdf_path)
