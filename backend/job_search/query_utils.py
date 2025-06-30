def extract_query_fields(parsed_resume: dict) -> dict:
    print(f"📝 Resume dict: {parsed_resume}")
    job_title = parsed_resume["experience"][0]["title"]
    location = parsed_resume.get("location", "Remote")
    summary = parsed_resume.get("summary", "").lower()
    
    work_type = None
    if "full-time" in summary:
        work_type = "Full-time"
    elif "contract" in summary:
         work_type = "Contract"
    
    query_dict = {
        "job_title": job_title,
        "location": location
    }
    
    if work_type:
        query_dict["work_type"] = work_type
    
    return query_dict
