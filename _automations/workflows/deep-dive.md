# Workflow: Deep Dive

**When to use:** You want a richer, more qualitative read — interview every person individually before synthesizing. Best when nuance, emotional texture, and follow-up matter more than breadth.

**Trigger phrases:** "do a deep dive," "interview everyone," "I want to go deep with each person," "1-on-1 with the whole panel"

---

## Step 1 — Assemble
Run `jury/assemble`:
- Capture question, optional context
- Recommend a smaller panel (5–6 people) — deep dives get expensive at 10
- Generate personas, display panel, write session state

## Step 2 — Structured 1-on-1 Interviews
For each persona (index 1 → N), run `jury/speak-to` with a consistent opening question, then let the user probe:

**Opening question (same for all):**
> "[User's original question] — what's your honest take?"

After the opening response, the user may ask 1–3 follow-up questions before moving to the next person.

**Standard follow-up prompts** (suggest these if the user isn't sure what to ask):
1. "What personal experience shapes that view?"
2. "What would change your mind?"
3. "What do you think people like you are most worried about?"

At the end of each 1-on-1:
```
  → Continue to person [N+1]? (yes / stay here / skip)
```

Log each conversation to `conversations[index]` in session state.

## Step 3 — Mid-Session Check-In
After interviewing half the panel (e.g. after person 3 of 6):
```
  Halfway through. Anything you want to adjust for the remaining interviews?
  (You can add a follow-up question, skip someone, or continue as-is)
```

## Step 4 — Synthesize
Run `jury/synthesize` after all interviews are complete:
- Deep dive synthesis should be richer than a standard session — more quotes, more nuance
- Explicitly note patterns *within* individual conversations (not just across personas)
- Flag any persona who changed position or expressed ambivalence mid-conversation
- Set `synthesis_complete: true`

## Step 5 — Offer Next Actions
```
Deep dive complete.

Options:
  → Run an ask-all to test a specific finding across the whole panel
  → Start a new session with a different question
  → Export the synthesis as a summary document
```
