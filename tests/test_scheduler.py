from unittest.mock import Mock, patch
from backend.utils.scheduler import run_scheduler_job
from backend.db import job_dao

def test_run_scheduler_job_adds_new_job_and_notifies():
    mock_conn = Mock()

    job = {"id": "abc123", "title": "Software Engineer"}
    job_fetcher = Mock(return_value=[job])

    job_dao.has_seen_job = Mock(return_value=False)
    job_dao.mark_job_as_seen = Mock()

    handler = Mock()
    notifier = Mock()

    with patch("backend.utils.scheduler.has_seen_job", return_value=False), \
        patch("backend.utils.scheduler.mark_job_as_seen") as mock_mark_seen:

        run_scheduler_job(mock_conn, job_fetcher, handler, notifier)

        handler.assert_called_once_with([job])
        notifier.assert_called_once_with("🆕 1 new jobs")
        mock_mark_seen.assert_called_once_with(mock_conn, "abc123")


    