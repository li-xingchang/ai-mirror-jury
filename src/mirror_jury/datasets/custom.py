"""
Load personas from any local CSV / JSONL file, or from a HuggingFace dataset path.

CSV/JSONL must have at least a column/field named "description" or "persona".
"""

import csv
import json
import random
from pathlib import Path

from mirror_jury.core.persona import Persona
from mirror_jury.datasets.base import BaseDataset


class CustomFileDataset(BaseDataset):
    """Load personas from a local .csv or .jsonl file."""

    def __init__(self, path: str | Path, seed: int = 42):
        self._path = Path(path)
        self._seed = seed
        self._rows: list[dict] | None = None

    def _ensure_loaded(self):
        if self._rows is not None:
            return
        suffix = self._path.suffix.lower()
        if suffix == ".csv":
            with open(self._path, newline="", encoding="utf-8") as f:
                self._rows = list(csv.DictReader(f))
        elif suffix in (".jsonl", ".ndjson"):
            with open(self._path, encoding="utf-8") as f:
                self._rows = [json.loads(line) for line in f if line.strip()]
        elif suffix == ".json":
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
                self._rows = data if isinstance(data, list) else [data]
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def size(self) -> int:
        self._ensure_loaded()
        return len(self._rows)

    def load(self, n: int) -> list[Persona]:
        self._ensure_loaded()
        rng = random.Random(self._seed)
        sample = rng.sample(self._rows, min(n, len(self._rows)))
        return [self._to_persona(i, row) for i, row in enumerate(sample)]

    def _to_persona(self, idx: int, row: dict) -> Persona:
        description = row.get("description") or row.get("persona") or str(row)
        return Persona(
            id=row.get("id", f"custom_{idx:04d}"),
            description=str(description).strip(),
            source=str(self._path.name),
            metadata={k: v for k, v in row.items() if k not in ("description", "persona", "id")},
        )
