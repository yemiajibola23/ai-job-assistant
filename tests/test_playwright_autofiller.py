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
    
def test_extract_field_label_uses_label_for_attribute_if_others_missing():
    attr_map = {"id": "full-name"}
    mock_field = mock_field_with_attributes(attr_map)
    mock_page = MagicMock()
    label_element = MagicMock()
    
    mock_page.query_selector.return_value = label_element
    label_element.inner_text.return_value = "Full Name From Label"
    
    engine = PlaywrightAutofiller(job_url="https://example.com")
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label ==  "Full Name From Label"
    
def test_extract_field_label_uses_parent_text_as_last_resort():
    mock_field = mock_field_with_attributes({})   
    mock_field.evaluate.return_value = "Parent Label Value"
    mock_page = MagicMock() 
    
    engine = PlaywrightAutofiller(job_url="https://example.com")
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label == "Parent Label Value"

    
def test_extract_field_labels_uses_fallbacks():
    aria_label = mock_field_with_attributes({"aria-label": "Aria Label Value"})
    placeholder_label = mock_field_with_attributes({"placeholder": "Placeholder Label Value"})
    id_label =  mock_field_with_attributes({"id": "full-name"})
    
    mock_page = MagicMock()
    label_element = MagicMock()
    label_element.inner_text.return_value = "Label From Tag"
    mock_page.query_selector.return_value = label_element
    
    parent_label = mock_field_with_attributes({})
    parent_label.evaluate.return_value = "Parent Label Text"
    
    engine = PlaywrightAutofiller(job_url="https://example.com")
    
    assert engine.extract_field_label(aria_label, mock_page) == "Aria Label Value"
    assert engine.extract_field_label(placeholder_label, mock_page) == "Placeholder Label Value"
    assert engine.extract_field_label(id_label, mock_page) == "Label From Tag"
    assert engine.extract_field_label(parent_label, mock_page) == "Parent Label Text"