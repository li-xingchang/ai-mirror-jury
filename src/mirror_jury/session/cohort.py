from __future__ import annotations
"""
Cohort — the group of personas assembled for a session.

Supports speaking to one person (persistent conversation) or broadcasting
to everyone at once (independent parallel responses).
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from mirror_jury.core.response import Response
from mirror_jury.session.juror import ConversationalJuror


class Cohort:
    def __init__(self, jurors: list[ConversationalJuror], question: str):
        self.question = question
        self._jurors = jurors
        self._by_id = {j.id: j for j in jurors}

    def __len__(self) -> int:
        return len(self._jurors)

    def list_personas(self) -> list[dict]:
        return [
            {"index": i + 1, "id": j.id, "brief": j.brief}
            for i, j in enumerate(self._jurors)
        ]

    def get(self, identifier: int | str) -> ConversationalJuror:
        """Retrieve a juror by 1-based index or persona ID."""
        if isinstance(identifier, int):
            if not 1 <= identifier <= len(self._jurors):
                raise ValueError(f"Index {identifier} out of range (1–{len(self._jurors)})")
            return self._jurors[identifier - 1]
        juror = self._by_id.get(identifier)
        if juror is None:
            raise ValueError(f"No persona with id '{identifier}'")
        return juror

    def speak_to(self, identifier: int | str, message: str) -> Response:
        """Send a message to one persona; conversation history is preserved across calls."""
        return self.get(identifier).chat(message)

    def speak_to_all(self, message: str, max_workers: int = 5) -> list[Response]:
        """Broadcast a message to every persona simultaneously; responses are independent."""
        responses: list[Response] = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(j.chat, message): j for j in self._jurors}
            for future in as_completed(futures):
                try:
                    responses.append(future.result())
                except Exception as exc:
                    juror = futures[future]
                    print(f"  [{juror.id}] error: {exc}")
        responses.sort(key=lambda r: r.persona_id)
        return responses
