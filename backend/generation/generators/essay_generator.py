from backend.generation.client.openai_client import OpenAIClient
from backend.generation.generators.base_generator import BaseGenerator
from backend.generation.prompts.essay_prompt import get_essay_prompt

class EssayResponseGenerator(BaseGenerator):
    def __init__(self, gpt_client = OpenAIClient()):
        self.gpt_client = gpt_client

    def generate(self, data: dict) -> str:
        prompt = get_essay_prompt(data)
        return self.gpt_client.generate(prompt)
