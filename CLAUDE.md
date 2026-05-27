# AI Mirror Jury — Claude Skills Library

A Claude skills library for running interactive, grounded conversations with a diverse panel of AI personas. Ask any question, assemble a cohort of 5–10 people, speak to them one-on-one or all at once, and synthesize what you learned.

---

## Architecture

```
ai-mirror-jury/
├── CLAUDE.md                          ← You are here
├── _context/                          ← Load before every session
│   ├── guardrails/SKILL.md            ← Verified facts by topic domain (anti-hallucination)
│   └── personas/SKILL.md             ← Framework for generating diverse, believable personas
├── jury/                              ← Core skill suite
│   ├── assemble/SKILL.md             ← Take user's question → build the panel
│   ├── speak-to/SKILL.md             ← 1-on-1 persistent conversation with one juror
│   ├── ask-all/SKILL.md              ← Broadcast a message to the full panel
│   └── synthesize/SKILL.md           ← Find patterns and insights across all responses
└── _automations/
    ├── SKILL.md                       ← Orchestration layer
    ├── scripts/session_manager.py     ← Read/write session state
    ├── state/session.json             ← Live session state (gitignored)
    └── workflows/
        ├── full-session.md            ← Assemble → Ask all → Synthesize
        └── deep-dive.md              ← Assemble → 1-on-1 with everyone → Synthesize
```

---

## How It Works

**Two context layers load before any session begins:**

1. `_context/guardrails/` — Verified, sourced facts for 9 topic domains. Silently injected into every persona's context so they reason from real data, not hallucination.
2. `_context/personas/` — Demographic and psychographic framework that ensures the generated cohort is genuinely diverse, not a cluster of similar voices.

**Four core skills do the work:**

| Skill | What it does |
|---|---|
| `jury/assemble` | Reads the user's question, matches topic → loads guardrails, generates 5–10 diverse personas, displays the panel, writes session state |
| `jury/speak-to` | 1-on-1 mode: Claude fully embodies a selected persona; conversation history persists in session state across turns |
| `jury/ask-all` | Broadcasts a single message to every persona; each responds independently in character |
| `jury/synthesize` | Reads all session responses and extracts themes, consensus, divergence, and key quotes |

---

## Session Start Protocol

Always load context first, then assemble:

```
1. Read _context/guardrails/SKILL.md
2. Read _context/personas/SKILL.md
3. Run jury/assemble  →  panel is ready
4. Use speak-to or ask-all as needed
5. Run jury/synthesize when done
```

---

## Session State

All skills share a single state file at `_automations/state/session.json`.

```json
{
  "session_id": "",
  "question": "",
  "topic_domain": "",
  "guardrail_facts": [],
  "personas": [
    {
      "index": 1,
      "id": "juror_01",
      "brief": "A 34-year-old freelance graphic designer in Austin, TX.",
      "full_description": "..."
    }
  ],
  "active_persona_index": null,
  "conversations": {
    "1": [],
    "2": []
  },
  "group_exchanges": []
}
```

Use `python _automations/scripts/session_manager.py` to inspect or reset state.

---

## Workflow Trigger Map

| User says | Auto-fires |
|---|---|
| "I have a question I want to explore" | `jury/assemble` |
| "speak to [N]" / "talk to person [N]" | `jury/speak-to` |
| "ask everyone" / "what does the panel think" | `jury/ask-all` |
| "what are the patterns" / "synthesize" | `jury/synthesize` |
| "run a full session" / "start from scratch" | `workflows/full-session` |
| "do a deep dive" / "interview everyone" | `workflows/deep-dive` |

---

## Design Principles

1. **Context before personas** — Guardrails load before any persona speaks. No session without them.
2. **Personas reason from evidence, not imagination** — They can only cite facts in the guardrails. If they don't know, they say so.
3. **Diversity is structural** — The persona framework enforces spread across age, occupation, geography, and values — not left to chance.
4. **Conversations persist** — 1-on-1 history is preserved in session state. You can come back to a persona multiple times.
5. **Synthesize last** — Synthesis runs after enough data is gathered, never mid-session.
