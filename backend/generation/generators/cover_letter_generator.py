from backend.generation.generators.base_generator import BaseGenerator

class CoverLetterGenerator(BaseGenerator):
    def __init__(self, jinja_env, gpt_client):
        self.jinja_env = jinja_env
        self.gpt_client = gpt_client
        
    def generate(self, data: dict) -> str:
        raise NotImplementedError