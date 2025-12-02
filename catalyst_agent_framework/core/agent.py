from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name:str):
        self.name = name
        self.history = []
    
    def run(self, input_text:str):
        pass

    def add_message(self, role:str, content:str):
        self.history.append({"role":role,"content":content})