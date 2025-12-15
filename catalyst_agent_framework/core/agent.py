from abc import ABC, abstractmethod
from .response import Message

from ..utils.logger import Logger
from ..utils.metrics import Metrics
from .events import Event

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.history: list[Message] = []
        self.logger = Logger()
        self.metrics = Metrics()
    
    def _emit_start_event(self):
        event = Event(name="agent.start", payload={"agent": self.name})
        self.logger.log("INFO", "agent.start", event=event.as_dict())
        self.metrics.increment("agent_start")
    
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