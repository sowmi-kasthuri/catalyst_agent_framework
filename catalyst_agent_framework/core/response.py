from dataclasses import dataclass

@dataclass
class message:
    role: str
    content: str

    def as_dict(self):
        return {"role":self.role, "content":self.content}