from playwright.sync_api import Page
from backend.autofill.gpt_mapper import map_form_fields

def fill_form_field(page, selector, value):
    page.locator(selector).fill(value)

def autofill_form(page: Page, field_map: dict) -> None:
    for selector, value in field_map.items():
        try:
            fill_form_field(page, selector, value)
        except Exception as e:
            print(f"⚠️ Warning: Failed to fill {selector} with value '{value}': {e}")

def autofill_application(page: Page, parsed_resume: dict):
    form_fields = extract_form_metadata(page)
    field_mapping = map_form_fields(form_fields)

    print("📬 GPT field mapping:")
    for resume_field, selector in field_mapping.items():
        print(f"{resume_field} → {selector}")


    selector_map = {}

    RESUME_FIELD_MAP = {
        "full_name": "name",
        "email": "email",
        "phone": "phone"
    }

    for resume_field,selector in field_mapping.items():
        if resume_field in RESUME_FIELD_MAP:
            resume_key = RESUME_FIELD_MAP[resume_field]
            value = parsed_resume.get(resume_key)
            if value:
                selector_map[selector] = value
    
    autofill_form(page, selector_map)

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