from ..core.agent import BaseAgent
from ..core.response import AgentResponse
from ..engines.openrouter_engine import OpenRouterEngine


class TravelAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()
        self.user(input_text)

        engine = OpenRouterEngine()

        prompt = f"""
You are a Travel Planning Agent.

User input:
{input_text}

Create a practical travel plan with the following sections:
1. Destination or nearby cluster
2. Suggested duration
3. High-level itinerary (Day 1–Day N)
4. Estimated cost with assumptions
5. 2–3 alternative options
6. Medical or special-needs notes (if applicable)

Do not include bookings or real-time prices.
"""

        output = engine.generate(prompt)
        self.assistant(output)

        return AgentResponse(
            output=output,
            steps=[m.as_dict() for m in self.history],
            metadata={"engine": "openrouter", "agent": "travel"}
        )
