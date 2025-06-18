
import pytest
from backend.generator.services.gpt_tailoring import generate_tailored_summary, generate_tailored_bullets

def test_generate_tailored_summary_returns_rewritten_text():
    # Arrange
    base_summary = (
        "Experienced software engineer with a background in mobile and web development. "
        "Skilled in building scalable applications and collaborating with cross-functional teams."
    )

    job_description = (
        "We're seeking a Senior iOS Engineer to help us build intuitive, high-performance apps using Swift and SwiftUI. "
        "Experience with async/await, modular architectures, and XCTest is required. "
        "Bonus if you’ve worked with Combine or push notifications."
    )

    # Act
    result = generate_tailored_summary(base_summary, job_description)

    # Assert
    # Replace with your test expectations
    assert isinstance(result, str)
    assert result != base_summary
    assert "Swift" in result


def test_generate_tailored_bullets_returns_aligned_bullets():
    # Arrange
    bullets = [
        "Developed scalable APIs for internal services.",
        "Led weekly code reviews and mentored junior engineers.",
        "Collaborated with frontend team on React integration."
    ]

    job_description = (
        "We're hiring a backend engineer with experience in building RESTful APIs, "
        "working with async Python, and deploying services with Docker. "
        "Familiarity with mentoring and team leadership is a plus."
    )

    # Act
    result = generate_tailored_bullets(bullets, job_description)

    # Assert
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(b, str) for b in result)
    assert any("API" in b or "Docker" in b or "Python" in b for b in result)
