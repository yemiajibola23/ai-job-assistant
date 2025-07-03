from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Set the path to the templates directory
template_dir = Path(__file__).parent / "jinja_templates"
env = Environment(loader=FileSystemLoader(str(template_dir)))
