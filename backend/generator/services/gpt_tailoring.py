from generator.prompts.summary_prompt import SUMMARY_PROMPT
from generator.prompts.bullets_prompt import BULLETS_PROMPT
from .openai_client import get_openai_response
import re

def generate_tailored_summary(base_summary: str, job_description: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        base_summary=base_summary.strip(),
        job_description=job_description.strip()
    )
    
    return get_openai_response(prompt)

def generate_tailored_bullets(experience_bullets: list[str], job_description: str) -> list[str]:
    formatted_bullets = "\n".join(experience_bullets)

    prompt = BULLETS_PROMPT.format(
        original_bullets=formatted_bullets,
        job_description=job_description.strip()
    )

    response = get_openai_response(prompt)
    raw_bullets = response.split("\n")

    # Strip leading numbering like "1. ", "2. ", etc.
    clean_bullets = [re.sub(r"^\s*\d+\.\s*", "", b).strip() for b in raw_bullets if b.strip()]

    return clean_bullets
