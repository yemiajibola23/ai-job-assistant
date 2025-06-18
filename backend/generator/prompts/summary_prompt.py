SUMMARY_PROMPT = """
You are an expert technical resume writer.

Given the following original resume summary and job description, rewrite the summary so that it highlights the most relevant skills, technologies, and experiences for the job. Keep it professional, confident, and concise.

Be sure to:
- Use keywords and language from the job description
- Keep it under 4 sentences
- Maintain a natural human tone (not robotic)

---

Original Resume Summary:
{base_summary}

---

Target Job Description:
{job_description}

---

Rewritten Summary:
"""
