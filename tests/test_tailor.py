import pytest
from backend.generator.services.generate_tailored_resume import generate_tailored_summary

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