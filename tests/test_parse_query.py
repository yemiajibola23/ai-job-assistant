from backend.job_search.parse_query import parse_query

def test_parse_query_extracts_fields_from_input():
    query = "Looking for remote Senior iOS Engineer role in Berlin"

    result = parse_query(query)

    assert result["job_title"] == "ios engineer"
    assert result["location"] == "berlin"
    assert result["work_type"] == "remote"
    assert result["level"] == "senior"