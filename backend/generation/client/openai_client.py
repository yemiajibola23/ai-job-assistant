import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise EnvironmentError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)
class OpenAIClient:
    def __init__(self, model="gpt-4"):
        self.model = model
        
    def generate(self, prompt: str) -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI response was empty or malformed")
        return content.strip()