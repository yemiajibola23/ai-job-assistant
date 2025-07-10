import pytest
from unittest.mock import AsyncMock, call, patch
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller
from backend.utils.constants import EMPTY_RESULT_DICT

@pytest.mark.asyncio
async def test_fill_basic_info_fills_fields_correctly():
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    data = {
        "first_name": "LeBron",
        "last_name": "James",
        "email": "lebron@example.com",
        "phone": "555-1234",
    }
    
    result= EMPTY_RESULT_DICT
    
    # Act
    await autofiller.fill_basic_info(mock_page, data, result)

    # Assert: page.fill called with correct xpaths
    calls = [
        ("xpath=//*[@id=\"first_name\"]", "LeBron"),
        ("xpath=//*[@id=\"last_name\"]", "James"),
        ("xpath=//*[@id=\"email\"]", "lebron@example.com"),
        ("xpath=//*[@id=\"phone\"]", "555-1234"),
    ]
    mock_page.fill.assert_has_calls([call(xpath, value) for xpath, value in calls], any_order=True)

    # Assert: result updated
    assert set(result["filled_fields"]) == {"first_name", "last_name", "email", "phone"}
    assert result["skipped_fields"] == []
    assert result["errors"] == []

@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_successfully_uploads_resume(mock_path_exists):
    
     # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()
    
    data = {
        "resume_path": "/path/to/resume"
    }
    
    result= EMPTY_RESULT_DICT
        
    await autofiller.upload_documents(mock_page, data, result)
    
    mock_page.set_input_files.assert_called_with('input#resume', "/path/to/resume")    
    assert result["uploaded_files"]["resume"] == "/path/to/resume"
    
    
@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_successfully_uploads_cover_letter(mock_exists):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    data = {
        "cover_letter_path": "/path/to/cover_letter"
    }
    
    result= EMPTY_RESULT_DICT

    # Act
    await autofiller.upload_documents(mock_page, data, result)

    # Assert
    mock_page.set_input_files.assert_called_with('input#cover_letter', "/path/to/cover_letter")
    assert result["uploaded_files"]["cover_letter"] == "/path/to/cover_letter"
    
@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_fallback_upload_cover_letter(mock_exists):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    # Simulate direct upload failure on first call, success on fallback
    mock_page.set_input_files = AsyncMock(side_effect=[
        Exception("Simulated direct upload failure"),  # for input#cover_letter
        None  # for fallback input[type="file"]
    ])
    mock_page.click = AsyncMock()

    data = {
        "cover_letter_path": "/path/to/cover_letter"
    }

    result= EMPTY_RESULT_DICT

    # Act
    await autofiller.upload_documents(mock_page, data, result)

    # Assert
    mock_page.click.assert_called_once()
    mock_page.set_input_files.assert_has_calls([
        call('input#cover_letter', "/path/to/cover_letter"),
        call('input[type="file"]', "/path/to/cover_letter")
    ])
    assert result["uploaded_files"]["cover_letter"] == "/path/to/cover_letter"


@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_fallback_upload_resume(mock_exists):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    # Simulate direct upload failure, fallback succeeds
    mock_page.set_input_files = AsyncMock(side_effect=[
        Exception("Simulated direct upload failure"),  # for input#resume
        None  # for fallback input[type="file"]
    ])
    mock_page.click = AsyncMock()

    data = {
        "resume_path": "/path/to/resume"
    }

    result = EMPTY_RESULT_DICT

    # Act
    await autofiller.upload_documents(mock_page, data, result)

    # Assert
    mock_page.click.assert_called_once()
    mock_page.set_input_files.assert_has_calls([
        call('input#resume', "/path/to/resume"),
        call('input[type="file"]', "/path/to/resume")
    ])
    assert result["uploaded_files"]["resume"] == "/path/to/resume"

@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.try_fill_by_id", return_value=False)
@patch("backend.autofill.greenhouse_autofiller.get_labeled_field_xpath", return_value="//*[@id='veteran_status_fallback']")
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_fill_voluntary_self_id_normalizes_value_and_falls_back(mock_exists, mock_xpath, mock_try_fill):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    data = {
        "veteran_status": "Prefer not to say"
    }

    result = EMPTY_RESULT_DICT

    # Act
    await autofiller.fill_voluntary_self_id(mock_page, data, result)

    # Assert fallback fill was called with normalized value
    mock_page.fill.assert_called_with("xpath=//*[@id='veteran_status_fallback']", "I do not wish to answer")
    assert "veteran_status" in result["filled_fields"]


@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.try_fill_by_id", return_value=True)
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_fill_voluntary_self_id_uses_primary_path_for_normalized_value(mock_exists, mock_try_fill):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()

    data = {
        "veteran_status": "Prefer not to say"
    }

    result = {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }

    # Act
    await autofiller.fill_voluntary_self_id(mock_page, data, result)

    # Assert: primary path was taken
    mock_try_fill.assert_called_with(mock_page, "veteran_status", "I do not wish to answer", result)
    mock_page.fill.assert_not_called()
    assert "veteran_status" not in result["errors"]