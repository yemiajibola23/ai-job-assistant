ESSAY_PROMPT = """
You are helping a candidate answer a job application question.
The job is for a {job_title} role at {company}.
Here is their resume summary:\n{resume_summary}
Now answer the following question in 3–5 professional sentences: {label}
"""


def get_essay_prompt(data: dict) -> str:
    label = data.get("label", "Why do you want this job?")
    job_title = data.get("job_title", "this role")
    company = data.get("company", "the company")
    resume_summary = data.get("summary", "")

    return ESSAY_PROMPT.format(job_title, company, resume_summary, label)