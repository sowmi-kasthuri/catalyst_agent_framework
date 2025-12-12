from dataclasses import dataclass

@dataclass
class Event:
    name: str
    payload: dict

    def as_dict(self):
        return {"name": self.name, "payload": self.payload}