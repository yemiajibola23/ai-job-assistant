from backend.generation.generators.base_generator import BaseGenerator
from backend.generation.prompts.tailored_resume_prompt import get_resume_prompt

class ResumeGenerator(BaseGenerator):
    def __init__(self, jinja_env, gpt_client):
        self.jinja_env = jinja_env
        self.gpt_client = gpt_client
    
    def generate(self, data: dict) -> str:
        try: 
            template = self.jinja_env.get_template('resume.md.j2')
            return template.render(data)
        except Exception as e:
            prompt = get_resume_prompt(data)
            print(e)
            return self.gpt_client.generate(prompt)