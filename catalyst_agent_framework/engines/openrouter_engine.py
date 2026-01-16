import os
import requests
from catalyst_agent_framework.core.llm_engine import LLMEngine


class OpenRouterEngine(LLMEngine):
    def __init__(self, model: str = "openai/gpt-4o-mini"):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.api_key = api_key
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, **kwargs):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            r = requests.post(self.url, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"OpenRouter generation failed: {e}")

    def call_tools(self, prompt: str, tools: list, **kwargs):
        raise NotImplementedError
