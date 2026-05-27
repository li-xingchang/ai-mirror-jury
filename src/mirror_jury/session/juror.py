from __future__ import annotations
"""
A conversational juror — a persona backed by Claude with persistent conversation history.
"""

import anthropic

from mirror_jury.core.persona import Persona
from mirror_jury.core.response import Response

_CLIENT: anthropic.Anthropic | None = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


class ConversationalJuror:
    MODEL = "claude-sonnet-4-6"

    def __init__(self, persona: Persona, context_facts: list[str]):
        self.persona = persona
        self._context_facts = context_facts
        self._history: list[dict] = []
        self._turn = 0

    @property
    def id(self) -> str:
        return self.persona.id

    @property
    def brief(self) -> str:
        """First sentence of the persona description, capped at 120 chars."""
        desc = self.persona.description
        dot = desc.find(". ")
        if 0 < dot < 120:
            return desc[: dot + 1]
        return desc[:120].rstrip() + ("..." if len(desc) > 120 else "")

    def _build_system(self) -> list[dict]:
        text = self.persona.to_system_prompt()
        if self._context_facts:
            facts = "\n".join(f"  • {f}" for f in self._context_facts)
            text += (
                "\n\nFACTUAL CONTEXT — you may reference these facts; "
                "do not invent statistics or cite sources beyond what is listed here:\n"
                + facts
            )
        return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]

    def chat(self, message: str) -> Response:
        self._turn += 1
        self._history.append({"role": "user", "content": message})

        resp = _client().messages.create(
            model=self.MODEL,
            max_tokens=600,
            system=self._build_system(),
            messages=self._history,
        )

        reply = resp.content[0].text.strip()
        self._history.append({"role": "assistant", "content": reply})
        return Response(
            persona_id=self.id,
            persona_brief=self.brief,
            message=reply,
            turn=self._turn,
        )

    def reset(self) -> None:
        self._history = []
        self._turn = 0
