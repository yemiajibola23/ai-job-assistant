import pytest
from unittest.mock import AsyncMock, call, patch, MagicMock
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller
from backend.utils.constants import EMPTY_RESULT_DICT
import backend.autofill.field_matcher_config as matcher_config


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
    result= EMPTY_RESULT_DICT
        
    await autofiller.upload_documents(mock_page, "/path/to/resume", "", result)
    
    mock_page.set_input_files.assert_called_with('input#resume', "/path/to/resume")    
    assert result["uploaded_files"]["resume"] == "/path/to/resume"
    
    
@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_successfully_uploads_cover_letter(mock_exists):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()
    result= EMPTY_RESULT_DICT

    # Act
    await autofiller.upload_documents(mock_page, "", "/path/to/cover_letter", result)

    # Assert
    mock_page.set_input_files.assert_called_with('input#cover_letter', "/path/to/cover_letter")
    assert result["uploaded_files"]["cover_letter"] == "/path/to/cover_letter"
    
@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.Path.exists", return_value=True)
async def test_upload_documents_fallback_upload_cover_letter(mock_exists):
    # Arrange
    mock_page = AsyncMock()
    autofiller = GreenhouseAutofiller()
    result= EMPTY_RESULT_DICT

    # Simulate direct upload failure on first call, success on fallback
    mock_page.set_input_files = AsyncMock(side_effect=[
        Exception("Simulated direct upload failure"),  # for input#cover_letter
        None  # for fallback input[type="file"]
    ])
    mock_page.click = AsyncMock()

    # Act
    await autofiller.upload_documents(mock_page, "", "/path/to/cover_letter", result)

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
    result = EMPTY_RESULT_DICT

    # Act
    await autofiller.upload_documents(mock_page, "/path/to/resume", "", result)

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

    result = EMPTY_RESULT_DICT

    # Act
    await autofiller.fill_voluntary_self_id(mock_page, data, result)

    # Assert: primary path was taken
    mock_try_fill.assert_called_with(mock_page, "veteran_status", "I do not wish to answer", result)
    mock_page.fill.assert_not_called()
    assert "veteran_status" not in result["errors"]

@pytest.mark.asyncio
@patch("backend.autofill.greenhouse_autofiller.try_fill_by_id", return_value=True)
async def test_fill_custom_questions_dispatches_basic_question(mock_try_fill):
    # Arrange
    autofiller = GreenhouseAutofiller()
    mock_page = AsyncMock()

    # Mock label
    mock_label = AsyncMock()
    mock_label.get_attribute.return_value = "question_123-label"
    mock_label.inner_text.return_value = "LinkedIn Profile"

    # Mock input
    mock_input = AsyncMock()
    mock_input.evaluate.return_value = "input"

    mock_page.query_selector_all.return_value = [mock_label]
    mock_page.query_selector.return_value = mock_input

    data = {
        "linkedin": "https://linkedin.com/in/test"
    }

    result = EMPTY_RESULT_DICT.copy()

    # Act
    with patch.dict(matcher_config.LABEL_KEY_MAP, {"linkedin_profile": "linkedin"}):
        await autofiller.fill_custom_questions(mock_page, data, {}, result)

    # Assert
    mock_try_fill.assert_called_with(mock_page, "question_123", "https://linkedin.com/in/test", result)
    assert "linkedin" in result["filled_fields"]
    
@pytest.mark.asyncio
async def test_handle_essay_custom_question_fills_textarea():
    # Arrange
    mock_gpt = MagicMock()
    mock_gpt.generate.return_value = "I'm excited to join because..."

    autofiller = GreenhouseAutofiller(gpt_client=mock_gpt)
    
    # mock page + input_element behavior
    mock_page = AsyncMock()
    mock_page.fill = AsyncMock()
    mock_page.keyboard.press = AsyncMock()
    
    result_log = EMPTY_RESULT_DICT
    
    label_text = "Why do you want to work here?"
    field_id = "question_123"
    
    job_data = {
        "job_descriptionn": "Test job description",
        "company": "Flock Safety"
    }

    # Act
    await autofiller.handle_essay_custom_question(mock_page, label_text, field_id, job_data, result_log)
    
    # Assert
    mock_page.fill.assert_awaited_once_with(f'xpath=//*[@id="{field_id}"]', "I'm excited to join because...")
    mock_page.keyboard.press.assert_awaited_once_with("Enter")

    assert label_text in result_log["filled_fields"]
    assert {
        "field_id": field_id,
        "essay_question": label_text,
        "response": "I'm excited to join because..."
    } in result_log["essays_filled"]
