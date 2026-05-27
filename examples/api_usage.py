"""
Programmatic API example.

Demonstrates:
  1. Assemble a jury for a question
  2. Speak to one person (persistent conversation)
  3. Broadcast to the whole panel

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/api_usage.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import MirrorJury, ResponseSummary

# 1. Set the question and assemble the panel
jury = MirrorJury(
    question="Should we raise our product's price by 30%?",
    cohort_size=6,
    seed=42,
).assemble()

print("Panel assembled:")
for p in jury.list_personas():
    print(f"  [{p['index']}] {p['brief']}")

# 2. Have a multi-turn conversation with person 1
print("\n--- 1-on-1 with person 1 ---")
r = jury.speak_to(1, "What's your gut reaction to a 30% price increase?")
print(f"[1]: {r.message}\n")

r = jury.speak_to(1, "Would you personally switch to a competitor?")
print(f"[1]: {r.message}\n")

# 3. Ask the whole panel a single question
print("--- Asking everyone ---")
responses = jury.speak_to_all("What's the one thing we'd need to do to justify this price increase?")
summary = ResponseSummary(responses, question="What would justify the price increase?")
summary.print_all()
