def get_labeled_field_xpath(label_text: str, field_type:str) -> str:
    """
    Returns an XPath selector string to locate a form field (input, textarea, select)
    based on a nearby label's text.

    The function tries two main strategies:
    1. Match by label with 'for' attribute that links to a field with matching ID.
    2. Match by label text proximity (sibling or descendant relationship).

    Args:
        label_text (str): The visible text of the label, e.g. "Phone Number".
        field_type (str): The type of field to target, e.g. "input", "textarea", or "select".

    Returns:
        str: An XPath string you can pass to Playwright's `page.locator(f"xpath={...}")`
    """
    
    normalized_label_text = label_text.strip()
    
    xpath_by_for = (
        f"//label[normalize-space(.)='{normalized_label_text}']/@for | "
        f"//label[contains(normalize-space(.), '{normalized_label_text}')]/@for"
    )
    
    xpath_by_proximity = (
        f"//label[contains(normalize-space(.), '{normalized_label_text}')]"
        f"/following-sibling::*//{field_type} | "
        f"//label[contains(normalize-space(.), '{normalized_label_text}')]"
        f"/following::{field_type}[1]"
    )

    
    return f"{xpath_by_for} | {xpath_by_proximity}"