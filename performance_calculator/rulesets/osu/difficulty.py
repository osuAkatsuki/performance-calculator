from __future__ import annotations

from dataclasses import dataclass

from performance_calculator.models.difficulty import DifficultyAttributes


@dataclass
class OsuDifficultyAttributes(DifficultyAttributes):
    aim_difficulty: float
    speed_difficulty: float
    speed_note_count: float
    flashlight_difficulty: float
    slider_factor: float
    approach_rate: float
    overall_difficulty: float
    drain_rate: float
    hit_circle_count: int
    slider_count: int
    spinner_count: int
