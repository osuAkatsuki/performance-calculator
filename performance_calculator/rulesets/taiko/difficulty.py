from __future__ import annotations

from dataclasses import dataclass

from performance_calculator.models.difficulty import DifficultyAttributes


@dataclass
class TaikoDifficultyAttributes(DifficultyAttributes):
    stamina_difficulty: float
    rhythm_difficulty: float
    colour_difficulty: float
    peak_difficulty: float
    great_hit_window: float
