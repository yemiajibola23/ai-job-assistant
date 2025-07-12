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