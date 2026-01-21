from ..core.agent import BaseAgent
from ..core.response import AgentResponse
from ..engines.openrouter_engine import OpenRouterEngine


class TravelAgent(BaseAgent):
    def run(self, input_text: str):
        required_keywords = ["origin", "budget", "day", "trip"]
        if not any(k in input_text.lower() for k in required_keywords):
            return AgentResponse(
            output="Please provide origin, travel window (days), budget range, and type of trip.",
            steps=[],
            metadata={"agent": "travel"}
        )
        self._emit_start_event()
        self.user(input_text)

        engine = OpenRouterEngine()

        prompt = f"""
You are a Travel Planning Agent.

User input:
{input_text}

Create a practical travel plan with CLEAR, LABELED sections using the exact headings below.
Keep each section concise.

## Destination / Cluster
- One primary destination or a small cluster on the same theme

## Suggested Duration
- Days / nights with brief rationale

## High-Level Itinerary
- Day 1 to Day N (bullet points)

## Estimated Cost (Assumptions)
- Travel
- Stay
- Local transport
- Buffer

## Alternatives
- Option A (cheaper)
- Option B (more comfortable)
- Option C (closer / farther)

## Medical / Special Needs Notes
- Include only if applicable

Do NOT include bookings or real-time prices.  

Print the disclaimer - All costs are rough estimates for planning purposes and may vary 
"""

        output = engine.generate(prompt)
        self.assistant(output)

        return AgentResponse(
            output=output,
            steps=[m.as_dict() for m in self.history],
            metadata={"engine": "openrouter", "agent": "travel"}
        )
