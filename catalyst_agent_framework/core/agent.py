from abc import ABC, abstractmethod
from .response import Message

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.history: list[Message] = []
    
    @abstractmethod
    def run(self, input_text: str):
        pass

    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))
    
    def user(self, content: str):
        self.add_message("user", content)
    
    def assistant(self, content: str):
        self.add_message("assistant", content)
    
    def system(self,content: str):
        self.add_message("system", content)