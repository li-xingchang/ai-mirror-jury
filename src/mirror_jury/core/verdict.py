from dataclasses import dataclass


@dataclass
class Verdict:
    juror_id: str
    position: str
    reasoning: str
    confidence: float  # 0.0 – 1.0
    round: int = 1

    def summary(self) -> str:
        pct = int(self.confidence * 100)
        return f"[{self.juror_id}] {self.position} ({pct}% confident)\n  {self.reasoning}"
