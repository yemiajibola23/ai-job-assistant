def fill_form_field(page, selector, value):
    page.locator(selector).fill(value)