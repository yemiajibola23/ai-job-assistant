from unittest.mock import Mock, AsyncMock, MagicMock, patch 
from backend.autofill.playwright_autofiller import PlaywrightAutofiller

# Patch the path where sync_playwright is used (not where it's defined)
@patch("backend.autofill.playwright_autofiller.sync_playwright")
def test_fill_form_calls_playwright_methods(mock_sync_playwright):
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page =  MagicMock()
    mock_field = MagicMock()
    
    mock_page.query_selector_all.return_value = [mock_field]
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context

    mock_pw = MagicMock()
    mock_pw.chromium.launch.return_value = mock_browser
    mock_sync_playwright.return_value.__enter__.return_value = mock_pw

    application_data ={
        "name": "Test User",
        "email": "test@example.com"
    }

    engine = PlaywrightAutofiller(job_url="https://example.com")
    engine.fill_form(application_data)

    mock_page.goto.assert_called_once_with("https://example.com")
    mock_page.query_selector_all.assert_called_once()
    mock_field.fill.assert_called()