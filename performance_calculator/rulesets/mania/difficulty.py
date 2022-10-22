from __future__ import annotations

from dataclasses import dataclass

from performance_calculator.models.difficulty import DifficultyAttributes


@dataclass
class ManiaDifficultyAttributes(DifficultyAttributes):
    great_hit_window: int
