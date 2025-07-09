from backend.autofill.xpath_utils import get_labeled_field_xpath

def test_get_labeled_field_xpath_for_email_input():
    xpath = get_labeled_field_xpath("Email", "input")

    assert "label" in xpath
    assert "Email" in xpath
    assert "input" in xpath
    assert "@for" in xpath
    assert "following" in xpath
