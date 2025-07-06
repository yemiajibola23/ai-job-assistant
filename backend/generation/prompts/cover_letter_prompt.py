
COVER_LETTER_PROMPT = """You are an expert career coach and professional writer. Given a resume and a job description, your task is to generate a tailored, compelling, and concise cover letter. The tone should be professional but warm, and show genuine interest in the company.

    ### Job Description:
    {job_description}

    ### Resume Summary:
    {resume_summary}

    ### Notes (optional):
    {user_notes}

    Write a cover letter that:
    - Is addressed to the hiring manager
    - Introduces the applicant and their interest in the role
    - Highlights relevant experience and skills
    - Reflects the tone of the company
    - Ends with a brief call to action or next step

    Please return only the letter — no preamble, no formatting.
    """

def get_cover_letter_prompt(data: dict) -> str:
    return COVER_LETTER_PROMPT.format(
        job_description=data.get("job_description", ""),
        resume_summary=data.get("summary", ""),
        user_notes=data.get("notes", "N/A")
    )

