from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

    def as_dict(self):
        return {"role":self.role, "content":self.content}
    
@dataclass
class AgentResponse:
    output: str
    steps: list
    metadata: dict