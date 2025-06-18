import pytest
from unittest.mock import patch
from pathlib import Path
import backend.generator.services.generate_tailored_resume as resume_module

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

    with patch.object(resume_module, "generate_tailored_summary", return_value="Tailored summary"), \
         patch.object(resume_module, "generate_tailored_bullets", return_value=["Bullet A", "Bullet B"]):

        output_path = resume_module.generate_full_tailored_resume("ios123", resume_data, job_description)

        # Ensure the file exists
        assert Path(output_path).exists()

        # Check content
        content = Path(output_path).read_text()
        assert "Tailored summary" in content
        assert "- Bullet A" in content
        assert "Swift, SwiftUI, Xcode" in content