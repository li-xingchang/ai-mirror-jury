"""
Quick demo: seat 6 jurors from Persona-Hub and get their verdict on one question.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python examples/basic_verdict.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import Case, JuryPanel, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset

case = Case(
    question="Should social media platforms be legally required to verify the real identity of every user?",
    context=(
        "Several countries are considering laws that would force platforms like X, "
        "Instagram, and TikTok to link every account to a government-issued ID. "
        "Supporters say it would reduce harassment and misinformation. "
        "Critics argue it destroys anonymity and chills free speech."
    ),
    options=["Yes, require identity verification", "No, keep anonymity as an option"],
)

dataset = PersonaHubDataset(seed=7)
panel = JuryPanel(dataset=dataset, size=6, max_workers=3).seat()
verdicts = panel.poll(case, round=1)

agg = JuryAggregator(verdicts)
print(agg.detailed_report())
