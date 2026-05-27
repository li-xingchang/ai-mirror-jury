"""
Quick demo: seat 6 jurors and get their verdict on a pre-built real-world scenario.

Facts are sourced and baked into the Case so jurors reason from evidence,
not hallucinated statistics.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/basic_verdict.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import JuryPanel, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset
from mirror_jury.scenarios import FOUR_DAY_WORK_WEEK

dataset = PersonaHubDataset(seed=7)
panel = JuryPanel(dataset=dataset, size=6, max_workers=3).seat()
verdicts = panel.poll(FOUR_DAY_WORK_WEEK, round=1)

agg = JuryAggregator(verdicts)
print(agg.detailed_report())
