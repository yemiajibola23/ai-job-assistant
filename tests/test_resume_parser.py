import os
from backend.resume.resume_parser import extract_text_from_pdf, parse_resume_text

def test_parse_resume_text_extracts_fields():
    sample_path = os.path.join(os.path.dirname(__file__), "data", "yemi_resume.pdf")
    text = extract_text_from_pdf(sample_path)
    result = parse_resume_text(text)

    assert result["email"] is not None, "Email not found"
    assert result["phone"] is not None, "Phone not found"
    assert result["name"] is not None, "Name not found"
    assert "raw_text" in result

    # Optional: precise name test
    expected_name = "Yemi Ajibola"  # replace with actual name in your PDF
    assert result["name"].lower() == expected_name.lower(), f"Expected name '{expected_name}' but got '{result['name']}'"

def test_parse_resume_text_extracts_skills():
    sample_path = os.path.join(os.path.dirname(__file__), "data", "yemi_resume.pdf")
    text = extract_text_from_pdf(sample_path)
    result = parse_resume_text(text)

    assert "swift" in result["skills"]
    assert "swiftui" in result["skills"]
    assert "kubernetes" not in result["skills"]