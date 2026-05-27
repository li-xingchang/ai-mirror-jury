"""
Use your own persona data (CSV or JSONL) instead of Persona-Hub.

Your file needs at least a "description" or "persona" column/field.

Example CSV:
  id,description
  p1,"A 45-year-old farmer from rural Iowa who values tradition and community."
  p2,"A 28-year-old software engineer in San Francisco who cares about open-source."

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python examples/custom_dataset.py --file path/to/personas.csv
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import Case, JuryPanel, JuryAggregator
from mirror_jury.datasets import CustomFileDataset

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="Path to .csv or .jsonl persona file")
parser.add_argument("--question", default="Should AI be regulated by the government?")
parser.add_argument("--size", type=int, default=6)
args = parser.parse_args()

case = Case(question=args.question)
dataset = CustomFileDataset(path=args.file)
panel = JuryPanel(dataset=dataset, size=args.size).seat()
verdicts = panel.poll(case)

agg = JuryAggregator(verdicts)
print(agg.detailed_report())
