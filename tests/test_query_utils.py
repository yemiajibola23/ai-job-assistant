from backend.job_search.query_utils import extract_query_fields

def test_extract_query_fields_happy_path():
    parsed_resume = {
        "name": "Yemi Ajibola",
        "location": "St. Louis, MO",
        "experience": [
            {"title": "Senior iOS Engineer", "company": "Eight Sleep", "years": 2},
            {"title": "iOS Developer", "company": "Wayfair", "years": 3},
        ],
        "summary": "Experienced iOS developer with 6+ years building Swift apps. Looking for full-time opportunities.",
    }

    expected = {
        "job_title": "iOS Engineer",
        "location": "St. Louis, MO",
        "work_type": "Full-time",
        "inferred_level": "Senior"
    }

    result = extract_query_fields(parsed_resume)
    assert result == expected