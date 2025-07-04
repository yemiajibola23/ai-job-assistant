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