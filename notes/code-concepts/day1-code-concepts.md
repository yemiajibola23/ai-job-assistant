# 📘 Day 1 – Code Concepts: Project Setup + Resume Parsing

## 🗂 Project Scaffolding
- Initialized Git repo, `.gitignore`, and virtual environment
- Created structured folder layout for app, backend, and tests
- Established `.env` file and added to `.gitignore` for secrets

## 📚 Dependencies
- Installed core packages: `streamlit`, `openai`, `python-dotenv`, `sentence-transformers`
- Installed `pymupdf` (accessed via `import fitz`) for PDF parsing

## 📄 PDF Text Extraction
- Used PyMuPDF to open and read resume PDF
```python
import fitz
doc = fitz.open("resume.pdf")
text = "".join([page.get_text() for page in doc])
```

## 🧠 Regex-Based Parsing
- Used `re.search()` to extract email and phone:
```python
re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
re.search(r"(\+?\d{1,2}[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}", text)
```

## 🧪 Local Test Setup
- Stored test PDF in `tests/data/`
- Created test script in `tests/test_resume_parser.py`
- Ran tests using: `python -m tests.test_resume_parser`

## 🔍 Debugging & Type Safety
- Used `# type: ignore` to bypass PyMuPDF type warnings
- Fixed module path issues by using `-m` from project root
