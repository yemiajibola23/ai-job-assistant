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
    
def test_extract_query_fields_missing_location():
    parsed_resume = {
        "experience": [{"title": "Junior Backend Developer"}],
        "summary": "Entry-level developer looking for part-time work."
    }

    result = extract_query_fields(parsed_resume)

    assert result.get("job_title")  == "Backend Developer"
    assert result.get("location") == "Remote"  # fallback default
    assert result.get("inferred_level") == "Junior"
    assert result.get("work_type") == "Part-time"
    

def test_extract_query_fields_missing_experience():
    parsed_resume = {
        "summary": "Looking for a contract React Developer role. Based in Chicago, IL.",
        "location": "Chicago, IL"
    }

    try:
        extract_query_fields(parsed_resume)
        assert False, "Should raise KeyError when experience is missing"
    except (KeyError, IndexError):
        pass  # expected

def test_extract_query_fields_unclear_level():
    parsed_resume = {
        "experience": [{"title": "Software Engineer"}],
        "location": "New York, NY",
        "summary": "Skilled engineer seeking new opportunities"
    }

    result = extract_query_fields(parsed_resume)

    assert result["job_title"] == "Software Engineer"
    assert result["inferred_level"] == "Mid"
    assert "work_type" not in result  # no signal found