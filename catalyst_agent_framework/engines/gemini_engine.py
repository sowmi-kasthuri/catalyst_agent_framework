import os
from google import genai
from catalyst_agent_framework.core.llm_engine import LLMEngine


class GeminiEngine(LLMEngine):
    def __init__(self, model: str = "models/gemini-2.0-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")
        
    def call_tools(self, prompt: str, tools: list, **kwargs):
        raise NotImplementedError
