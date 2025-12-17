from ..core.agent import BaseAgent

class TaskAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()
        pass