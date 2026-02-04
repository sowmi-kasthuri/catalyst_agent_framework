from ..core.agent import BaseAgent
from ..core.response import AgentResponse
from ..engines.openrouter_engine import OpenRouterEngine


class ReleaseQualityAgent(BaseAgent):
    def run(self, input_text: str):
        self._emit_start_event()
        self.user(input_text)

        engine = OpenRouterEngine()

        prompt = f"""
    You are a Release Quality Intelligence Agent operating inside a CI/CD pipeline.

    Your job:
    Analyze code changes and test signals to assess release risk and support a go/no-go decision.
    You are advisory only. Do not give commands. Explicitly state uncertainty.

    CI/CD Context:
    {input_text}

    Use the exact section headings below.

    ## Release Risk Summary
    - Overall risk: Low / Medium / High
    - Short explanation

    ## Confidence Indicator
    - Confidence score (0.0 – 1.0)
    - One-line explanation of confidence level

    ## Primary Risk Factors
    - What changed that matters
    - Why those areas are sensitive

    ## Quality Gaps / Blind Spots
    - Likely untested or weakly tested areas

    ## Signals from CI/CD
    - Test failures, flakiness, skips, anomalies

    ## Recommendation
    - Go / Caution / No-Go
    - Advisory, not authoritative

    ## Suggested Follow-ups
    - Tests or reviews to prioritize

    Do not block releases.
    Do not modify code.
    Do not claim certainty.

    This assessment is advisory and intended to support human release decisions, not replace them.
    """

        output = engine.generate(prompt)
        self.assistant(output)

        return AgentResponse(
            output=output,
            steps=[m.as_dict() for m in self.history],
            metadata={"engine": "openrouter", "agent": "release_quality"}
    )
