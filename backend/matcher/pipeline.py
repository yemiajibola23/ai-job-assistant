from backend.matcher.matcher import match_resume_to_jobs

def filter_and_match_jobs(jobs: list[dict], resume_text: str, threshold: float = 0.65) -> list[dict]:
    print(f"🪵 Found {len(jobs)} jobs")
    print(f"🪵 Descriptions extracted: {[job.get('description') for job in jobs]}")

    #print(f"🧾 Resume preview:\n{resume_text[:250]}")

    descriptions = [job["description"] for job in jobs]
    ranked_scores = match_resume_to_jobs(resume_text, descriptions, 5)

    desc_to_job = {job["description"]: job for job in jobs}
    for desc, score in ranked_scores:
            job = desc_to_job.get(desc)
            if job:
                job["score"] = score
                job["matched"] = score >= threshold
                if not job["matched"]:
                    job["rejection_reason"] = "score below threshold"
    
    return [job for job in jobs if job.get("matched")]