---
name: personas
description: >
  Context layer — load before jury/assemble. Defines the framework for generating a cohort of
  5–10 diverse, believable personas. Ensures demographic and psychographic spread so the panel
  reflects a genuine cross-section of people, not a cluster of similar voices. Trigger automatically
  at the start of any jury/assemble run, after guardrails are loaded.
---

# Persona Generation Framework

This context layer gives Claude the rules and templates for constructing a jury cohort. The goal is a panel that genuinely represents different kinds of people — not all college-educated, not all from the same region, not all with the same relationship to technology or institutions.

---

## Diversity Requirements

Every cohort of 5–10 personas **must** cover all four axes:

### 1. Age Spread
Include at least one persona from each of these brackets:
- **18–29** — early career, student, or first job
- **30–45** — mid-career, often parenting-age
- **46–60** — established, often managing others or approaching peak earning
- **61+** — near retirement or retired; different relationship to institutions and technology

### 2. Occupation Spread
Do not cluster in any single category. Cover at least 4 of these:
- **Professional / white-collar** (manager, analyst, lawyer, accountant, teacher, nurse, engineer)
- **Trades / blue-collar** (electrician, plumber, truck driver, construction worker, warehouse worker)
- **Small business / self-employed** (restaurant owner, freelancer, contractor, farmer)
- **Service / hourly** (retail worker, server, delivery driver, home health aide)
- **Student / no income** (undergraduate, graduate student, vocational trainee)
- **Retired / fixed income**
- **Creative / gig economy** (artist, designer, content creator, musician)

### 3. Geography Spread
Cover at least 3 of these:
- **Urban** (major metro: NYC, LA, Chicago, Houston, etc.)
- **Suburban** (commuter belt around a mid-size or large city)
- **Rural / small town** (Midwest, Appalachia, rural South, Plains states)
- **Non-US** (if relevant to the question — include an international perspective where useful)

### 4. Values & Worldview Spread
Every cohort must include voices that lean in different directions:
- Someone skeptical of large institutions (government, corporations)
- Someone who trusts established systems and expertise
- Someone primarily motivated by economic concerns
- Someone primarily motivated by values or community
- Someone who is risk-tolerant and change-oriented
- Someone who is risk-averse and stability-oriented

---

## Persona Description Format

Each persona needs a full description (used in system prompt) and a brief (shown to user).

**Full description** (~150–250 words):
```
[Name optional — first name only or no name]
A [age]-year-old [occupation] [location context].

[2-3 sentences about their background, family situation, and how they got to where they are.]

[2-3 sentences about their values, what they care about, what frustrates them, and how they make decisions.]

[1-2 sentences about their relationship to the topic — what direct experience they have, if any.]
```

**Brief** (first sentence only, ≤ 120 chars):
```
A [age]-year-old [occupation] [location detail].
```

---

## Persona Generation Workflow

When `jury/assemble` calls for personas:

1. **Read the question** — identify the topic and who would plausibly have strong or varied opinions about it.
2. **Check diversity requirements** — plan the cohort before writing personas to ensure spread across all 4 axes.
3. **Write full descriptions** — each persona gets a coherent inner life, not just a demographic label.
4. **Generate briefs** — first sentence of each description.
5. **Number them 1–N** — used for `speak-to` targeting.

---

## Quality Bar

A good persona:
- Has a specific job title, not just "works in tech" or "in healthcare"
- Has a location that grounds them ("outside Columbus, OH" not just "the Midwest")
- Has an opinion shaped by their actual life experience, not by what an AI thinks that demographic believes
- Can disagree with other personas without it feeling forced
- Uses natural language — not corporate speak, not academic language, not AI-ese

A bad persona:
- "Sarah, 35, marketing professional who values work-life balance" (too generic)
- "A conservative from rural America" (demographic label masquerading as a person)
- Any persona whose entire identity is their opinion on the question

---

## Example Personas

**Example 1:**
> A 58-year-old electrician foreman in Youngstown, OH. He's been in the trades for 35 years, runs a crew of 12, and has seen two recessions take out small contractors around him. His kids are grown; his wife works part-time at a pharmacy. He's skeptical of anything that sounds like it came from a think tank and trusts people who've actually done the work. He's not on social media much but pays close attention to anything that affects his pension and healthcare costs.

**Example 2:**
> A 26-year-old UX designer at a mid-size SaaS company in Austin, TX. She moved from the Philippines at 16, put herself through UT Austin on scholarships, and is now paying off student loans while trying to save for a down payment. She cares deeply about fairness and representation in tech but is also pragmatic — she needs her job to work. She's highly online, reads a lot, and forms strong opinions quickly.

**Example 3:**
> A 71-year-old retired middle school principal from Flagstaff, AZ. She spent 38 years in public education, raised three kids as a single mom after her divorce in the 90s, and now volunteers at her church and watches her grandchildren two days a week. She trusts institutions but has grown more skeptical of corporate America over the last decade. She doesn't understand most technology but adapts when she has to.
