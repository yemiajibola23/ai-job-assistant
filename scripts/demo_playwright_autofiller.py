from backend.autofill.playwright_autofiller import PlaywrightAutofiller
from pathlib import Path
import argparse
import logging

# Set logging level to DEBUG for all loggers
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true", help="Run autofill without submitting application")
args = parser.parse_args()

def main():
    application_data = {
        "name": "Yemi Ajibola",
        "email": "yemi@example.com",
        "phone": "555-123-4567",
        "linkedin": "https://linkedin.com/in/yemi",
        "resume": str(Path("/tests/data/yemi_resume.pdf").resolve()),
        "cover_letter": str(Path("/path/to/test_cover_letter.pdf").resolve())
    }

    job_url = "https://job-boards.greenhouse.io/speechify/jobs/5411578004"

    autofiller = PlaywrightAutofiller(job_url)
    result = autofiller.fill_form(application_data, dry_run=args.dry_run)

    print("=== Result Log ===")
    for key, val in result.items():
        print(f"{key}: {val}")

if __name__ == "__main__":
    main()