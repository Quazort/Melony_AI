import ollama
from core.config import settings
from openai import AsyncOpenAI



class Agent:
    def __init__(self, role):
        self.config = settings.LLM_MODEL
        self.role = role

    def ai_generate(self, text):
        response = ollama.chat(model=self.config,
                               messages=[{"role": "system", "content": self.role}, {"role": "user", "content": text}])
        return response

    async def ai_generate_v2(self,text):
        client = AsyncOpenAI(
            api_key=settings.API_KEY,
            base_url="https://api.deepseek.com",
            timeout=20)

        response = await client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": text},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
            timeout=15
        )
        print(response.choices[0].message.content)
        return response