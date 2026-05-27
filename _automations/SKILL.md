---
name: automations
description: >
  Orchestration layer for AI Mirror Jury. Manages automated workflows that chain skills together into
  complete sessions. Trigger when the user says "run a full session," "start from scratch," "do a deep
  dive," "interview everyone," or any time a multi-skill workflow needs to be initiated. This skill is
  the conductor — it sequences assemble → speak-to / ask-all → synthesize in the right order, passes
  context through session state, and logs what happened.
---

# Automations — Orchestration Layer

## Architecture

```
LAYER 1: Context Loading
  guardrails + personas loaded at session start

LAYER 2: Core Skill Execution
  assemble → speak-to / ask-all (interleaved as needed) → synthesize

LAYER 3: Cross-Session
  session state persists; users can return to the same panel
```

---

## Available Workflows

| Workflow | File | When to use |
|---|---|---|
| Full Session | `workflows/full-session.md` | Standard end-to-end: question → panel → ask-all → 1-on-1s → synthesize |
| Deep Dive | `workflows/deep-dive.md` | Interview every person 1-on-1 before synthesizing |

---

## Session State Schema

`_automations/state/session.json`

```json
{
  "session_id": "mirror_[timestamp]",
  "started_at": "",
  "last_updated": "",
  "question": "",
  "user_context": "",
  "topic_domain": "",
  "guardrail_facts": [],
  "personas": [
    {
      "index": 1,
      "id": "juror_01",
      "brief": "",
      "full_description": ""
    }
  ],
  "active_persona_index": null,
  "conversations": {
    "1": [],
    "2": []
  },
  "group_exchanges": [
    {
      "message": "",
      "responses": [
        {"index": 1, "persona_brief": "", "response": ""}
      ]
    }
  ],
  "synthesis_complete": false,
  "workflow_log": []
}
```

---

## How to Start Any Workflow

```
User says: "Run a full session"
→ Load session state (or create new)
→ Check if panel is already assembled
→ Route to: workflows/full-session.md
→ Execute step by step
→ Update session state on completion
→ Summarize findings and offer next actions
```

Every workflow outputs:
1. **Panel** — who was assembled
2. **Responses** — what the panel said
3. **Synthesis** — patterns and takeaways
4. **State update** — session.json updated
5. **Log entry** — appended to workflow_log
