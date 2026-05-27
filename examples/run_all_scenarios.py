"""
Run every built-in scenario and print a summary tally for each.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/run_all_scenarios.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import JuryPanel, JuryAggregator, ALL_SCENARIOS
from mirror_jury.datasets import PersonaHubDataset

dataset = PersonaHubDataset(seed=42)
panel = JuryPanel(dataset=dataset, size=6, max_workers=4).seat()

for name, case in ALL_SCENARIOS.items():
    print(f"\n{'='*60}")
    print(f"SCENARIO: {name.replace('_', ' ').upper()}")
    verdicts = panel.poll(case)
    print(JuryAggregator(verdicts).report())
