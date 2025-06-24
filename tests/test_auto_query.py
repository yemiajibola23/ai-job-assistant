import pytest
from backend.job_search.auto_query import run_auto_query
from backend.utils.constants import TEST_RESUME_PATH
from pathlib import Path
from backend.db.connection import get_connection
from backend.db.schema import create_jobs_table

def test_run_auto_query():
    conn = get_connection(Path("test-job-assistant.db"))  # isolated DB
    cursor = conn.cursor()
    cursor.execute(create_jobs_table)

    result = run_auto_query(TEST_RESUME_PATH, conn)

    assert isinstance(result["query"], str)
    assert(len(result["query"]) > 0)


    assert isinstance(result["matches"], list)
    assert len(result["matches"]) > 0
    assert isinstance(result["matches"][0], dict)

    assert isinstance(result["saved_count"], int)
    assert 0 <= result["saved_count"] <= len(result["matches"])

    conn.close()
    Path("test-job-assistant.db").unlink(missing_ok=True)
