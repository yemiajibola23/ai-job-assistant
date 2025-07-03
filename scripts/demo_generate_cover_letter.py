from backend.generation.generators.cover_letter_generator import CoverLetterGenerator
from backend.generation.client.openai_client import OpenAIClient
from backend.generation.export.pdf_exporter import convert_markdown_to_pdf
from backend.generation.templates.jinja_env import env

def main():
    generator = CoverLetterGenerator(jinja_env=env, gpt_client=OpenAIClient())

    data = {
        "hiring_manager": "Jane Doe",
        "job_title": "Backend Engineer",
        "company_name": "OpenAI",
        "skills": "Python, distributed systems, async processing, REST APIs, container orchestration, cloud deployments, system design",
        "custom_paragraph": "I'm especially drawn to your mission.",
        "applicant_name": "Yemi Ajibola",
        "resume_summary": "Experienced iOS engineer with Swift, SwiftUI, and MVVM expertise.",
        "job_description": "We're hiring a mobile engineer to lead iOS development on our next-gen app.",
        "user_notes": "Mention excitement about health tech and experience with push notifications."
    }

    markdown = generator.generate(data)

    # Save markdown temporarily
    md_path = f"output/temp_cover_letter_demo.md"
    with open(md_path, "w") as f:
        f.write(markdown)

    pdf_path = convert_markdown_to_pdf(md_path)
    print(f"✅ Cover letter exported to: {pdf_path}")

if __name__ == "__main__":
    main()
