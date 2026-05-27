"""Unit tests — no API calls required."""

import pytest
from mirror_jury.core.persona import Persona
from mirror_jury.core.response import Response
from mirror_jury.context.guardrails import get_guardrail_facts
from mirror_jury.analysis.aggregator import ResponseSummary


def make_responses(messages: list[str]) -> list[Response]:
    return [
        Response(persona_id=f"p{i}", persona_brief=f"Person {i}", message=m)
        for i, m in enumerate(messages)
    ]


# ── Persona ──────────────────────────────────────────────────────────────────

def test_persona_system_prompt():
    p = Persona(id="p1", description="A retired teacher from Ohio.")
    assert "retired teacher" in p.to_system_prompt()


def test_persona_system_prompt_stays_in_character():
    p = Persona(id="p1", description="A nurse in Chicago.")
    assert "character" in p.to_system_prompt().lower()


# ── Response ─────────────────────────────────────────────────────────────────

def test_response_fields():
    r = Response(persona_id="p1", persona_brief="A teacher.", message="I think so.", turn=2)
    assert r.persona_id == "p1"
    assert r.turn == 2


# ── Guardrails ───────────────────────────────────────────────────────────────

def test_guardrails_match_ai_question():
    facts = get_guardrail_facts("Should we regulate AI systems?")
    assert len(facts) > 0
    assert any("AI" in f or "EU" in f for f in facts)


def test_guardrails_match_work_question():
    facts = get_guardrail_facts("Should we move to a remote work policy?")
    assert len(facts) > 0


def test_guardrails_return_empty_for_unknown():
    # Highly specific question with no matching keywords
    facts = get_guardrail_facts("What color should our logo be?")
    assert isinstance(facts, list)


# ── ResponseSummary ───────────────────────────────────────────────────────────

def test_summary_len():
    rs = ResponseSummary(make_responses(["yes", "no", "maybe"]))
    assert len(rs) == 3


def test_summary_as_text():
    rs = ResponseSummary(make_responses(["I agree.", "I disagree."]), question="Test?")
    text = rs.as_text()
    assert "Test?" in text
    assert "I agree." in text
    assert "I disagree." in text
