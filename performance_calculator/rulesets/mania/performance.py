from __future__ import annotations

import math
from dataclasses import dataclass

from performance_calculator.models.mods import Mods
from performance_calculator.models.performance import PerformanceAttributes
from performance_calculator.models.performance import PerformanceCalculator
from performance_calculator.models.score import Score
from performance_calculator.rulesets.mania.difficulty import ManiaDifficultyAttributes


@dataclass
class ManiaPerformanceAttributes(PerformanceAttributes):
    difficulty: float


class ManiaPerformanceCalculator(PerformanceCalculator):
    difficulty_attributes: ManiaDifficultyAttributes

    def calculate(self, score: Score) -> ManiaPerformanceAttributes:
        count_perfect = score.num_gekis
        count_great = score.num_300s
        count_good = score.num_katus
        count_ok = score.num_100s
        count_meh = score.num_50s
        count_miss = score.num_misses

        total_hits = (
            count_perfect + count_ok + count_great + count_good + count_meh + count_miss
        )

        accuracy = 0.0
        if total_hits != 0:
            accuracy = (
                (count_perfect * 320)
                + (count_great * 300)
                + (count_good * 200)
                + (count_ok * 100)
                + (count_meh * 50)
            ) / (total_hits * 320)

        multiplier = 8.0

        if score.mods & Mods.NOFAIL:
            multiplier *= 0.75

        if score.mods & Mods.EASY:
            multiplier *= 0.5

        difficulty_value = self._compute_difficulty_value(accuracy, total_hits)
        total_value = difficulty_value * multiplier

        return ManiaPerformanceAttributes(
            total=total_value,
            difficulty=difficulty_value,
        )

    def _compute_difficulty_value(self, accuracy: float, total_hits: int) -> float:
        difficulty_value = (
            math.pow(max(self.difficulty_attributes.star_rating - 0.15, 0.05), 2.2)
            * max(0.0, 5.0 * accuracy - 4.0)
            * (1.0 + 0.1 * min(1.0, total_hits / 1500))
        )

        return difficulty_value
