import os
from openai import OpenAI
import pprint
from dotenv import load_dotenv

load_dotenv()

def get_open_ai_response(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
   
    if not api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY environment variable")
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    pprint.pprint(response.model_dump())

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI response was empty or malformed")

    return content.strip()