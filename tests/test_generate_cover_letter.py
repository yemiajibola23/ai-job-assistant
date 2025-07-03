import pytest
from unittest.mock import MagicMock, patch
from jinja2 import Environment, FileSystemLoader
from backend.generation.generators.cover_letter_generator import CoverLetterGenerator
import os

@pytest.fixture
def jinja_env():
    template_path = os.path.join("backend", "generation", "templates", "jinja_templates")
    return Environment(loader=FileSystemLoader(template_path))

def test_jinja_success_path(jinja_env):
    gpt_mock = MagicMock()
    generator = CoverLetterGenerator(jinja_env, gpt_mock)
    
    data = {
        "hiring_manager": "Jane Doe",
        "job_title": "Backend Engineer",
        "company_name": "OpenAI",
        "skills": "Python, distributed systems, async processing, REST APIs, container orchestration, cloud deployments, system design",
        "custom_paragraph": "I'm especially drawn to your mission.",
        "applicant_name": "Yemi Ajibola"
    }
    
    with patch.object(generator, "_is_sufficient", return_value=True):
        result = generator.generate(data)
    
    assert "Dear Jane Doe" in result
    assert "Backend Engineer" in result
    gpt_mock.assert_not_called()
    
def test_gpt_fallback_path(jinja_env):
    gpt_mock = MagicMock()
    gpt_mock.generate.return_value = "GPT-generated cover letter"

    generator = CoverLetterGenerator(jinja_env, gpt_mock)
    data = {
        "company_name": "OpenAI"  # intentionally sparse
    }

    with patch.object(generator, "_is_sufficient", return_value=False):
        result = generator.generate(data)

    assert result == "GPT-generated cover letter"
    gpt_mock.generate.assert_called_once()
