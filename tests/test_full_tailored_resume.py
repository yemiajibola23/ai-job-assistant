from unittest.mock import patch
from pathlib import Path
from backend.generation.generators.resume_generator import ResumeGenerator

def test_generate_full_tailored_resume_creates_markdown(tmp_path):
    job_description = "Looking for an iOS engineer with Swift, SwiftUI, and MVVM experience."
    resume_data = {
        "name": "Yemi Ajibola",
        "email": "yemi@example.com",
        "phone": "555-123-4567",
        "skills": ["Swift", "SwiftUI", "Xcode"],
        "summary": "Base summary",
        "experience": [
            {"bullets": ["Old bullet 1", "Old bullet 2"]}
        ]
    }

    mock_env = None  # Or use a dummy Jinja env if needed
    mock_client = type("MockClient", (), {"generate": lambda self, p: "Tailored summary" if "summary" in p else "1. Bullet A\n2. Bullet B"})()

    generator = ResumeGenerator(jinja_env=mock_env, gpt_client=mock_client)

    output_path = generator.generate_full_tailored_resume("ios123", resume_data, job_description)

    # Ensure the file exists
    assert Path(output_path).exists()

    # Check content
    content = Path(output_path).read_text()
    assert "Tailored summary" in content
    assert "- Bullet A" in content
    assert "Swift, SwiftUI, Xcode" in content
