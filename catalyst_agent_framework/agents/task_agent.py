from ..core.agent import BaseAgent
from ..core.response import AgentResponse
from ..core.response import Message

class TaskAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()
        self.user(input_text)

        return AgentResponse(
            output="",
            steps=[m.as_dict() for m in self.history],
            metadata={}
        )
