"""
Multi-round deliberation demo: jurors hear each other and may change their minds.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python examples/deliberation.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import Case, JuryPanel, Deliberation, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset

case = Case(
    question="Is a four-day work week a good policy for employers to adopt?",
    context=(
        "A number of companies across the US, UK, and Iceland have piloted a "
        "32-hour work week at full pay. Results have been mixed: some report "
        "productivity gains and reduced burnout, others cite coordination challenges "
        "and difficulty serving customers across time zones."
    ),
)

dataset = PersonaHubDataset(seed=99)
panel = JuryPanel(dataset=dataset, size=8, max_workers=4).seat()

deliberation = Deliberation(panel=panel, rounds=2)
all_rounds = deliberation.run(case)

final = Deliberation.final_verdicts(all_rounds)
agg = JuryAggregator(final)
print("\n" + agg.report())
