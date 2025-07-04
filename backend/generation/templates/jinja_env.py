from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def get_jinja_env() -> Environment:
    """
    Loads the Jinja environment pointing to the resume template directory.
    """
    template_dir = Path(__file__).parent / "jinja_templates"
    return Environment(loader=FileSystemLoader(str(template_dir)))
