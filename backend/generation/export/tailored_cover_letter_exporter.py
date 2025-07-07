# backend/generation/export/tailored_resume_exporter.py

from pathlib import Path
from backend.generation.save.file_saver import save_to_file
from backend.generation.export.pdf_exporter import convert_markdown_to_pdf

def generate_and_render_tailored_cover_letter(job_id: str, resume_data: dict, job_description: str, tailored_data: dict, cover_letter_generator) -> Path:    
    markdown = cover_letter_generator.generate(tailored_data)

    md_path = f"output/cover_letters/tailored_cover_letter_{job_id}.md"
    save_to_file(markdown, md_path)

    pdf_path = convert_markdown_to_pdf(md_path)
    return Path(pdf_path)
