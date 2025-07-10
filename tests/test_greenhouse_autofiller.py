import pytest
from unittest.mock import AsyncMock, call
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
