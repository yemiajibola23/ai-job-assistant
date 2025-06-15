def fill_form_field(page, selector, value):
    page.locator(selector).fill(value)

def autofill_form(page, field_map: dict) -> None:
    for selector, value in field_map.items():
        try:
            fill_form_field(page, selector, value)
        except Exception as e:
            print(f"⚠️ Warning: Failed to fill {selector} with value '{value}': {e}")