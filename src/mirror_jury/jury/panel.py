"""Jury panel — assembles jurors from a dataset and collects first-round verdicts."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from mirror_jury.core.case import Case
from mirror_jury.core.persona import Persona
from mirror_jury.core.verdict import Verdict
from mirror_jury.datasets.base import BaseDataset
from mirror_jury.jury.juror import Juror


class JuryPanel:
    def __init__(self, dataset: BaseDataset, size: int = 12, max_workers: int = 4):
        self._dataset = dataset
        self._size = size
        self._max_workers = max_workers
        self._personas: list[Persona] = []
        self._jurors: list[Juror] = []

    def seat(self) -> "JuryPanel":
        """Sample personas from the dataset and seat the jury."""
        self._personas = self._dataset.load(self._size)
        self._jurors = [Juror(p) for p in self._personas]
        print(f"Seated {len(self._jurors)} jurors from '{self._dataset.__class__.__name__}'.")
        return self

    def poll(self, case: Case, prior_verdicts: list[Verdict] | None = None, round: int = 1) -> list[Verdict]:
        """Ask every juror for a verdict, running requests in parallel."""
        verdicts: list[Verdict] = []
        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            futures = {
                pool.submit(j.deliberate, case, prior_verdicts, round): j
                for j in self._jurors
            }
            for future in as_completed(futures):
                try:
                    verdicts.append(future.result())
                except Exception as exc:
                    juror = futures[future]
                    print(f"  Juror {juror.persona.id} raised an error: {exc}")
        verdicts.sort(key=lambda v: v.juror_id)
        return verdicts

    @property
    def jurors(self) -> list[Juror]:
        return self._jurors
