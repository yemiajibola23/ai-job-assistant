import spacy

def parse_query(query: str) -> dict:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)

    JOB_TITLES = ["ios engineer", "android developer", "backend engineer", "frontend engineer", "data scientist"]

    location = next((ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"), None)
    work_type = "remote" if "remote" in query.lower() else None
    level = "senior" if "senior" in query.lower() else None
    job_title = next((title for title in JOB_TITLES if title in query.lower()), None)
    
    return {
        "job_title": job_title,
        "location": location,
        "work_type": work_type,
        "level": level,
    }