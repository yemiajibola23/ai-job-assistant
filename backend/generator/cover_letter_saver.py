import re
import os
from datetime import datetime

def sanitize_filename(text: str) -> str:
    """Make filename readable."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text.lower().strip()[:50])

def save_cover_letter(content: str, job_title: str, company: str, folder: str="output/cover_letters") -> str:
        """
    Saves the generated cover letter to a markdown file.

    Args:
        content (str): The cover letter text.
        job_title (str): Title of the job for filename context.
        company (str): Company name for filename context.
        folder (str): Directory to save file to.

    Returns:
        str: Path to the saved file.
    """
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d %H%M%S")

        filename = f"{sanitize_filename(company)}_{sanitize_filename(job_title)}_timestamp.md"
        path = os.path.join(folder, filename)

        with open(path, "w") as f:
              f.write(content)
        
        return path
