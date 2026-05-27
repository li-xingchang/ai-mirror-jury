# AI Mirror Jury

**Run a focus group of 200,000 real-world personas in seconds — not weeks.**

AI Mirror Jury lets you ask any policy, product, or ethical question and instantly see how a diverse, demographically representative panel would respond — complete with individual reasoning, confidence scores, and multi-round deliberation.

---

## The problem with AI opinion polling

When you ask a single AI model "what do people think about X?", you get one averaged, sanitized answer. That's not useful. Real decisions — in policy, product design, journalism, research — require understanding the *distribution* of human opinion: who agrees, who resists, and why.

Traditional solutions are slow and expensive. A quality focus group takes weeks and costs thousands. A national poll requires weeks of fieldwork. AI Mirror Jury gives you a credible, diverse, grounded panel in under a minute.

---

## How it works

```
┌─────────────────────┐    ┌──────────────────────────────┐    ┌─────────────────────┐
│  Public Dataset     │    │  AI Jurors                   │    │  Aggregated Result  │
│                     │    │                              │    │                     │
│  Persona-Hub        │───▶│  Each juror is a real-world  │───▶│  Position tally     │
│  200k+ personas     │    │  persona from the dataset.   │    │  Majority verdict   │
│  (CC-BY 4.0)        │    │  They reason from verified   │    │  Confidence score   │
│                     │    │  facts — not hallucinations. │    │  Individual quotes  │
└─────────────────────┘    └──────────────────────────────┘    └─────────────────────┘
         │                            │
         │  Sample N personas         │  Optionally run deliberation:
         │  to form jury              │  jurors see each other's reasoning
         │                            │  and may update their position
```

**1. Load personas** from [Persona-Hub](https://huggingface.co/datasets/proj-persona/PersonaHub) — 200,000+ diverse human profiles spanning age, occupation, location, values, and lived experience. Licensed CC-BY 4.0, freely available on HuggingFace.

**2. Anchor to facts** — every Case comes with sourced, verified facts. Jurors are instructed to reason *only* from these facts plus their personal values. No hallucinated statistics.

**3. Poll in parallel** — each juror deliberates independently via the Claude API with prompt caching on their persona, keeping costs low.

**4. Deliberate** *(optional)* — in round 2, jurors see each other's reasoning. They may update their position or dig in. Mirrors how real jury deliberation works.

**5. Aggregate** — get a tally, majority verdict, average confidence, and the full text of each juror's reasoning.

---

## Quickstart

```bash
git clone https://github.com/li-xingchang/ai-mirror-jury
cd ai-mirror-jury
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...

# Single-round verdict on a pre-built scenario
python examples/basic_verdict.py

# Two-round deliberation
python examples/deliberation.py

# Run all 6 built-in scenarios
python examples/run_all_scenarios.py

# Your own personas + your own question
python examples/custom_dataset.py --file personas.csv --question "Should we launch this feature?"
```

---

## Built-in scenarios

Every scenario includes real, sourced facts so jurors can't fabricate supporting evidence.

| Scenario | Key facts sourced from |
|---|---|
| `FOUR_DAY_WORK_WEEK` | Iceland trial (ALDA 2021), UK pilot (Autonomy 2023), BLS |
| `AI_REGULATION` | EU AI Act, Biden EO, Pew Research, NCSL |
| `SOCIAL_MEDIA_AGE_LIMITS` | Australian Online Safety Act, JAMA Pediatrics, Surgeon General |
| `UNIVERSAL_BASIC_INCOME` | Stockton SEED study, Finnish UBI trial, CBO, Alaska PFD |
| `CRIMINAL_SENTENCING_REFORM` | BJS federal prison data, First Step Act, ACLU, NIJ |
| `CLIMATE_CARBON_TAX` | Canada carbon price, EPA inventory, IMF working paper, CBO |

```python
from mirror_jury.scenarios import AI_REGULATION, ALL_SCENARIOS
```

---

## Sample output

```
==================================================
JURY VERDICT  (8 jurors)
==================================================
  yes, with guardrails          4 /  8  (50%)
  no, self-regulation           2 /  8  (25%)
  yes, for highest-risk only    2 /  8  (25%)

Majority position : yes, with guardrails
Avg confidence    : 0.71
==================================================

INDIVIDUAL VERDICTS:

[ph_0003] yes, with guardrails (82% confident)
  As a small business owner I've seen how unregulated tech can create unfair advantages.
  The EU AI Act shows it's possible without killing innovation — I'd want the same here.

[ph_0011] no, self-regulation (65% confident)
  Government moves too slowly. By the time Congress acts, the technology will have changed
  completely. I'd rather see industry standards led by the labs themselves.
...
```

---

## Code API

```python
from mirror_jury import Case, JuryPanel, Deliberation, JuryAggregator
from mirror_jury.datasets import PersonaHubDataset
from mirror_jury.scenarios import FOUR_DAY_WORK_WEEK

# Use a built-in scenario (facts already sourced)
case = FOUR_DAY_WORK_WEEK

# Or build your own with grounding facts
case = Case(
    question="Should we require calorie labels on alcohol?",
    context="The FDA is considering mandatory calorie labeling for beer, wine, and spirits.",
    facts=[
        "A standard 5oz glass of wine contains ~120 calories.",
        "The US requires calorie labels on most packaged foods but not alcohol.",
        "A 2021 JAMA study found calorie labels on menus reduced fast food orders by ~8%.",
    ],
    sources=["FDA Alcohol Labeling Rulemaking, 2023", "JAMA, 'Menu Labeling Effects,' 2021"],
    options=["Yes, require labels", "No, keep voluntary"],
)

# Seat a jury
dataset = PersonaHubDataset(seed=42)
panel = JuryPanel(dataset=dataset, size=12, max_workers=4).seat()

# Single-round verdict
verdicts = panel.poll(case)

# Or multi-round deliberation
deliberation = Deliberation(panel=panel, rounds=2)
all_rounds = deliberation.run(case)
verdicts = Deliberation.final_verdicts(all_rounds)

# Report
agg = JuryAggregator(verdicts)
print(agg.report())           # tally + majority
print(agg.detailed_report())  # + each juror's full reasoning
```

---

## Why answers stay grounded

The biggest risk in LLM-powered simulations is **hallucination** — jurors inventing statistics, citing studies that don't exist, or confidently stating false facts as justification.

AI Mirror Jury prevents this with three layers:

1. **Sourced facts in every Case** — the `facts` field contains verified, cited data points. Every built-in scenario is sourced from government reports, peer-reviewed studies, or major news investigations.

2. **Explicit grounding instruction** — every juror's prompt includes: *"Do NOT invent statistics, cite studies, or reference events not listed in the facts. If uncertain, express that rather than fabricating details."*

3. **Persona-only reasoning** — jurors are instructed to combine the provided facts with their *personal values and lived experience*, not general knowledge. This keeps responses authentic to their character without opening the door to fabrication.

---

## Key classes

| Class | Description |
|---|---|
| `Case` | Question + context + **sourced facts** + optional answer choices |
| `Persona` | A single juror profile from the dataset |
| `Juror` | Claude-backed juror; returns a `Verdict` with position, reasoning, confidence |
| `JuryPanel` | Samples personas, seats jurors, polls them in parallel |
| `Deliberation` | Multi-round loop; jurors react to each other's reasoning |
| `JuryAggregator` | Tallies positions, finds majority, formats reports |
| `PersonaHubDataset` | Loads from Persona-Hub on HuggingFace (auto-cached) |
| `CustomFileDataset` | Loads from a local `.csv` or `.jsonl` file |

---

## Use cases

- **Policy research** — gauge how different demographic groups respond to a proposed law before it's introduced
- **Product decisions** — simulate how your target users would react to a new feature or pricing change
- **Journalism** — give diverse voices to a story before interviews are complete
- **Education** — run classroom simulations of real public debates with grounded evidence
- **Ethics review** — surface how different communities would be affected by an AI system's decisions

---

## Running tests

```bash
pip install pytest
pytest
```

All core logic is tested without API calls.

---

## Requirements

- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable
- `pip install -r requirements.txt` installs `anthropic` and `datasets`

---

## Dataset

**Persona-Hub** (`proj-persona/PersonaHub`) — a public dataset of 200,000+ diverse human persona descriptions, released by Microsoft Research under the Creative Commons Attribution 4.0 license. Downloaded automatically on first use and cached in `~/.cache/huggingface/`.

Bring your own personas with `CustomFileDataset` — any `.csv` or `.jsonl` with a `description` or `persona` column works.

---

## License

MIT
