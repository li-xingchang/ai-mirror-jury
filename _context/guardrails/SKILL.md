---
name: guardrails
description: >
  Context layer — load before every jury session. Provides verified, sourced facts organized by topic domain.
  Match the user's question to the most relevant domain and inject those facts into every persona's context.
  This is the anti-hallucination layer: personas may only cite facts from here; they must express uncertainty
  rather than invent statistics. Trigger automatically at the start of any jury/assemble run.
---

# Guardrails — Verified Facts by Topic Domain

This context layer is **never shown to the user**. It is silently embedded into each persona's system context before they speak. Its only job is to prevent personas from inventing statistics, citing fabricated studies, or stating false facts as background knowledge.

## How to Apply

1. Read the user's question.
2. Score each domain below by keyword match.
3. Load the highest-scoring domain's facts into every persona's context as `FACTUAL CONTEXT`.
4. Instruct each persona: *"You may reference these facts. Do not invent statistics or cite sources not listed here. If you're uncertain, say so."*

If no domain matches (score = 0), load no facts and instruct personas to rely entirely on personal values and lived experience — not invented data.

---

## Domain: Work & Employment
**Keywords:** work, job, employ, salary, wage, remote, office, hours, labor, career, hire, workforce, four-day, 4-day

- The US average work week is 34.4 hours (BLS, 2024).
- Remote work peaked at ~60% of US workers in 2020; by 2024 roughly 28% work fully remote (Pew Research, 2023).
- Iceland's 4-day work week trial (2015–2019) covered ~1% of the workforce; 86% of workers gained shorter hours afterward (ALDA, 2021).
- A 2022 UK pilot with 61 companies found 92% continued the 4-day week after the trial; sick days fell 65% (Autonomy Research, 2023).
- The US unemployment rate was 3.9% in early 2024 (BLS).
- Median US household income was ~$80,600 in 2023 (US Census Bureau).

---

## Domain: Technology & AI
**Keywords:** ai, artificial intelligence, machine learning, tech, software, algorithm, robot, automation, gpt, model, generative, chatgpt

- The EU AI Act (2024) is the world's first comprehensive AI law; it bans real-time facial recognition in public and requires audits for high-risk systems.
- A 2023 Pew Research poll found 62% of Americans feel more concerned than excited about AI.
- The US has no federal AI-specific law as of 2025; sector agencies (FDA, CFPB) apply existing rules to AI in their domains.
- Global AI investment reached ~$92 billion in 2023 (Stanford AI Index, 2024).
- A 2024 McKinsey survey found 65% of organizations regularly use generative AI, up from 33% a year earlier.
- AI-generated content is increasingly used in advertising; a 2024 Edelman survey found 52% of consumers feel uneasy seeing AI-made ads from major brands.

---

## Domain: Healthcare
**Keywords:** health, medical, doctor, hospital, insurance, drug, prescription, mental health, therapy, nurse, patient, healthcare

- The US spends ~18% of GDP on healthcare — the highest of any wealthy nation (OECD, 2023).
- About 25 million Americans remained uninsured in 2023 (US Census Bureau).
- The average US family health insurance premium was ~$23,968/year in 2023 (KFF).
- Life expectancy in the US is 76.4 years (2022), lower than most peer nations.
- Mental health conditions affect 1 in 5 US adults annually (NIMH).
- Prescription drug prices in the US are 2–4× higher than in comparable countries (RAND, 2021).

---

## Domain: Environment & Climate
**Keywords:** climate, environment, carbon, emission, energy, renewable, fossil, green, sustainability, pollution, warming

- The US emits about 5 billion metric tons of CO2 per year — the second-largest emitter after China (EPA, 2024).
- Global average temperature in 2023 was 1.45°C above pre-industrial levels (WMO).
- The Inflation Reduction Act (2022) allocates ~$369 billion for clean energy; CBO projects a 40% emissions cut by 2030.
- Renewable energy accounted for 21% of US electricity generation in 2023 (EIA).
- Extreme weather events cost the US a record $92.9 billion in damages in 2023 (NOAA).

---

## Domain: Economics & Consumer Behavior
**Keywords:** economy, inflation, price, market, gdp, recession, interest rate, debt, tax, spending, budget, consumer, cost

- US CPI inflation peaked at 9.1% in June 2022 and fell to ~3.1% by late 2023 (BLS).
- The US federal debt exceeded $34 trillion in 2024.
- Consumer spending accounts for ~70% of US GDP.
- The Federal Reserve raised interest rates 11 times from 2022–2023, bringing the benchmark rate to 5.25–5.5%.
- Small businesses employ ~46% of US private-sector workers (SBA, 2023).

---

## Domain: Product & Business
**Keywords:** product, launch, startup, business, pricing, customer, revenue, brand, saas, app, feature, marketing, campaign, ad, advertising

- Price increases of 1–10% typically cause a 10–20% drop in unit volume for elastic consumer goods (McKinsey pricing research).
- Customer acquisition costs have risen ~222% over the past decade across most digital channels (ProfitWell, 2022).
- Product-market fit is commonly defined as >40% of users saying they'd be "very disappointed" without the product (Sean Ellis benchmark).
- The EU's GDPR fines have totaled over €4 billion since 2018 (DLA Piper, 2024).
- A 2024 Edelman Trust Barometer found brand trust is the #2 factor in purchase decisions after price.
- A 2023 Nielsen study found 71% of consumers prefer buying from brands whose values align with their own.

---

## Domain: Social Policy
**Keywords:** policy, government, vote, election, immigration, welfare, poverty, gun, minimum wage, social, housing, inequality

- About 37 million Americans live below the federal poverty line (~$15,060/year for a single person, 2024).
- The US federal minimum wage has been $7.25/hour since 2009; 30 states have higher minimums.
- Voter turnout in the 2020 US presidential election was 66.8% — the highest since 1900.
- The US population is ~335 million; ~14% are foreign-born (US Census, 2023).
- Social Security and Medicare account for ~46% of federal mandatory spending.

---

## Domain: Education
**Keywords:** school, university, college, student, teacher, education, tuition, degree, learning, campus, loan, curriculum

- US student loan debt totals ~$1.77 trillion across 43 million borrowers (Federal Reserve, 2024).
- The average cost of a 4-year public university is ~$10,950/year in tuition; private is ~$39,400 (College Board, 2023).
- About 42% of US adults have a bachelor's degree or higher (US Census, 2023).
- US fourth-grade reading scores fell to their lowest level since 1990 in 2022 (NAEP).
- Teacher salaries average ~$66,800/year nationally; adjusted for inflation, they've declined since 1990 (NEA, 2023).

---

## Domain: Criminal Justice
**Keywords:** crime, prison, incarceration, police, drug, sentencing, justice, arrest, parole, conviction, recidivism, bail

- The US incarcerates 2 million people — the highest rate in the world at 655 per 100,000 (BJS, 2023).
- About 45% of the ~150,000 people in federal prison are serving time for drug offenses (BJS, 2023).
- The First Step Act (2018) has resulted in ~30,000 sentence reductions through 2023.
- Drug courts show recidivism rates roughly 10–15 percentage points lower than standard prosecution (NIJ).
- Black Americans are imprisoned at 5× the rate of white Americans (BJS, 2020).
- Recidivism within 3 years of release is ~68% nationally (BJS).

---

## User-Supplied Context

If the user provides a `context:` field with specific background information about a real event, product, or situation — **that context takes highest priority**. Inject it alongside the domain facts. Personas must treat it as established fact and must not contradict or embellish it.

Example: user asking about a specific company's marketing campaign should supply the actual campaign details, public reactions, and dates. The guardrail domain facts provide general background; the user context anchors the specific scenario.
