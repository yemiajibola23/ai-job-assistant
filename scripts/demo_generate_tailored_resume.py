import argparse
from pathlib import Path
import json

from backend.generation.prompts.tailored_resume_prompt import tailor_resume_data, get_resume_prompt
from backend.generation.generators.resume_generator import ResumeGenerator
from backend.generation.client.openai_client import client  # Make sure this aligns with your GPT usage
from backend.generation.templates.jinja_env import get_jinja_env  # Assumes you have a shared Jinja loader setup


def load_resume_data(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_job_description(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def save_output(markdown: str, job_id: str) -> Path:
    output_dir = Path("output/resumes")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"tailored_resume_{job_id}.md"
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def main(resume_path: str, jd_path: str, job_id: str):
    base_data = load_resume_data(Path(resume_path))
    job_description = load_job_description(Path(jd_path))

    tailored_data = tailor_resume_data(base_data, job_description)

    jinja_env = get_jinja_env()
    generator = ResumeGenerator(jinja_env=jinja_env, gpt_client=client)
    markdown = generator.generate(tailored_data)

    out_path = save_output(markdown, job_id)
    print(f"✅ Resume saved to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a tailored resume for a specific job.")
    parser.add_argument("--resume", required=True, help="Path to base resume JSON")
    parser.add_argument("--jd", required=True, help="Path to job description text file")
    parser.add_argument("--job_id", required=True, help="Job ID to use in output filename")

    args = parser.parse_args()
    main(resume_path=args.resume, jd_path=args.jd, job_id=args.job_id)
