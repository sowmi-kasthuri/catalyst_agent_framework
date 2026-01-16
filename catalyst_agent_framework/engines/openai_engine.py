# Status: Implemented but inactive
# Used for future provider demos or extensions

from ..core.llm_engine import LLMEngine

class OpenAIEngine(LLMEngine):
    def __init__(self, client, model: str, **defaults):
        self.client = client
        self.model = model
        self.defaults = defaults
    
    def generate(self, prompt: str, **kwargs):
        pass

    def call_tools(self, prompt: str, tools: list, **kwargs):
        pass