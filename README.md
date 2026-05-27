# AI Mirror Jury

A Claude skills library for running interactive conversations with a diverse panel of AI personas — on any question.

**Built by Li Chang** | Product × AI Practitioner

---

## What It Does

You ask a question. A cohort of 5–10 diverse people gets assembled. You can speak to anyone on the panel one-on-one or ask the whole group at once. Their responses are grounded in verified facts — not hallucinated statistics. When you're ready, synthesize everything into patterns, consensus, divergence, and key takeaways.

No surveys. No scheduling. No single AI opinion pretending to be many.

---

## Skill Architecture

```
ai-mirror-jury/
├── _context/
│   ├── guardrails/     ← Verified facts by topic (anti-hallucination layer)
│   └── personas/       ← Framework for diverse, believable cohorts
├── jury/
│   ├── assemble/       ← Question in → panel ready
│   ├── speak-to/       ← 1-on-1 with any juror (conversation persists)
│   ├── ask-all/        ← Broadcast to the whole panel
│   └── synthesize/     ← Patterns, consensus, divergence, quotes
└── _automations/
    ├── workflows/
    │   ├── full-session.md   ← End-to-end: assemble → ask-all → synthesize
    │   └── deep-dive.md      ← 1-on-1 with everyone → synthesize
    └── scripts/
        └── session_manager.py
```

---

## How to Use

### Option 1 — Let Claude Code route for you
Open this repo in Claude Code. Describe what you want and the right skill fires automatically:

```
"I want to explore how people would react to a 30% price increase"
→ fires jury/assemble

"speak to 3"
→ fires jury/speak-to

"ask everyone what the biggest risk is"
→ fires jury/ask-all

"what are the patterns"
→ fires jury/synthesize

"run a full session"
→ fires _automations/workflows/full-session
```

### Option 2 — Run a workflow end-to-end
Tell Claude Code to run `_automations/workflows/full-session.md` or `deep-dive.md` and it will walk through the entire session automatically.

### Option 3 — Invoke skills manually
Read any `SKILL.md` and follow it yourself inside a Claude conversation.

---

## The Guardrails Layer

Personas don't have free rein to invent facts. Before any session, `_context/guardrails/SKILL.md` loads verified, sourced data for 9 topic domains:

| Domain | Key sources |
|---|---|
| Work & Employment | BLS, ALDA, Autonomy Research |
| Technology & AI | EU AI Act, Pew Research, McKinsey, Edelman |
| Healthcare | OECD, KFF, NIMH, RAND |
| Environment | EPA, WMO, EIA, NOAA |
| Economics | BLS, Federal Reserve, SBA |
| Product & Business | McKinsey, ProfitWell, Edelman, Nielsen |
| Social Policy | US Census, CDC |
| Education | Federal Reserve, College Board, NEA |
| Criminal Justice | BJS, NIJ, ACLU |

Personas may only cite facts from the loaded domain. If they don't know something, they say so — they don't invent it.

**For specific events** (a real campaign, a company decision, a recent news story), supply your own context when assembling. It gets injected alongside the domain facts and takes highest priority.

---

## Session Commands

Once a panel is assembled:

| Command | What it does |
|---|---|
| `speak <N>` | Enter 1-on-1 mode with person N. Conversation history persists. |
| `ask all` | Broadcast a message. Every persona responds independently. |
| `list` | Show the panel again. |
| `synthesize` | Extract patterns, consensus, divergence, and key quotes. |
| `back` | Exit 1-on-1 mode and return to the panel menu. |

---

## Session State

All skills share `_automations/state/session.json` (gitignored). Inspect or reset it:

```bash
python _automations/scripts/session_manager.py            # show current state
python _automations/scripts/session_manager.py --personas # list the panel
python _automations/scripts/session_manager.py --reset    # start fresh
```

---

## Design Principles

1. **Context before personas** — Guardrails load before any persona speaks.
2. **Evidence, not imagination** — Personas reason from provided facts + personal values. No invented statistics.
3. **Diversity is structural** — The persona framework enforces spread across age, occupation, geography, and worldview. Not left to chance.
4. **Conversations persist** — 1-on-1 history is preserved. You can return to a persona and they remember what you discussed.
5. **Synthesize last** — Run synthesis after you've gathered enough — not mid-session.
