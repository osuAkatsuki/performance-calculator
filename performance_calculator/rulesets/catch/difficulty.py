from __future__ import annotations

from dataclasses import dataclass

from performance_calculator.models.difficulty import DifficultyAttributes


@dataclass
class CatchDifficultyAttributes(DifficultyAttributes):
    approach_rate: float
