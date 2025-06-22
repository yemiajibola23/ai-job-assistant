from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from generation.export import convert_markdown_to_pdf
from backend.generation.prompts import COVER_LETTER_PROMPT

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover_letter(resume_summary: str, job_description: str, user_notes: str = "") -> str:
    """
    Generates a cover letter tailored to a job description and resume summary.

    Args:
        resume_summary (str): Extracted or summarized resume text.
        job_description (str): Full job posting or relevant excerpt.
        user_notes (str, optional): Any extra instructions (e.g., tone, specific experiences to mention).

    Returns:
        str: Generated cover letter.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": COVER_LETTER_PROMPT}
        ],
        temperature=0.7,
        max_tokens=500
    )

    content = response.choices[0].message.content
    return content.strip() if content else "[ERROR] No content returned by GPT."

def generate_cover_letter_file(job_id: str, resume_summary: str, job_description: str, user_notes: str = ""):
    content = generate_cover_letter(resume_summary, job_description, user_notes)

    output_dir = Path("output/cover_letters")
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / f"cover_letter_{job_id}.md"
    path.write_text(content.strip(), encoding="utf-8")

    return str(path)

def generate_cover_letter_pdf(job_id: str, resume_summary: str, job_description: str, user_notes: str = ""):
    md_path = generate_cover_letter_file(job_id, resume_summary, job_description, user_notes)
    pdf_path =  convert_markdown_to_pdf(md_path)

    return pdf_path