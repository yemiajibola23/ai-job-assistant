from playwright.sync_api import Page

def fill_form_field(page, selector, value):
    page.locator(selector).fill(value)

def autofill_form(page, field_map: dict) -> None:
    for selector, value in field_map.items():
        try:
            fill_form_field(page, selector, value)
        except Exception as e:
            print(f"⚠️ Warning: Failed to fill {selector} with value '{value}': {e}")

def extract_form_metadata(page: Page) -> list[dict]:
    field_metadata = []
    elements = page.query_selector_all("input, textarea, select")

    for element in elements:
        tag = element.evaluate("el => el.tagName.toLowerCase()")

        if tag == "input":
            type_attr = element.get_attribute("type")
        else:
            type_attr = None
        
        name = element.get_attribute("name")
        id_attr = element.get_attribute("id")
        placeholder = element.get_attribute("placeholder")
        
        label_text = None
        if id_attr:
            label_element = page.query_selector(f"label[for='{id_attr}']")
            if label_element:
                label_text = label_element.inner_text().strip()
            else:
               label_handle = element.evaluate_handle("el => el.closest('label')")
               parent_label = label_handle.as_element() 
               if parent_label:
                   label_text = parent_label.inner_text().strip()
        
        metadata_dict = {
            "tag": tag,
            "type": type_attr,
            "name": name,
            "id": id_attr,
            "placeholder": placeholder,
            "label": label_text
        }

        field_metadata.append(metadata_dict)
    
    return field_metadata