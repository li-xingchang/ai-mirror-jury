"""
AI Mirror Jury — interactive conversations with a diverse panel of AI personas.

Quickstart:
    jury = MirrorJury("Should we raise prices by 30%?").assemble()
    response = jury.speak_to(1, "What's your gut reaction?")
    responses = jury.speak_to_all("What's the biggest risk?")
"""

from mirror_jury.core import Persona, Response
from mirror_jury.datasets import BaseDataset, CustomFileDataset, PersonaHubDataset
from mirror_jury.session import ConversationalJuror, Cohort, MirrorJury
from mirror_jury.analysis import ResponseSummary

__all__ = [
    "Persona",
    "Response",
    "BaseDataset",
    "PersonaHubDataset",
    "CustomFileDataset",
    "ConversationalJuror",
    "Cohort",
    "MirrorJury",
    "ResponseSummary",
]
