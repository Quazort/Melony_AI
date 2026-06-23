import ollama
from core.config import settings
from openai import AsyncOpenAI, OpenAI


class Agent:
    def __init__(self, role):
        self.config = settings.LLM_MODEL
        self.role = role

    def ai_generate(self, text):
        response = ollama.chat(model=self.config,
                               messages=[{"role": "system", "content": self.role}, {"role": "user", "content": text}])
        return response

    def ai_generate_v2(self, text):
        client = OpenAI(
            api_key=settings.AI_KEY,
            base_url="https://api.deepseek.com",
            timeout=30)

        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": text},
            ],
            temperature= 0.7,
            response_format={'type': 'json_object'},
            stream=False,
            timeout=30
        )
        return response
