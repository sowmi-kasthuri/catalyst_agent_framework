from ..core.agent import BaseAgent
from ..core.response import AgentResponse
from ..engines.openrouter_engine import OpenRouterEngine


class ResearchAgent(BaseAgent):
    def run(self, input_text: str):
        # Emit lifecycle start event
        self._emit_start_event()

        # Record user input
        self.user(input_text)

        # LLM engine
        engine = OpenRouterEngine()

        # First-pass research prompt
        prompt = f"""
You are an AI Research Agent.

Task:
Synthesize the topic below into structured insights. Be neutral, analytical, and concise.
Avoid certainty. Explicitly state limitations and unknowns.

Topic:
{input_text}

Use the exact section headings below.

## Executive Summary
- 5–7 bullet points summarizing the topic

## Key Concepts & Definitions
- Short explanations of core ideas

## Major Trade-offs / Perspectives
- Competing approaches with pros and cons

## Practical Implications
- What this means for real-world decisions (engineering, ops, orgs)

## Risks, Limitations & Unknowns
- Where conclusions may break down

## Further Questions
- 3–5 questions worth exploring next

Do not include citations, links, or browsing claims.
"""

        # Generate response
        output = engine.generate(prompt)

        # Record assistant output
        self.assistant(output)

        # Return structured agent response
        return AgentResponse(
            output=output,
            steps=[m.as_dict() for m in self.history],
            metadata={"engine": "openrouter", "agent": "research"}
        )
