# backend/utils/constants.py

APPLICATION_STATUSES = [
    "Interested",
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Saved",
]

DEFAULT_SCORE_THRESHOLD = 0.75
TEST_RESUME_PATH = "tests/data/yemi_resume.pdf"

EMPTY_RESULT_DICT =  {
    "filled_fields": [],
    "skipped_fields": [],
    "uploaded_files": {},
    "essays_filled": [],
    "errors": [],
    "clicked_submit": False,
    "confirmation_found": False
}

TEST_JOB_DICT = {
    "job_id": "4582524005",
    "job_title": "iOS Engineer",
    "company_name": "Grow Therapy",
    "location": "Seattle, WA (Hybrid – 3x/week)",
    "job_url": "https://job-boards.greenhouse.io/growtherapy/jobs/4582524005?gh_src=8d47tscl5us",
    "job_description": (
        "Grow Therapy is building its first mobile application and is looking for an iOS Engineer to help lead development. "
        "In this role, you'll design, build, and maintain an advanced iOS application using Swift, working closely with a team "
        "of product managers, designers, and engineers. You will own architectural decisions, implement new features, and ensure "
        "a high-quality user experience. The app will support therapists and patients across Grow’s marketplace. This is a hybrid "
        "role based in Seattle, WA, with an expectation of working in the office 3x per week."
    ),
    "job_posted_at": "2025-07-11",  # Approximate based on your query date
    "job_type": "Full-time",
    "industry": "Mental Health / Telehealth / Marketplace",
    "job_tags": [
        "Swift",
        "UIKit",
        "Core Animation",
        "Core Data",
        "Mobile Architecture",
        "Apple Store Review Process",
        "AI Productivity Tools",
        "Cross-functional Collaboration",
        "Seattle Hybrid"
    ],
    "job_board": "Greenhouse",
    "resume_path": "tests/data/yemi_resume.pdf"
}
