"""
Pre-built real-world scenarios with verified, sourced facts.

Each Case is grounded in documented, publicly available data so jurors
reason from evidence rather than hallucinated statistics.
"""

from mirror_jury.core.case import Case


FOUR_DAY_WORK_WEEK = Case(
    question="Should employers adopt a four-day, 32-hour work week at full pay?",
    context=(
        "Several large-scale pilots have tested the four-day work week across different "
        "industries and countries, producing mixed but largely positive results."
    ),
    facts=[
        "Iceland ran a 4-day work week trial from 2015–2019 across 2,500 workers (~1% of the workforce); "
        "86% of Icelandic workers have since moved to shorter hours or won the right to.",
        "A 2022 UK pilot with 61 companies found 92% continued the 4-day week after the trial; "
        "revenue rose 1.4% on average and sick days fell 65%.",
        "Microsoft Japan's 2019 trial reported a 40% productivity boost but lasted only one month.",
        "Critics note the UK pilot was voluntary — companies that enrolled likely already had "
        "cultures suited to flexible work.",
        "The US Bureau of Labor Statistics reports the average American works 34.4 hours/week; "
        "many already work fewer than 40 hours.",
        "32-hour mandates could disproportionately burden industries that cannot compress shifts, "
        "such as healthcare, retail, and manufacturing.",
    ],
    sources=[
        "Autonomy Research / UK 4-Day Week Pilot Report, Feb 2023",
        "Icelandic government / ALDA report, 2021",
        "Microsoft Japan press release, Nov 2019",
        "U.S. Bureau of Labor Statistics, Current Employment Statistics, 2024",
    ],
    options=["Yes, employers should adopt it", "No, it should not be mandated", "Depends on the industry"],
)


AI_REGULATION = Case(
    question="Should the US federal government regulate AI development with binding rules?",
    context=(
        "Governments worldwide are debating how — or whether — to impose legal requirements "
        "on companies building and deploying artificial intelligence systems."
    ),
    facts=[
        "The EU AI Act (2024) is the world's first comprehensive AI law; it bans certain uses "
        "(e.g. real-time facial recognition in public) and requires audits for 'high-risk' systems.",
        "President Biden's 2023 Executive Order on AI required safety testing and reporting for "
        "frontier AI models; the Trump administration rescinded it in Jan 2025.",
        "A 2023 Pew Research poll found 62% of Americans feel more concerned than excited about AI.",
        "The US has no federal AI-specific law as of 2025; sector-specific agencies (FDA, CFPB) "
        "apply existing rules to AI in their domains.",
        "Several states — including California, Colorado, and Illinois — have passed or proposed "
        "their own AI regulations.",
        "Leading AI labs (OpenAI, Anthropic, Google DeepMind) have each voluntarily agreed to "
        "safety commitments with the White House, but these are non-binding.",
    ],
    sources=[
        "EU AI Act, Official Journal of the European Union, 2024",
        "White House Executive Order on Safe AI, Oct 2023",
        "Pew Research Center, 'AI and Human Enhancement', Aug 2023",
        "National Conference of State Legislatures, AI Legislation Database, 2025",
    ],
    options=["Yes, pass binding federal rules", "No, self-regulation is sufficient", "Yes, but only for highest-risk systems"],
)


SOCIAL_MEDIA_AGE_LIMITS = Case(
    question="Should social media platforms be banned for children under 16?",
    context=(
        "Lawmakers in multiple countries are debating minimum age requirements for social media "
        "access, citing mental health research and child safety concerns."
    ),
    facts=[
        "Australia passed a law in 2024 banning under-16s from social media; platforms face "
        "fines up to AUD 50 million for systemic non-compliance.",
        "A 2023 meta-analysis in JAMA Psychiatry found 'screen time' had weak and inconsistent "
        "effects on adolescent mental health; effect sizes were small (r ≈ 0.05).",
        "The US Surgeon General called for warning labels on social media in 2024, "
        "comparing the risk to tobacco.",
        "A 2021 leaked Facebook internal study found Instagram was linked to negative body image "
        "in teenage girls in some surveys.",
        "Age verification at scale typically requires uploading government ID, raising "
        "significant privacy concerns.",
        "Researchers note that teens who are barred from major platforms may migrate to "
        "less-moderated alternatives.",
    ],
    sources=[
        "Australian Online Safety Amendment Act, 2024",
        "Coyne et al., JAMA Pediatrics, 2023",
        "U.S. Surgeon General Advisory, Jun 2023",
        "Wall Street Journal / Facebook internal documents, Sep 2021",
    ],
    options=["Yes, ban under-16s", "No, parental controls are sufficient", "Set the age limit at 13 with stricter enforcement"],
)


UNIVERSAL_BASIC_INCOME = Case(
    question="Should the US government implement a Universal Basic Income of $1,000/month for all adults?",
    context=(
        "UBI — unconditional cash payments to every citizen — has been piloted in several "
        "cities and countries, with mixed fiscal and social outcomes."
    ),
    facts=[
        "Stockton, CA's SEED pilot (2019–2021) gave 125 residents $500/month; "
        "full-time employment rose from 28% to 40% among recipients vs. 25% to 37% in the control group.",
        "Finland's 2017–2018 UBI trial (€560/month to 2,000 unemployed people) found improved "
        "wellbeing and mental health but no significant increase in employment.",
        "Andrew Yang's 2020 'Freedom Dividend' proposal of $1,000/month would cost ~$3 trillion/year "
        "— roughly 60% of the current federal budget.",
        "The Congressional Budget Office estimates roughly 37 million Americans live below the "
        "poverty line; the federal poverty level for a single person is ~$15,060/year (2024).",
        "Some economists warn UBI could increase inflation if not offset by tax increases "
        "or spending cuts elsewhere.",
        "Alaska has paid an annual Permanent Fund Dividend to residents since 1982; "
        "the 2023 payment was $1,312 per person.",
    ],
    sources=[
        "Stockton SEED Longitudinal Study, University of Pennsylvania, 2021",
        "Finnish Government / Kela UBI Experiment Final Report, 2020",
        "Committee for a Responsible Federal Budget, UBI cost estimate, 2019",
        "U.S. Census Bureau, Poverty Data, 2024",
        "Alaska Permanent Fund Corporation, 2023 Annual Report",
    ],
    options=["Yes, implement $1,000/month UBI", "No, targeted programs are better", "Yes, but only for those below the poverty line"],
)


CRIMINAL_SENTENCING_REFORM = Case(
    question="Should the US eliminate mandatory minimum sentences for nonviolent drug offenses?",
    context=(
        "Mandatory minimum laws require judges to impose fixed prison terms for certain crimes "
        "regardless of individual circumstances. Reform advocates and some conservatives "
        "have called for repeal."
    ),
    facts=[
        "The US incarcerates 2 million people — the highest rate in the world at 655 per 100,000.",
        "About 45% of the roughly 150,000 people in federal prison are serving time for drug offenses "
        "(Bureau of Justice Statistics, 2023).",
        "The First Step Act (2018), signed by President Trump, reduced some mandatory minimums "
        "and resulted in ~30,000 sentence reductions through 2023.",
        "A 2014 Pew Charitable Trusts report found states that reduced incarceration rates saw "
        "no corresponding increase in crime rates.",
        "Black Americans are imprisoned for drug offenses at roughly 10x the rate of white Americans "
        "despite similar usage rates (ACLU, 2020).",
        "Drug courts — diversion programs replacing incarceration with treatment — show "
        "recidivism rates roughly 10–15 percentage points lower than standard prosecution.",
    ],
    sources=[
        "Bureau of Justice Statistics, Federal Justice Statistics, 2023",
        "U.S. Sentencing Commission, First Step Act Report, 2023",
        "Pew Charitable Trusts, 'Max Out: The Rise in Prison Supervisors,' 2014",
        "ACLU, 'The War on Marijuana in Black and White,' 2020",
        "National Institute of Justice, Drug Courts Research Summary, 2022",
    ],
    options=["Yes, eliminate mandatory minimums for nonviolent drug offenses", "No, keep mandatory minimums", "Replace with drug courts / treatment mandates"],
)


CLIMATE_CARBON_TAX = Case(
    question="Should the US implement a national carbon tax?",
    context=(
        "A carbon tax places a fee on the carbon content of fossil fuels, intending to "
        "reduce emissions by making polluting more expensive. Several countries already have one."
    ),
    facts=[
        "Canada implemented a federal carbon price of CAD 65/tonne in 2024; "
        "most households receive a quarterly rebate that exceeds what they pay in carbon costs.",
        "The US emits about 5 billion metric tons of CO2 per year, making it the second-largest "
        "emitter after China.",
        "A 2019 IMF study found a $75/tonne carbon tax in the US could reduce emissions 35% "
        "by 2030 and raise ~1.1% of GDP in revenue.",
        "The Inflation Reduction Act (2022) uses tax credits rather than a carbon price; "
        "the CBO projects it will reduce US emissions 40% below 2005 levels by 2030.",
        "A carbon border adjustment mechanism (CBAM) can prevent 'carbon leakage' where "
        "production simply moves to countries without carbon pricing.",
        "Low-income households spend a higher share of income on energy; "
        "without rebates, a carbon tax is regressive.",
    ],
    sources=[
        "Government of Canada, Carbon Pricing Overview, 2024",
        "EPA, U.S. Greenhouse Gas Inventory Report, 2024",
        "IMF Working Paper, 'Fiscal Policies for Paris Climate Strategies,' 2019",
        "Congressional Budget Office, IRA Climate Provisions Report, 2023",
    ],
    options=["Yes, implement a carbon tax with household rebates", "No, rely on subsidies and incentives instead", "Yes, but only with a carbon border adjustment"],
)


ALL_SCENARIOS: dict[str, Case] = {
    "four_day_work_week": FOUR_DAY_WORK_WEEK,
    "ai_regulation": AI_REGULATION,
    "social_media_age_limits": SOCIAL_MEDIA_AGE_LIMITS,
    "universal_basic_income": UNIVERSAL_BASIC_INCOME,
    "criminal_sentencing_reform": CRIMINAL_SENTENCING_REFORM,
    "climate_carbon_tax": CLIMATE_CARBON_TAX,
}
