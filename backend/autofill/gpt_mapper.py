from backend.generation.openai_client import client
import json
from openai.types.shared_params import FunctionDefinition
from json import JSONDecodeError
import re

def map_form_fields(form_fields: list[dict]):
    """
    Maps extracted form fields to standardized resume keys using GPT function calling.
    Acts as a wrapper around the underlying GPT call.
    """
    return call_gpt_function(form_fields)

def call_gpt_function(form_fields: list[dict]) -> dict:
    prompt = f"""
You are an autofill assistant.

Given the following list of form fields:

{json.dumps(form_fields, indent=2)}

Map them to a dictionary where the keys are standardized resume fields:
- full_name
- email
- phone
- linkedin
- cover_letter

Each value should be a CSS selector to autofill the field.
Only return a valid JSON object.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI response was empty or malformed")
    
    if "```" in content:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if match:
            content = match.group(1).strip()
        else:
            raise ValueError("Failed to extract JSON block from GPT response")

    try:
        return json.loads(content)
    except JSONDecodeError as e:
        print("❌ JSONDecodeError:", e)
        print("🧠 GPT raw content:\n", content)
        raise ValueError("Failed to parse GPT response as valid JSON")
 
