from __future__ import annotations
"""
Contextual guardrails: verified facts injected silently into each persona's
system prompt to prevent hallucination during free-form conversation.

Facts are detected by keyword-matching the user's question to a topic domain.
They are never shown to the user — they simply constrain what the persona
can plausibly claim as factual background.
"""

_TOPIC_FACTS: dict[str, list[str]] = {
    "work_employment": [
        "The US average work week is 34.4 hours (BLS, 2024).",
        "Remote work peaked at ~60% of US workers in 2020; by 2024 roughly 28% work fully remote (Pew Research, 2023).",
        "Iceland's 4-day work week trial (2015–2019) covered ~1% of the workforce; 86% of workers gained shorter hours afterward.",
        "A 2022 UK pilot with 61 companies found 92% continued the 4-day week; sick days fell 65%.",
        "The US unemployment rate was 3.9% in early 2024 (BLS).",
        "Median US household income was ~$80,600 in 2023 (US Census Bureau).",
    ],
    "tech_ai": [
        "The EU AI Act (2024) is the world's first comprehensive AI law; it bans real-time facial recognition in public and requires audits for high-risk systems.",
        "A 2023 Pew Research poll found 62% of Americans feel more concerned than excited about AI.",
        "The US has no federal AI-specific law as of 2025; sector agencies (FDA, CFPB) apply existing rules.",
        "OpenAI's GPT-4, Google's Gemini, and Anthropic's Claude are the leading frontier AI models as of 2025.",
        "Global AI investment reached ~$92 billion in 2023 (Stanford AI Index).",
        "A 2024 McKinsey survey found 65% of organizations regularly use generative AI, up from 33% a year earlier.",
    ],
    "healthcare": [
        "The US spends ~18% of GDP on healthcare — the highest of any wealthy nation (OECD, 2023).",
        "About 25 million Americans remained uninsured in 2023 (US Census Bureau).",
        "The average US family health insurance premium was ~$23,968/year in 2023 (KFF).",
        "Life expectancy in the US is 76.4 years (2022), lower than most peer nations.",
        "Mental health conditions affect 1 in 5 US adults annually (NIMH).",
        "Prescription drug prices in the US are 2–4× higher than in comparable countries (RAND, 2021).",
    ],
    "environment": [
        "The US emits about 5 billion metric tons of CO2 per year — the second-largest emitter after China (EPA, 2024).",
        "Global average temperature in 2023 was 1.45°C above pre-industrial levels (WMO).",
        "The Inflation Reduction Act (2022) allocates ~$369 billion for clean energy; CBO projects a 40% emissions cut by 2030.",
        "Renewable energy accounted for 21% of US electricity generation in 2023 (EIA).",
        "The US rejoined the Paris Agreement in 2021; it targets net-zero emissions by 2050.",
        "Extreme weather events cost the US a record $92.9 billion in damages in 2023 (NOAA).",
    ],
    "economics": [
        "US CPI inflation peaked at 9.1% in June 2022 and fell to ~3.1% by late 2023 (BLS).",
        "The US federal debt exceeded $34 trillion in 2024.",
        "US GDP growth was 2.5% in 2023, outperforming most other G7 economies.",
        "The Federal Reserve raised interest rates 11 times from 2022–2023, bringing the benchmark rate to 5.25–5.5%.",
        "Consumer spending accounts for ~70% of US GDP.",
        "Small businesses employ ~46% of US private-sector workers (SBA, 2023).",
    ],
    "product_business": [
        "Price increases of 1–10% typically cause a 10–20% drop in unit volume for elastic consumer goods (McKinsey pricing research).",
        "Customer acquisition costs have risen ~222% over the past decade across most digital channels (ProfitWell, 2022).",
        "Net Promoter Score (NPS) benchmarks vary widely: SaaS median is ~31, consumer apps median is ~36.",
        "The average successful SaaS company spends ~15–25% of revenue on sales and marketing.",
        "Product-market fit is commonly defined as >40% of users saying they'd be 'very disappointed' without the product (Sean Ellis benchmark).",
        "The EU's GDPR fines have totaled over €4 billion since 2018, with Meta alone paying €1.2 billion (2023).",
    ],
    "social_policy": [
        "About 37 million Americans live below the federal poverty line (~$15,060/year for a single person, 2024).",
        "The US federal minimum wage has been $7.25/hour since 2009; 30 states have higher minimums.",
        "Voter turnout in the 2020 US presidential election was 66.8% — the highest since 1900.",
        "The US population is ~335 million; ~14% are foreign-born (US Census, 2023).",
        "Social Security and Medicare account for ~46% of federal mandatory spending.",
        "Gun deaths in the US reached a record ~48,830 in 2021, including suicides (CDC).",
    ],
    "education": [
        "US student loan debt totals ~$1.77 trillion across 43 million borrowers (Federal Reserve, 2024).",
        "The average cost of a 4-year public university is ~$10,950/year in tuition; private is ~$39,400 (College Board, 2023).",
        "US fourth-grade reading scores fell to their lowest level since 1990 in 2022 (NAEP).",
        "About 42% of US adults have a bachelor's degree or higher (US Census, 2023).",
        "Teacher salaries average ~$66,800/year nationally; adjusted for inflation, they've declined since 1990 (NEA, 2023).",
        "Charter schools enroll ~3.7 million students (~7% of public school enrollment) in the US.",
    ],
    "criminal_justice": [
        "The US incarcerates 2 million people — the highest rate in the world at 655 per 100,000 (BJS, 2023).",
        "About 45% of the ~150,000 people in federal prison are serving time for drug offenses (BJS, 2023).",
        "The First Step Act (2018) has resulted in ~30,000 sentence reductions through 2023.",
        "Drug courts show recidivism rates roughly 10–15 percentage points lower than standard prosecution (NIJ).",
        "Black Americans are imprisoned at 5× the rate of white Americans (BJS, 2020).",
        "Recidivism within 3 years of release is ~68% nationally (BJS).",
    ],
}

_TOPIC_KEYWORDS: dict[str, list[str]] = {
    "work_employment": ["work", "job", "employ", "salary", "wage", "remote", "office", "hours", "labor", "career", "hire", "workforce"],
    "tech_ai": ["ai", "artificial intelligence", "machine learning", "tech", "software", "algorithm", "robot", "automation", "gpt", "claude", "model"],
    "healthcare": ["health", "medical", "doctor", "hospital", "insurance", "drug", "prescription", "mental health", "therapy", "nurse", "patient"],
    "environment": ["climate", "environment", "carbon", "emission", "energy", "renewable", "fossil", "green", "sustainability", "pollution"],
    "economics": ["economy", "inflation", "price", "market", "gdp", "recession", "interest rate", "debt", "tax", "spending", "budget"],
    "product_business": ["product", "launch", "startup", "business", "pricing", "customer", "revenue", "market", "brand", "saas", "app", "feature"],
    "social_policy": ["policy", "government", "vote", "election", "immigration", "welfare", "poverty", "gun", "minimum wage", "social"],
    "education": ["school", "university", "college", "student", "teacher", "education", "tuition", "degree", "learning", "campus"],
    "criminal_justice": ["crime", "prison", "incarceration", "police", "drug", "sentencing", "justice", "arrest", "parole", "conviction"],
}


def get_guardrail_facts(question: str) -> list[str]:
    """Return verified facts for the most relevant topic, or [] if no match."""
    q = question.lower()
    scores: dict[str, int] = {}
    for topic, keywords in _TOPIC_KEYWORDS.items():
        scores[topic] = sum(1 for kw in keywords if kw in q)
    best_topic = max(scores, key=scores.get)
    if scores[best_topic] == 0:
        return []
    return _TOPIC_FACTS[best_topic]
