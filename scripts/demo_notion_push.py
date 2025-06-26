from backend.notion.service import create_page

job = {
    "job_title": "Senior iOS Engineer",
    "company_name": "Flock Safety",
    "location": "Remote, Atlanta",
    "job_url": "https://jobs.flocksafety.com/senior-ios",
    "status": "Interviewing",
    "level": "Senior",
    "interview_stage": "Technical Interview"
}

create_page(job)