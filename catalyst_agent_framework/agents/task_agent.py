from ..core.agent import BaseAgent
from ..core.agent import AgentResponse

class TaskAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()

        return AgentResponse(
            output = "",
            steps = [],
            metadata = {}
        )
