from backend.generation.openai_client import client
import json
from openai.types.shared_params import FunctionDefinition
def map_form_fields(form_fields: list[dict]):
    pass

def call_gpt_function(form_fields: list[dict]) -> dict:
    # define function_schema
    function_schema: FunctionDefinition = {
    "name": "map_form_fields",
    "description": "Map HTML form fields to known resume data keys.",
    "parameters": {
        "type": "object",
        "properties": {
            "fields": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tag": {"type": "string"},
                        "type": {"type": "string"},
                        "name": {"type": "string"},
                        "id": {"type": "string"},
                        "placeholder": {"type": "string"},
                        "label": {"type": "string"}
                    },
                    "required": ["tag"]
                }
            }
        },
        "required": ["fields"]
    }
}
    # call OpenAI client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart autofill assistant that maps form fields to resume attributes like full_name, email, phone, linkedin, cover_letter, etc. Use the provided form field metadata to make your mapping."},
            {"role": "user", "content": json.dumps({"fields": form_fields})}            
        ],
        functions=[function_schema],
        function_call={"name": "map_form_fields"}
    )
    # parse and return result
    function_call = response.choices[0].message.function_call
    if function_call is None:
        raise ValueError("GPT did not return a function call.")
    
    arguments = function_call.arguments
    parsed_result = json.loads(arguments)

    return parsed_result
