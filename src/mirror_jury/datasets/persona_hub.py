"""
Loader for the Persona-Hub dataset.

  HuggingFace: proj-persona/PersonaHub
  License: Creative Commons Attribution 4.0
  Size: ~200,000 diverse human personas

The dataset ships several subsets; we default to "persona" which contains
plain-text descriptions usable as juror system prompts.
"""

import random
from mirror_jury.core.persona import Persona
from mirror_jury.datasets.base import BaseDataset


class PersonaHubDataset(BaseDataset):
    """Load personas from PersonaHub (proj-persona/PersonaHub on HuggingFace)."""

    DATASET_NAME = "proj-persona/PersonaHub"
    DEFAULT_SPLIT = "train"

    def __init__(self, subset: str = "persona", seed: int = 42):
        self._subset = subset
        self._seed = seed
        self._data = None

    def _ensure_loaded(self):
        if self._data is not None:
            return
        try:
            from datasets import load_dataset
        except ImportError as e:
            raise ImportError(
                "Install the 'datasets' package: pip install datasets"
            ) from e

        ds = load_dataset(self.DATASET_NAME, self._subset, split=self.DEFAULT_SPLIT)
        self._data = list(ds)

    def size(self) -> int:
        self._ensure_loaded()
        return len(self._data)

    def load(self, n: int) -> list[Persona]:
        self._ensure_loaded()
        rng = random.Random(self._seed)
        sample = rng.sample(self._data, min(n, len(self._data)))
        return [self._to_persona(i, row) for i, row in enumerate(sample)]

    def _to_persona(self, idx: int, row: dict) -> Persona:
        description = row.get("persona") or row.get("description") or str(row)
        return Persona(
            id=f"ph_{idx:04d}",
            description=description.strip(),
            source="persona_hub",
            metadata={"subset": self._subset},
        )
