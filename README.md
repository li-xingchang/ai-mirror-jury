# AI Mirror Jury

Simulate how a **diverse panel of real-world personas** would respond to any question, policy, or ethical dilemma — by grounding each AI juror in a publicly available user dataset.

## How it works

1. **Load personas** from a public dataset (default: [Persona-Hub](https://huggingface.co/datasets/proj-persona/PersonaHub), ~200k diverse human profiles)
2. **Seat a jury** — randomly sample N personas to form a panel
3. **Poll** — each juror responds in character via the Claude API
4. **Deliberate** *(optional)* — jurors see each other's reasoning and can update their position
5. **Aggregate** — tally positions, detect majority, report confidence

Each juror is powered by Claude with **prompt caching** on their persona, keeping costs low even for large panels.

## Quickstart

```bash
git clone https://github.com/li-xingchang/ai-mirror-jury
cd ai-mirror-jury
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...

# Single-round verdict (6 jurors)
python examples/basic_verdict.py

# Two-round deliberation (8 jurors)
python examples/deliberation.py

# Your own persona CSV/JSONL
python examples/custom_dataset.py --file my_personas.csv --question "Should AI be regulated?"
```

## Dataset

### Default: Persona-Hub

[`proj-persona/PersonaHub`](https://huggingface.co/datasets/proj-persona/PersonaHub) — 200,000+ diverse persona descriptions covering a wide range of ages, occupations, locations, values, and life experiences. Licensed CC-BY 4.0.

The dataset is downloaded automatically on first use via the HuggingFace `datasets` library and cached in `~/.cache/huggingface`.

### Bring your own

Drop in any `.csv` or `.jsonl` file with a `description` (or `persona`) field:

```python
from mirror_jury import Case, JuryPanel, JuryAggregator
from mirror_jury.datasets import CustomFileDataset

dataset = CustomFileDataset("my_personas.csv")
panel = JuryPanel(dataset=dataset, size=12).seat()
verdicts = panel.poll(Case(question="..."))
print(JuryAggregator(verdicts).detailed_report())
```

## API

```python
from mirror_jury import Case, JuryPanel, Deliberation, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset

# Define the question
case = Case(
    question="Should the voting age be lowered to 16?",
    context="Several democracies have already done this for local elections.",
    options=["Yes", "No"],
)

# Seat a 12-person jury
dataset = PersonaHubDataset(seed=42)
panel = JuryPanel(dataset=dataset, size=12, max_workers=4).seat()

# Single poll
verdicts = panel.poll(case)

# Or run multi-round deliberation
deliberation = Deliberation(panel=panel, rounds=2)
all_rounds = deliberation.run(case)
verdicts = Deliberation.final_verdicts(all_rounds)

# Aggregate
agg = JuryAggregator(verdicts)
print(agg.report())           # summary tally
print(agg.detailed_report())  # includes each juror's reasoning
```

### Key classes

| Class | Description |
|---|---|
| `Case` | Question, optional context, optional answer options |
| `Persona` | A single juror profile loaded from the dataset |
| `Juror` | Claude-backed juror; calls the API and returns a `Verdict` |
| `JuryPanel` | Samples personas, seats jurors, polls in parallel |
| `Deliberation` | Runs multiple rounds; jurors see each other's reasoning |
| `JuryAggregator` | Tallies positions, detects majority, formats reports |
| `PersonaHubDataset` | Loads from Persona-Hub (HuggingFace) |
| `CustomFileDataset` | Loads from a local CSV or JSONL file |

## Running tests

```bash
pip install pytest
pytest
```

Tests cover all core logic without making API calls.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |

## License

MIT
