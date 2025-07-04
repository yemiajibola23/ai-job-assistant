import pytest
from unittest.mock import MagicMock, patch 
from backend.autofill.playwright_autofiller import PlaywrightAutofiller
import tempfile
import os
from playwright.sync_api import sync_playwright

MINIMAL_RESUME_DATA = {
    "name": "Test User",
    "summary": "iOS dev",
    "experience": [],
    "skills": []
}

def make_test_autofiller(**kwargs):
    return PlaywrightAutofiller(
        job_url=kwargs.get("job_url", "https://example.com/"),
        job_id=kwargs.get("job_id", "test-job"),
        job_description=kwargs.get("job_description", "fake job desc"),
        resume_data=kwargs.get("resume_data", MINIMAL_RESUME_DATA)
    )

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
    mock_page.query_selector.return_value = None
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context

    mock_pw = MagicMock()
    mock_pw.chromium.launch.return_value = mock_browser
    mock_sync_playwright.return_value.__enter__.return_value = mock_pw

    application_data ={
        "name": "Test User",
        "email": "test@example.com"
    }

    engine = make_test_autofiller()
    
    engine.extract_field_label = MagicMock(return_value="Full Name")
    engine.fill_form(application_data)

    mock_page.goto.assert_called_once_with("https://example.com/")
    mock_page.query_selector_all.assert_called_once()
    mock_field.fill.assert_called()
    
def test_extract_field_label_returns_aria_label_if_available():
    attr_map = {"aria-label": "Aria Label Value"}
    
    mock_field = mock_field_with_attributes(attr_map)    
    mock_page = MagicMock()
    
    engine = make_test_autofiller()
    
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label == "Aria Label Value"
    
def test_extract_field_label_uses_placeholder_if_aria_missing():
   
    attr_map = {"placeholder": "Placeholder Label"}
    
    mock_field = mock_field_with_attributes(attr_map) 
    mock_page = MagicMock()
    
    engine = make_test_autofiller()
    
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label == "Placeholder Label"
    
def test_extract_field_label_uses_label_for_attribute_if_others_missing():
    attr_map = {"id": "full-name"}
    mock_field = mock_field_with_attributes(attr_map)
    mock_page = MagicMock()
    label_element = MagicMock()
    
    mock_page.query_selector.return_value = label_element
    label_element.inner_text.return_value = "Full Name From Label"
    
    engine = make_test_autofiller()
    
    label = engine.extract_field_label(mock_field, mock_page)
    
    assert label ==  "Full Name From Label"
    
def test_extract_field_label_uses_parent_text_as_last_resort():
    mock_field = mock_field_with_attributes({})   
    mock_field.evaluate.return_value = "Parent Label Value"
    mock_page = MagicMock() 
    
    engine = make_test_autofiller()
    
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
    
    engine = make_test_autofiller()
    
    assert engine.extract_field_label(aria_label, mock_page) == "Aria Label Value"
    assert engine.extract_field_label(placeholder_label, mock_page) == "Placeholder Label Value"
    assert engine.extract_field_label(id_label, mock_page) == "Label From Tag"
    assert engine.extract_field_label(parent_label, mock_page) == "Parent Label Text"

@patch("backend.autofill.playwright_autofiller.match_label_to_key")    
def test_fill_form_fills_correct_field_based_on_label(mock_match_label_to_key):
    mock_field = MagicMock()
    mock_page = MagicMock()
    mock_page.query_selector.side_effect = [MagicMock(), None]
    mock_page.query_selector_all.side_effect = [[mock_field], []]
    
    engine = make_test_autofiller()
    engine.extract_field_label = MagicMock(return_value="Full Name")
    
    mock_match_label_to_key.return_value = "name"
    
    application_data = {"name": "Test User"}
    
    engine.fill_form(application_data, mock_page)
    
    mock_field.fill.assert_called_once_with("Test User")
    
@patch("backend.autofill.playwright_autofiller.match_label_to_key")    
def test_fill_form_selects_radio_button(mock_match_label_to_key):
    mock_radio = MagicMock()
    mock_radio.get_attribute.side_effect = lambda attr: "radio" if attr == "type" else None
    mock_radio.evaluate.return_value = "Yes"
    
    mock_page = MagicMock()
    mock_page.query_selector.side_effect = [MagicMock(), None]
    mock_page.query_selector_all.side_effect = [[mock_radio], []]
    
    engine = make_test_autofiller()    
    
    engine.extract_field_label = MagicMock(return_value="Yes")
    mock_match_label_to_key.return_value = "work_authorization"
    application_data = { "work_authorization": "Yes" }
    
    engine.fill_form(application_data, mock_page)
    
    mock_radio.check.assert_called_once()
    
@patch("backend.autofill.playwright_autofiller.match_label_to_key")       
def test_fill_form_selects_dropdown(mocK_match_label_to_key):
    mock_select = MagicMock()
    mock_select.evaluate.side_effect = lambda script:("select" if "tagName" in script else "Work Eligibility")
    mock_select.get_attribute.side_effect = lambda attr: None
    mock_select.select_option = MagicMock()
    
    mock_page = MagicMock()
    mock_page.query_selector.side_effect = [MagicMock(), None]
    mock_page.query_selector_all.side_effect = [[mock_select], []]
    
    engine = make_test_autofiller()
    
    engine.extract_field_label = MagicMock(return_value="Work Eligibility")
    mocK_match_label_to_key.return_value = "work_eligibility"
    application_data = {"work_eligibility": "US Citizen"}
    
    engine.fill_form(application_data, mock_page)
    
    mock_select.select_option.assert_called_once_with("US Citizen")
    
    
def test_click_next_if_available_clicks_button_and_returns_true():
    mock_page = MagicMock()
    mock_button = MagicMock()
    mock_page.query_selector.return_value = mock_button

    engine = make_test_autofiller()

    result = engine._click_next_if_available(mock_page)

    mock_button.click.assert_called_once()
    mock_page.wait_for_timeout.assert_called_once()
    assert result is True
    
def test_click_next_if_available_returns_false_when_no_button():
    mock_page = MagicMock()
    mock_page.query_selector.return_value = None

    engine = make_test_autofiller()

    result = engine._click_next_if_available(mock_page)

    assert result is False

@patch("backend.autofill.playwright_autofiller.generate_and_render_tailored_resume")
def test_fill_form_uploads_resume(mock_generate_resume):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        mock_page = context.new_page()
        
        mock_page.set_content("""
            <html>
                <body>
                    <form>
                        <label for="resume">Upload Resume</label>
                        <input type="file" id="resume" name="resume">
                    </form>
                </body>
            </html>
        """)
    
        with patch("backend.autofill.playwright_autofiller.match_label_to_key") as mock_match:
            mock_match.return_value = "resume"
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(b"%PDF-1.4 mock resume")
                resume_path = tmp.name
        
            engine =make_test_autofiller()
            mock_generate_resume.return_value = resume_path
            
            engine.fill_form({"resume": resume_path}, mock_page)
        
            input_handle = mock_page.query_selector("input[type='file']")
            assert input_handle is not None, "File input not found"
        
            file_name = input_handle.evaluate("(el) => el.files[0].name")
            assert file_name.endswith(".pdf")
        
            os.remove(resume_path)