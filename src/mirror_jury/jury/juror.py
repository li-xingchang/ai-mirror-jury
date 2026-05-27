"""Single AI juror backed by the Claude API."""

import json
import re

import anthropic

from mirror_jury.core.case import Case
from mirror_jury.core.persona import Persona
from mirror_jury.core.verdict import Verdict

_CLIENT = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


_GROUNDING_INSTRUCTION = """\
IMPORTANT RULES FOR YOUR RESPONSE:
- Draw ONLY on the verified facts provided above and your own personal values, \
emotions, and lived experience as described in your character.
- Do NOT invent statistics, cite studies, or reference events not listed in the facts.
- If you are uncertain, express that uncertainty rather than fabricating details.
- Speak in first person as yourself — not as a policy analyst or neutral observer."""

_VERDICT_SCHEMA = """\
Respond with valid JSON only — no markdown fences, no extra text:
{
  "position": "<your clear stance or answer in plain language>",
  "reasoning": "<2-3 sentences from your personal perspective, citing only facts provided>",
  "confidence": <number between 0.0 and 1.0>
}"""


class Juror:
    MODEL = "claude-sonnet-4-6"

    def __init__(self, persona: Persona):
        self.persona = persona

    def deliberate(self, case: Case, prior_verdicts: list[Verdict] | None = None, round: int = 1) -> Verdict:
        messages = self._build_messages(case, prior_verdicts)

        response = _client().messages.create(
            model=self.MODEL,
            max_tokens=512,
            system=[
                {
                    "type": "text",
                    "text": self.persona.to_system_prompt(),
                    # Cache the persona — unchanged across deliberation rounds
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        )

        raw = response.content[0].text.strip()
        return self._parse_verdict(raw, round)

    def _build_messages(self, case: Case, prior_verdicts: list[Verdict] | None) -> list[dict]:
        user_text = case.render()
        user_text += f"\n\n{_GROUNDING_INSTRUCTION}"

        if prior_verdicts:
            others = "\n".join(
                f"- Juror {v.juror_id}: {v.position} — {v.reasoning}"
                for v in prior_verdicts
                if v.juror_id != self.persona.id
            )
            user_text += (
                f"\n\nYour fellow jurors have shared their views:\n{others}\n\n"
                "You may update your position or hold firm — but stay grounded in "
                "the verified facts and your own values. Explain your reasoning."
            )

        user_text += f"\n\n{_VERDICT_SCHEMA}"
        return [{"role": "user", "content": user_text}]

    def _parse_verdict(self, raw: str, round: int) -> Verdict:
        try:
            # Strip markdown fences if the model adds them despite instructions
            cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
            data = json.loads(cleaned)
            return Verdict(
                juror_id=self.persona.id,
                position=str(data.get("position", "unclear")),
                reasoning=str(data.get("reasoning", "")),
                confidence=float(data.get("confidence", 0.5)),
                round=round,
            )
        except (json.JSONDecodeError, ValueError):
            return Verdict(
                juror_id=self.persona.id,
                position="unclear",
                reasoning=raw[:300],
                confidence=0.5,
                round=round,
            )
