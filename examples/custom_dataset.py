"""
Use your own persona file instead of Persona-Hub.

Your CSV or JSONL must have a "description" or "persona" column/field.

Example CSV row:
  id,description
  p1,"A 45-year-old farmer from rural Iowa who values tradition and community."

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/custom_dataset.py --file path/to/personas.csv
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mirror_jury import MirrorJury, ResponseSummary
from mirror_jury.datasets import CustomFileDataset

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="Path to .csv or .jsonl persona file")
parser.add_argument("--question", default="Should we expand to a new market this year?")
parser.add_argument("--size", type=int, default=5)
args = parser.parse_args()

jury = MirrorJury(
    question=args.question,
    cohort_size=args.size,
    dataset=CustomFileDataset(args.file),
).assemble()

print(f"\nQuestion: {args.question}\n")
responses = jury.speak_to_all(args.question)
ResponseSummary(responses).print_all()
