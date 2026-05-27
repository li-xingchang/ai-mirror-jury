"""Unit tests for core data structures (no API calls required)."""

import pytest
from mirror_jury.core import Case, Persona, Verdict
from mirror_jury.analysis import JuryAggregator


def make_verdicts(positions: list[str]) -> list[Verdict]:
    return [
        Verdict(juror_id=f"j{i}", position=p, reasoning="test", confidence=0.8)
        for i, p in enumerate(positions)
    ]


def test_case_renders_question():
    c = Case(question="Is this a test?")
    assert "Is this a test?" in c.render()


def test_case_renders_options():
    c = Case(question="Pick one.", options=["A", "B"])
    rendered = c.render()
    assert "A" in rendered and "B" in rendered


def test_persona_system_prompt():
    p = Persona(id="p1", description="A retired teacher from Ohio.")
    prompt = p.to_system_prompt()
    assert "retired teacher" in prompt


def test_verdict_summary():
    v = Verdict(juror_id="j1", position="yes", reasoning="Because.", confidence=0.9)
    assert "j1" in v.summary()
    assert "yes" in v.summary()


def test_aggregator_tally():
    verdicts = make_verdicts(["yes", "yes", "no", "yes"])
    agg = JuryAggregator(verdicts)
    tally = agg.tally()
    assert tally["yes"] == 3
    assert tally["no"] == 1


def test_aggregator_majority():
    verdicts = make_verdicts(["yes", "yes", "no", "yes"])
    agg = JuryAggregator(verdicts)
    assert agg.majority() == "yes"


def test_aggregator_hung_jury():
    verdicts = make_verdicts(["yes", "no"])
    agg = JuryAggregator(verdicts)
    assert agg.majority() is None


def test_aggregator_report_contains_totals():
    verdicts = make_verdicts(["yes", "no", "yes"])
    report = JuryAggregator(verdicts).report()
    assert "3 jurors" in report or "3)" in report or "3" in report
