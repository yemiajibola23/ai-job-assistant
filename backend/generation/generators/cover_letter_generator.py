from backend.generation.generators.base_generator import BaseGenerator
from backend.generation.prompts.cover_letter_prompt import get_cover_letter_prompt
from backend.utils.logging import get_logger

logger = get_logger(__name__)
class CoverLetterGenerator(BaseGenerator):
    def __init__(self, jinja_env, gpt_client):
        self.jinja_env = jinja_env
        self.gpt_client = gpt_client
        
    def generate(self, data: dict) -> str:
        try:
            template = self.jinja_env.get_template("cover_letter.md.j2")
            markdown = template.render(**data)
            logger.debug(f"[DEBUG] JINJA RESULT: {markdown}")


            if self._is_sufficient(markdown): 
                logger.debug("[cover_letter] 📝 Jinja rendered successfully")
                return markdown
            else:
                logger.warning("[cover_letter] ⚠️ Jinja output insufficient — using GPT fallback")
                raise ValueError("Jinja output is insufficient")
        except Exception as e:
            logger.error(f"[cover_letter] ❌ Jinja rendering failed: {e}")
            prompt = get_cover_letter_prompt(data)
            logger.info("[cover_letter] 💡 Using GPT fallback instead")
            logger.debug(f"[cover_letter] 🧠 Prompt to GPT: {prompt[:100]}...")
            return self.gpt_client.generate(prompt)
        
    def _is_sufficient(self, content: str) -> bool:
        return len(content.strip().split()) > 20