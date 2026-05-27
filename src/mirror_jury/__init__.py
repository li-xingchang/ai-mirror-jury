"""AI Mirror Jury — simulate how a diverse panel of people would respond to any question."""

from mirror_jury.core import Case, Persona, Verdict
from mirror_jury.datasets import BaseDataset, CustomFileDataset, PersonaHubDataset
from mirror_jury.jury import Deliberation, Juror, JuryPanel
from mirror_jury.analysis import JuryAggregator
from mirror_jury.scenarios import ALL_SCENARIOS

__all__ = [
    "Case",
    "Persona",
    "Verdict",
    "BaseDataset",
    "PersonaHubDataset",
    "CustomFileDataset",
    "Juror",
    "JuryPanel",
    "Deliberation",
    "JuryAggregator",
    "ALL_SCENARIOS",
]
