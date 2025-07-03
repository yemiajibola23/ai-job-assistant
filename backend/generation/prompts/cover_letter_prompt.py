def get_cover_letter_prompt(data: dict) -> str:
    # Fill in with prompt generation logic if Jinja fallback fails
    return f"Write a cover letter for {data.get('job_title', 'a job')}"
