# AI Mirror Jury

**Have a real conversation with a panel of diverse people — without scheduling a single interview.**

AI Mirror Jury assembles a cohort of 5–10 AI personas drawn from a public dataset of 200,000+ real human profiles. You can talk to them one-on-one or ask the whole group a question at once. Each persona stays in character, remembers the conversation, and responds from their own background, values, and lived experience.

---

## The idea

When you need to understand how people will react to something — a price change, a policy, a product feature — you typically have two options: slow and expensive (user interviews, focus groups, surveys) or fast but shallow (asking a single AI to "think like a user").

AI Mirror Jury is a third option. You get a demographically diverse panel assembled instantly. You can probe them with follow-up questions. They push back. They have opinions shaped by who they are, not just by what you asked.

---

## How it works

**1. You ask a question.**
Any question — product, policy, business, social. The question determines which factual guardrails get loaded.

**2. A cohort of 5–10 personas is assembled.**
Personas are sampled from [Persona-Hub](https://huggingface.co/datasets/proj-persona/PersonaHub), a public dataset of 200,000+ diverse human profiles (CC-BY 4.0). Each one has a distinct background, job, location, and set of values.

**3. Verified facts are silently injected into each persona's context.**
To prevent hallucination, relevant real-world data (sourced from government reports, peer-reviewed studies, and public research) is loaded into each persona's system prompt. Personas can reference these facts but cannot invent their own statistics. The user never sees this — it just keeps responses grounded.

**4. You talk to them.**
- **1-on-1**: Pick a persona by number. Have a multi-turn conversation. They remember everything you've said.
- **Ask all**: Broadcast a single question and get independent responses from every persona at once.

---

## Quickstart

```bash
git clone https://github.com/li-xingchang/ai-mirror-jury
cd ai-mirror-jury
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Launch the interactive session
python -m mirror_jury
```

```
==============================
  AI MIRROR JURY
  Hear from a diverse panel — on any question.
==============================

What question do you want to explore?
> Should we raise our subscription price by 30%?

How many people in your panel? (5–10, default 7): 6

Assembling a panel of 6 people…
Done.

────────────────────────────────────────────────────────────
  YOUR PANEL
────────────────────────────────────────────────────────────
  [1] A 34-year-old freelance graphic designer in Austin, TX.
  [2] A 52-year-old retired school principal from rural Ohio.
  [3] A 28-year-old startup founder based in New York City.
  [4] A 67-year-old grandmother and part-time bookkeeper in Florida.
  [5] A 41-year-old nurse practitioner in a Chicago suburb.
  [6] A 23-year-old college student studying economics in California.
────────────────────────────────────────────────────────────

Commands:
  speak <N>   — 1-on-1 with person N (conversation persists)
  ask all     — Ask everyone the same question at once
  list        — Show the panel again
  help        — Show this menu
  quit        — Exit

> speak 3
────────────────────────────────────────────────────────────
  1-on-1 with person [3]
  A 28-year-old startup founder based in New York City.
  (type 'back' to return to the panel)
────────────────────────────────────────────────────────────

You: What's your gut reaction to a 30% price increase?
[3]: Honestly, as a founder myself I've been on both sides of this.
A 30% jump is aggressive — I'd need to see a real reason why...

You: Would a new feature justify it?
[3]: Depends entirely on the feature. If it saves me time or money,
sure. But "we added AI" is not a reason to pay 30% more...

You: back

> ask all
Your message to everyone: What one thing would make you accept a 30% price increase?

[1] A 34-year-old freelance graphic designer in Austin, TX.
  Honestly, if the product suddenly saved me 3 hours a week, I'd
  pay it without thinking twice. But that bar is real...

[2] A 52-year-old retired school principal from rural Ohio.
  I'd need to know my data is safe and my account won't disappear.
  Trust matters more to me than features at this point...
...
```

---

## Python API

```python
from mirror_jury import MirrorJury, ResponseSummary

# Assemble your panel
jury = MirrorJury(
    question="Should we launch in Europe or the US first?",
    cohort_size=7,
    seed=42,
).assemble()

# See who's in the panel
for p in jury.list_personas():
    print(f"[{p['index']}] {p['brief']}")

# Multi-turn 1-on-1 conversation (history persists)
r = jury.speak_to(1, "What's your gut reaction?")
print(r.message)

r = jury.speak_to(1, "What would change your mind?")
print(r.message)

# Ask everyone at once
responses = jury.speak_to_all("What's the biggest risk of launching in Europe first?")
ResponseSummary(responses).print_all()
```

---

## Bring your own personas

Drop in any `.csv` or `.jsonl` file with a `description` or `persona` field:

```python
from mirror_jury import MirrorJury
from mirror_jury.datasets import CustomFileDataset

jury = MirrorJury(
    question="...",
    dataset=CustomFileDataset("my_personas.csv"),
).assemble()
```

---

## Why personas stay grounded

Free-form AI conversations carry a hallucination risk: a persona might invent a statistic, cite a study that doesn't exist, or confidently state something false to support their character's view.

AI Mirror Jury addresses this with **contextual guardrails** — a silent layer of verified, sourced facts loaded into each persona's system prompt based on the topic of your question. Personas can reference these facts but are explicitly instructed not to invent statistics or cite sources beyond what's provided.

The guardrails cover 9 topic domains (technology & AI, healthcare, work & employment, economics, environment, criminal justice, education, social policy, and product & business), each sourced from government data, peer-reviewed studies, and major public research. The user never sees them — they simply keep the conversation honest.

---

## Dataset

**[Persona-Hub](https://huggingface.co/datasets/proj-persona/PersonaHub)** (`proj-persona/PersonaHub`) — 200,000+ diverse human persona descriptions released by Microsoft Research under CC-BY 4.0. Downloaded automatically on first use via the HuggingFace `datasets` library and cached in `~/.cache/huggingface`.

---

## Running tests

```bash
pip install pytest
pytest
```

No API calls required to run the test suite.

---

## Requirements

- Python 3.11+
- `ANTHROPIC_API_KEY` set in your environment
- `pip install -r requirements.txt`

---

## License

MIT
