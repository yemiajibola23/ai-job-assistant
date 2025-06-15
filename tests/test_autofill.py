from unittest.mock import Mock
from backend.autofill.autofill import fill_form_field

def test_fill_form_field_calls_correct_locator_and_fill():
    # Use unittest.mock.Mock to simulate page
    mock_page = Mock()
    mock_locator = Mock()
    mock_page.locator.return_value = mock_locator

    fill_form_field(mock_page, "#email", "test@example.com")

    # Assert that .locator(selector).fill(value) is called correctly
    mock_page.locator.assert_called_once_with("#email")
    mock_locator.fill.assert_called_once_with("test@example.com")