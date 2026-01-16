from ..core.agent import BaseAgent
from ..engines.openrouter_engine import OpenRouterEngine
from ..core.response import AgentResponse


class TaskAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()
        self.user(input_text)

        engine = OpenRouterEngine()
        output = engine.generate(input_text)

        self.assistant(output)

        return AgentResponse(
            output=output,
            steps=[m.as_dict() for m in self.history],
            metadata={"engine": "openrouter"}
        )