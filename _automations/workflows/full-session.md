# Workflow: Full Session

**When to use:** Standard end-to-end Mirror Jury session. Question → panel → ask-all → optional 1-on-1s → synthesis.

**Trigger phrases:** "run a full session," "start from scratch," "I want to explore a question," "let's do a jury session"

---

## Step 1 — Assemble
Run `jury/assemble`:
- Capture question, optional panel size, optional context
- Load guardrails for the detected domain
- Generate 5–10 diverse personas
- Display the panel
- Write session state

## Step 2 — Opening Ask-All
Run `jury/ask-all` with the user's original question verbatim:
- Broadcast to the full panel
- Display all responses
- Write to `group_exchanges[0]` in session state

## Step 3 — User-Directed Exploration
Hand control back to the user. They may:
- `speak <N>` — go 1-on-1 with someone who surprised them
- `ask all` again — probe a specific angle across the whole panel
- `synthesize` — skip exploration and go straight to insights

Log each action to `workflow_log`.

## Step 4 — Synthesize (when user is ready)
Run `jury/synthesize`:
- Read all group exchanges and 1-on-1 conversations
- Extract consensus, divergence, surprises
- Segment by demographics
- Output key quotes and actionable takeaways
- Set `synthesis_complete: true` in session state

## Step 5 — Offer Next Actions
```
Session complete.

Options:
  → Start a new session with a different question
  → Ask a follow-up question to the same panel
  → Go 1-on-1 with a specific persona to dig deeper
```
