"""
Multi-round deliberation: jurors hear each other and may shift positions.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/deliberation.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import JuryPanel, Deliberation, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset
from mirror_jury.scenarios import AI_REGULATION

dataset = PersonaHubDataset(seed=99)
panel = JuryPanel(dataset=dataset, size=8, max_workers=4).seat()

deliberation = Deliberation(panel=panel, rounds=2)
all_rounds = deliberation.run(AI_REGULATION)

final = Deliberation.final_verdicts(all_rounds)
agg = JuryAggregator(final)
print("\n" + agg.report())
