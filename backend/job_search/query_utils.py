import re

def extract_query_fields(parsed_resume: dict) -> dict:
    print(f"📝 Resume dict: {parsed_resume}")
    raw_title = parsed_resume["experience"][0]["title"]
    location = parsed_resume.get("location", "Remote")
    summary = parsed_resume.get("summary", "").lower()
    
    work_type = None
    if "full-time" in summary:
        work_type = "Full-time"
    elif "contract" in summary:
         work_type = "Contract"
    elif "part-time" in summary:
        work_type = "Part-time"
         
    title_lower = raw_title.lower()
    if "senior" in title_lower or "lead" in title_lower:
        inferred_level = "Senior"
    elif "junior" in title_lower or "entry" in title_lower:
        inferred_level = "Junior"
    else:
        inferred_level = "Mid"
        
    stripped_title = re.sub(r"\b(senior|lead|junior|entry[- ]level)\b", "", raw_title, flags=re.IGNORECASE).strip()
    stripped_title = re.sub(r"\s{2,}", " ", stripped_title)  # clean up extra spaces
    
    query_dict = {
        "job_title": stripped_title,
        "location": location,
        "inferred_level": inferred_level
    }
    
    if work_type:
        query_dict["work_type"] = work_type
    
    return query_dict
