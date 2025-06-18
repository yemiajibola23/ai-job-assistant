from .openai_client import get_open_ai_response
from generator.prompts.summary_prompt import SUMMARY_PROMPT

def generate_tailored_summary(base_summary: str, job_description: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        base_summary=base_summary.strip(),
        job_description=job_description.strip()
    )
    
    return get_open_ai_response(prompt)