# tests/conftest.py
import logging
from pathlib import Path
from backend.db.connection import get_connection
from backend.db.schema import create_jobs_table, create_seen_jobs_table, create_applications_table
import pytest


def pytest_configure(config):
    # Force suppression of noisy external loggers
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("sentence_transformers").setLevel(logging.CRITICAL)
    logging.getLogger("transformers").setLevel(logging.CRITICAL)
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)

def setup_test_db(db_path: Path):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(create_jobs_table)
    cursor.execute(create_seen_jobs_table)
    cursor.execute(create_applications_table)
    return conn

@pytest.fixture
def test_db_connection(tmp_path):
    db_path = tmp_path / "test-job-assistant.db"
    conn = setup_test_db(db_path)
    yield conn
    conn.close()
