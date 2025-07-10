from typing import Optional
from backend.utils.logging import get_logger

logger = get_logger(__name__)

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

    xpath_by_div_label = (
        f"//div[contains(text(), '{normalized_label_text}')]/following::{field_type}[1]"
    )
    
    xpath_by_any_tag = (
    f"//*[contains(text(), '{normalized_label_text}')]/following::{field_type}[1]"
    )

    
    return (
        f"{xpath_by_for} | "
        f"{xpath_by_proximity} | "
        f"{xpath_by_div_label} | "
        f"{xpath_by_any_tag}"
    )
    
def resolve_greenhouse_field_xpath(page, label_text: str, field_type: str) -> Optional[str]:
    label_xpath = f"//label[contains(text(), '{label_text}')]"
    label_element = page.query_selector(f"xpath={label_xpath}")
    if not label_element:
        return None

    label_id = label_element.get_attribute("id")
    print(f"[debug] Label ID for '{label_text}': {label_id}")
    if not label_id or not label_id.startswith("question_") or not label_id.endswith("-label"):
        return None

    container_id = label_id.replace("-label", "")

    # Handle both native <select> and React-style <input class="select__input">
    if field_type == "select":
        return (
            f"//*[@id='{container_id}']//select | "
            f"//*[@id='{container_id}']//input[contains(@class, 'select__input')]"
        )
    else:
        return f"//*[@id='{container_id}']//{field_type}"


async def try_fill_by_id(page, field_id: str, value: str, result_log) -> bool:
    """
    Attempts to fill an input field by ID.
    Returns True if successful, False otherwise.
    """
    xpath = f'//*[@id="{field_id}"]'
    try:
        await page.fill(f'xpath={xpath}', value)
        logger.info(f"✅ Filled {field_id} with value: {value}")
        result_log["filled_fields"].append(field_id)
        return True
    except Exception as e:
        logger.exception(f"❌ Failed to fill {field_id} via ID")
        result_log["errors"].append({field_id: str(e)})
        return False

