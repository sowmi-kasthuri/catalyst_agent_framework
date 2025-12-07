from abc import ABC, abstractmethod

class LLMEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str):
        pass

    @abstractmethod
    def call_tools(self, prompt: str, tools: list):
        pass