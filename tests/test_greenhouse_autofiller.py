import pytest
from unittest.mock import AsyncMock, call, patch
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller

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
    
    result= {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }

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
    
    result= {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }
        
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

    result = {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }

    # Act
    await autofiller.upload_documents(mock_page, data, result)

    # Assert
    mock_page.set_input_files.assert_called_with('input#cover_letter', "/path/to/cover_letter")
    assert result["uploaded_files"]["cover_letter"] == "/path/to/cover_letter"
    
    
    import pytest
from unittest.mock import AsyncMock, patch, call
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller

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

    result = {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }

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

    result = {
        "filled_fields": [],
        "skipped_fields": [],
        "uploaded_files": {},
        "errors": [],
        "clicked_submit": False,
        "confirmation_found": False
    }

    # Act
    await autofiller.upload_documents(mock_page, data, result)

    # Assert
    mock_page.click.assert_called_once()
    mock_page.set_input_files.assert_has_calls([
        call('input#resume', "/path/to/resume"),
        call('input[type="file"]', "/path/to/resume")
    ])
    assert result["uploaded_files"]["resume"] == "/path/to/resume"
