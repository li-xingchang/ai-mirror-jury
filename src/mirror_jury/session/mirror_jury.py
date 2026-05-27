from __future__ import annotations
"""
MirrorJury — the main entry point for a session.

Usage:
    jury = MirrorJury("Should we raise prices by 30%?").assemble()
    jury.speak_to(1, "What's your gut reaction?")
    jury.speak_to_all("What's the biggest risk?")
"""

from mirror_jury.context.guardrails import get_guardrail_facts
from mirror_jury.core.response import Response
from mirror_jury.datasets.base import BaseDataset
from mirror_jury.datasets.persona_hub import PersonaHubDataset
from mirror_jury.session.cohort import Cohort
from mirror_jury.session.juror import ConversationalJuror


class MirrorJury:
    def __init__(
        self,
        question: str,
        cohort_size: int = 7,
        dataset: BaseDataset | None = None,
        seed: int = 42,
    ):
        if not 5 <= cohort_size <= 10:
            raise ValueError("cohort_size must be between 5 and 10")
        self.question = question
        self._cohort_size = cohort_size
        self._dataset = dataset or PersonaHubDataset(seed=seed)
        self._cohort: Cohort | None = None

    def assemble(self) -> "MirrorJury":
        """Load personas and wire up the cohort. Call this before speaking."""
        facts = get_guardrail_facts(self.question)
        personas = self._dataset.load(self._cohort_size)
        jurors = [ConversationalJuror(p, facts) for p in personas]
        self._cohort = Cohort(jurors, self.question)
        return self

    @property
    def cohort(self) -> Cohort:
        if self._cohort is None:
            raise RuntimeError("Call .assemble() first.")
        return self._cohort

    def list_personas(self) -> list[dict]:
        return self.cohort.list_personas()

    def speak_to(self, identifier: int | str, message: str) -> Response:
        """Chat with one persona. Conversation history persists across calls."""
        return self.cohort.speak_to(identifier, message)

    def speak_to_all(self, message: str) -> list[Response]:
        """Ask every persona the same message simultaneously."""
        return self.cohort.speak_to_all(message)
