from __future__ import annotations
from abc import ABC, abstractmethod
from mirror_jury.core.persona import Persona


class BaseDataset(ABC):
    @abstractmethod
    def load(self, n: int) -> list[Persona]:
        """Sample n personas from the dataset."""
        ...

    @abstractmethod
    def size(self) -> int:
        """Return total number of personas available."""
        ...
