import pytest
from scripts.auto_query import run_auto_query
from backend.utils.constants import TEST_RESUME_PATH

def test_run_auto_query(test_db_connection):

    result = run_auto_query(TEST_RESUME_PATH, test_db_connection)

    assert isinstance(result["query"], str)
    assert(len(result["query"]) > 0)


    assert isinstance(result["matches"], list)
    assert len(result["matches"]) > 0
    assert isinstance(result["matches"][0], dict)

    assert isinstance(result["saved_count"], int)
    assert 0 <= result["saved_count"] <= len(result["matches"])