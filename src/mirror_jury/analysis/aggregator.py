"""Aggregate and summarise jury verdicts."""

from collections import Counter

from mirror_jury.core.verdict import Verdict


class JuryAggregator:
    def __init__(self, verdicts: list[Verdict]):
        self._verdicts = verdicts

    def tally(self) -> dict[str, int]:
        """Count occurrences of each position."""
        return dict(Counter(v.position.lower() for v in self._verdicts))

    def majority(self) -> str | None:
        """Return the position held by more than half the jury, or None."""
        tally = self.tally()
        total = len(self._verdicts)
        for position, count in tally.items():
            if count / total > 0.5:
                return position
        return None

    def average_confidence(self) -> float:
        if not self._verdicts:
            return 0.0
        return sum(v.confidence for v in self._verdicts) / len(self._verdicts)

    def report(self) -> str:
        tally = self.tally()
        majority = self.majority()
        avg_conf = self.average_confidence()
        total = len(self._verdicts)

        lines = [
            "=" * 50,
            f"JURY VERDICT  ({total} jurors)",
            "=" * 50,
        ]
        for position, count in sorted(tally.items(), key=lambda x: -x[1]):
            pct = int(count / total * 100)
            lines.append(f"  {position:<25} {count:>3} / {total}  ({pct}%)")
        lines.append(f"\nMajority position : {majority or 'hung jury'}")
        lines.append(f"Avg confidence    : {avg_conf:.2f}")
        lines.append("=" * 50)
        return "\n".join(lines)

    def detailed_report(self) -> str:
        lines = [self.report(), "\nINDIVIDUAL VERDICTS:"]
        for v in sorted(self._verdicts, key=lambda x: x.juror_id):
            lines.append(f"\n{v.summary()}")
        return "\n".join(lines)
