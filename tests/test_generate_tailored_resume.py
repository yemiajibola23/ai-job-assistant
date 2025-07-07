import pytest
from unittest.mock import MagicMock, patch
from jinja2 import Environment, FileSystemLoader
from backend.generation.generators.resume_generator import ResumeGenerator
import os
import logging
from jinja2.exceptions import TemplateError

def test_generate_uses_jinja_if_successful():
    mock_template = MagicMock()
    mock_template.render.return_value = "Mock Resume Markdown"
    
    mock_jinja_env = MagicMock()
    mock_jinja_env.get_template.return_value = mock_template 
    
    gpt_mock = MagicMock()
    
    generator = ResumeGenerator(mock_jinja_env, gpt_mock)
    
    data = {"name": "Yemi", "summary": "Senior iOS dev"}
    result = generator.generate(data)
    
    assert result == "Mock Resume Markdown"
    gpt_mock.chat_completions_create.assert_not_called()
    
def test_generate_falls_back_on_gpt_on_jinja_failure():
    mock_template = MagicMock()
    mock_template.render.side_effect = TemplateError("Simulated render failure")
    
    mock_jinja_env = MagicMock()
    mock_jinja_env.get_template.return_value = mock_template
    
    gpt_mock = MagicMock()
    gpt_mock.generate.return_value = "GPT fallback resume"
    
    generator = ResumeGenerator(mock_jinja_env, gpt_mock)
    
    data = {"name": "Yemi", "summary": "Senior iOS dev"}
    result = generator.generate(data)
    
    assert result == "GPT fallback resume"

@patch.object(ResumeGenerator, "generate_tailored_bullets")
@patch.object(ResumeGenerator, "generate_tailored_summary")
def test_tailor_resume_data(mock_tailored_summary, mock_tailored_bullets):
    mock_tailored_summary.return_value = "Really good at iOS Development"
    mock_tailored_bullets.return_value = ["Bullet1", "Bullet2", "Bullet3", "Bullet4"]
        
    mock_jinja_env = MagicMock()
    gpt_mock = MagicMock()

    input_data = {
        "summary": "Old summary",
        "experience": [
            {"company": "Company A", "bullets": ["a1", "a2"]},
            {"company": "Company B", "bullets": ["b1", "b2"]}
        ],
        "education": ["BS in CS"],
        "skills": ["Swift"]
    }
    
    generator = ResumeGenerator(mock_jinja_env, gpt_mock)

    result = generator.tailor_resume_data(input_data, job_description="iOS job")

    assert result["summary"] == "Really good at iOS Development"
    
    assert len(result["experience"]) == 2
    assert result["experience"][0]["bullets"] == ["Bullet1", "Bullet2"]
    assert result["experience"][1]["bullets"] == ["Bullet3", "Bullet4"]
    assert result["education"] == ["BS in CS"]  # Pass-through

    # Ensure the job description influenced the tailoring
    print(mock_tailored_summary.call_args)
    # Summary was tailored using correct job description (keyword args)
    assert mock_tailored_summary.call_args.kwargs["job_description"] == "iOS job"

    # Bullets were tailored using correct job description (positional args)
    assert mock_tailored_bullets.call_args[0][1] == "iOS job"


    