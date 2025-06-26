from backend.notion.service import push_to_notion
jobs = [
    {
        "job_title": "Senior iOS Engineer",
        "company_name": "Flock Safety",
        "location": "Remote, Atlanta",
        "job_url": "https://jobs.flocksafety.com/senior-ios",
        "status": "Interviewing",
        "level": "Senior",
        "interview_stage": "Technical Interview"
    },
    {
        "job_title": "Mobile Engineer",
        "company_name": "Doist",
        "location": "Remote",
        "job_url": "https://doist.notion.site/mobile-job",
        "status": "Waiting for confirmation",
        "level": "Mid",
        "interview_stage": "Recruiter Call"
    },
    {
        "job_title": "iOS Developer",
        "company_name": "Apple",
        "location": "Cupertino",
        # Missing job_url to trigger failure
        "status": "Applied",
        "level": "Entry",
        "interview_stage": "Recruiter Call"
    }
]


result = push_to_notion(jobs)
print(result)