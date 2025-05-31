from backend.resume.resume_parser import extract_text_from_pdf, parse_resume_text

pdf_path = "tests/data/yemi_resume.pdf"
text = extract_text_from_pdf(pdf_path)
parsed = parse_resume_text(text)

print("=== Parsed Resume Data ===")
print(parsed)