from backend.generation.generators.resume_generator import get_resume_prompt
from backend.generation.export.pdf_exporter import convert_markdown_to_pdf
from backend.generation.generators.resume_generator import ResumeGenerator
from backend.generation.templates.jinja_env import get_jinja_env
from backend.generation.client.openai_client import client

def main():
    # existing logic here
    resume_data = {
        "name": "Yemi Ajibola",
        "email": "yemi@example.com",
        "phone": "555-123-4567",
        "skills": ["Swift", "SwiftUI", "Xcode"],
        "summary": "Base summary for PDF test",
        "experience": [
            {"bullets": ["Built scalable iOS features", "Led SwiftUI adoption"]}
        ]
    }

    job_description = "Looking for an iOS engineer with Swift, SwiftUI, and MVVM experience."

    resume_generator = ResumeGenerator(get_jinja_env(), client)
    md_path = resume_generator.generate_full_tailored_resume("pdf_test", resume_data, job_description)
    pdf_path = convert_markdown_to_pdf(md_path)

    print(f"✅ PDF exported to: {pdf_path}")

if __name__ == "__main__":
    main()