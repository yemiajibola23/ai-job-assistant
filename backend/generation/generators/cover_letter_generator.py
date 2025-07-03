from backend.generation.generators.base_generator import BaseGenerator
from backend.generation.prompts.cover_letter_prompt import get_cover_letter_prompt
class CoverLetterGenerator(BaseGenerator):
    def __init__(self, jinja_env, gpt_client):
        self.jinja_env = jinja_env
        self.gpt_client = gpt_client
        
    def generate(self, data: dict) -> str:
        try:
            template = self.jinja_env.get_template("cover_letter.md.j2")
            markdown = template.render(**data)
            print("[DEBUG] JINJA RESULT:", markdown)

            if self._is_sufficient(markdown): 
                return markdown
            else:
                raise ValueError("Jinja output is insufficient")
        except Exception as e:
            print("[DEBUG] Jinja failed:", e)
            prompt = get_cover_letter_prompt(data)
            return self.gpt_client.generate(prompt)
        
    def _is_sufficient(self, content: str) -> bool:
        return len(content.strip().split()) > 20