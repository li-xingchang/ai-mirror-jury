from dataclasses import dataclass


@dataclass
class Response:
    persona_id: str
    persona_brief: str
    message: str
    turn: int = 1
