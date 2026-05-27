"""Multi-round deliberation loop."""

from mirror_jury.core.case import Case
from mirror_jury.core.verdict import Verdict
from mirror_jury.jury.panel import JuryPanel


class Deliberation:
    """
    Run multiple polling rounds so jurors can react to each other's reasoning.
    Stops early if the panel reaches consensus (all jurors share the same position).
    """

    def __init__(self, panel: JuryPanel, rounds: int = 2):
        self._panel = panel
        self._rounds = rounds

    def run(self, case: Case) -> list[list[Verdict]]:
        all_rounds: list[list[Verdict]] = []
        prior: list[Verdict] | None = None

        for r in range(1, self._rounds + 1):
            print(f"\n--- Round {r} ---")
            verdicts = self._panel.poll(case, prior_verdicts=prior, round=r)
            all_rounds.append(verdicts)
            prior = verdicts

            positions = {v.position.lower() for v in verdicts}
            if len(positions) == 1:
                print(f"Consensus reached in round {r}: '{positions.pop()}'")
                break

        return all_rounds

    @staticmethod
    def final_verdicts(all_rounds: list[list[Verdict]]) -> list[Verdict]:
        """Return the last round's verdicts."""
        return all_rounds[-1] if all_rounds else []
