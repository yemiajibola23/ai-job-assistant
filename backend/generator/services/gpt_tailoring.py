from generator.prompts.summary_prompt import SUMMARY_PROMPT
from generator.prompts.bullets_prompt import BULLETS_PROMPT
from .openai_client import get_openai_response

def generate_tailored_summary(base_summary: str, job_description: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        base_summary=base_summary.strip(),
        job_description=job_description.strip()
    )
    
    return get_openai_response(prompt)

def generate_tailored_bullets(experience_bullets: list[str], job_description: str) -> list[str]:
    formatted_bullets = "\n".join(
        [f"{i}. {b}" for i, b in enumerate(experience_bullets, start=1)]
    )

    prompt = BULLETS_PROMPT.format(
        original_bullets=formatted_bullets,
        job_description=job_description.strip()
    )

    response = get_openai_response(prompt)
    return response.split("\n")
