from markdown2 import markdown
from weasyprint import HTML
from pathlib import Path

def convert_markdown_to_pdf(markdown_path: str) -> str:
    output_dir = Path("output/pdf")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(markdown_path, "r", encoding="utf-8") as f:
        html = markdown(f.read())

    job_id = Path(markdown_path).stem.replace("tailored_resume_", "")
    pdf_path = output_dir / f"tailored_resume_{job_id}.pdf"
    HTML(string=html).write_pdf(str(pdf_path))

    return str(pdf_path)
