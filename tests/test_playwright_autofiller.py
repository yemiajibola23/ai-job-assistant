from unittest.mock import Mock, AsyncMock, MagicMock, patch 
from backend.autofill.playwright_autofiller import PlaywrightAutofiller

def mock_field_with_attributes(attr_map: dict):
    def get_attr_side_effect(attr_name):
        return attr_map.get(attr_name)
    
    mock_field = MagicMock()
    mock_field.get_attribute.side_effect = get_attr_side_effect

    return mock_field
    

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
    
def test_extract_field_label_returns_aria_label_if_available():
    attr_map = {"aria-label": "Aria Label Value"}
    
    mock_field = mock_field_with_attributes(attr_map)    
    mock_page = MagicMock()
    
    engine = PlaywrightAutofiller(job_url="https://example.com")
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label == "Aria Label Value"
    
def test_extract_field_label_uses_placeholder_if_aria_missing():
   
    attr_map = {"placeholder": "Placeholder Label"}
    
    mock_field = mock_field_with_attributes(attr_map) 
    mock_page = MagicMock()
    
    engine = PlaywrightAutofiller(job_url="https://example.com")
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label == "Placeholder Label"

    
def test_extract_field_labels_uses_fallbacks():
#     1. Create a mock field with all attributes returning None except "aria-label"
#    - get_attribute("aria-label") → "Name from Aria"
    mock_field = MagicMock()

    # 2. Confirm extract_field_label(field, page) returns "Name from Aria"

    # ---

    # 3. Create another mock field:
    #    - get_attribute("aria-label") → None
    #    - get_attribute("placeholder") → "Name from Placeholder"

    # 4. Confirm extract_field_label(field, page) returns "Name from Placeholder"

    # ---

    # 5. Create another field with:
    #    - aria-label and placeholder → None
    #    - get_attribute("id") → "name-field"
    #    - page.query_selector("label[for='name-field']").inner_text() → "Name from Label Tag"

    # 6. Confirm result is "Name from Label Tag"

    # ---

    # 7. Final fallback:
    #    - All others return None
    #    - field.evaluate(...) returns "Name from Parent"

    # 8. Confirm result is "Name from Parent"