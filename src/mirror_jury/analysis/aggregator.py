from __future__ import annotations
"""Format and display a set of responses from a speak_to_all call."""

import textwrap

from mirror_jury.core.response import Response


class ResponseSummary:
    def __init__(self, responses: list[Response], question: str = ""):
        self._responses = responses
        self.question = question

    def __len__(self) -> int:
        return len(self._responses)

    def print_all(self, width: int = 72) -> None:
        if self.question:
            print(f"\nQuestion: {self.question}")
        print(f"{'─' * width}")
        for r in self._responses:
            print(f"\n{r.persona_brief}")
            print(textwrap.fill(r.message, width=width, initial_indent="  ", subsequent_indent="  "))
        print(f"\n{'─' * width}")

    def as_text(self, width: int = 72) -> str:
        lines = []
        if self.question:
            lines.append(f"Question: {self.question}")
        lines.append("─" * width)
        for r in self._responses:
            lines.append(f"\n{r.persona_brief}")
            lines.append(textwrap.fill(r.message, width=width, initial_indent="  ", subsequent_indent="  "))
        lines.append("─" * width)
        return "\n".join(lines)
