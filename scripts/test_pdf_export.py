from generation.resume import generate_full_tailored_resume
from generation.export import convert_markdown_to_pdf

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

md_path = generate_full_tailored_resume("pdf_test", resume_data, job_description)
pdf_path = convert_markdown_to_pdf(md_path)

print(f"✅ PDF exported to: {pdf_path}")
