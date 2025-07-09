import pytest
from unittest.mock import MagicMock, patch
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller

@patch("backend.autofill.greenhouse_autofiller.get_labeled_field_xpath")
def test_fill_field_by_xpath_success(mock_get_xpath):
    # Arrange
    mock_page = MagicMock()
    mock_locator = MagicMock()
    mock_locator.count.return_value = 1
    mock_locator.first.fill.return_value = None

    mock_page.locator.return_value = mock_locator
    mock_get_xpath.return_value = "//label[contains(text(), 'Phone')]/following::input[1]"

    autofiller = GreenhouseAutofiller(mock_page, {}, dry_run=True)

    # Act
    result = autofiller._fill_field_by_xpath("Phone", "555-1234")

    # Assert
    assert result is True
    mock_page.locator.assert_called_once()
    mock_locator.first.fill.assert_called_once_with("555-1234")
