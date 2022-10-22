from __future__ import annotations

import math
from dataclasses import dataclass

from performance_calculator.models.mods import Mods
from performance_calculator.models.performance import PerformanceAttributes
from performance_calculator.models.performance import PerformanceCalculator
from performance_calculator.models.score import Score
from performance_calculator.rulesets.taiko.difficulty import TaikoDifficultyAttributes


@dataclass
class TaikoPerformanceAttributes(PerformanceAttributes):
    difficulty: float
    accuracy: float
    effective_miss_count: float


class TaikoPerformanceCalculator(PerformanceCalculator):
    difficulty_attributes: TaikoDifficultyAttributes

    def calculate(self, score: Score) -> TaikoPerformanceAttributes:
        total_successful_hits = score.num_300s + score.num_100s + score.num_50s
        total_hits = total_successful_hits + score.num_misses

        accuracy = 0.0
        if total_hits > 0:
            accuracy = (score.num_300s * 300 + score.num_100s * 150) / (
                total_hits * 300.0
            )

        effective_miss_count = 0.0
        if total_successful_hits > 0:
            effective_miss_count = (
                max(1.0, 1000.0 / total_successful_hits) * score.num_misses
            )

        multiplier = 1.13

        if score.mods & Mods.HIDDEN:
            multiplier *= 1.075

        if score.mods & Mods.EASY:
            multiplier *= 0.975

        difficulty_value = self._compute_difficulty_value(
            score,
            total_hits,
            effective_miss_count,
            accuracy,
        )
        accuracy_value = self._compute_accuracy_value(
            score,
            total_hits,
            accuracy,
        )
        total_value = (
            math.pow(
                math.pow(difficulty_value, 1.1) + math.pow(accuracy_value, 1.1),
                1.0 / 1.1,
            )
            * multiplier
        )

        return TaikoPerformanceAttributes(
            total=total_value,
            difficulty=difficulty_value,
            accuracy=accuracy_value,
            effective_miss_count=effective_miss_count,
        )

    def _compute_difficulty_value(
        self,
        score: Score,
        total_hits: int,
        effective_miss_count: float,
        accuracy: float,
    ) -> float:
        difficulty_value = (
            math.pow(
                5 * max(1.0, self.difficulty_attributes.star_rating / 0.115) - 4.0,
                2.25,
            )
            / 1150.0
        )

        length_bonus = 1 + 0.1 * min(1.0, total_hits / 1500.0)
        difficulty_value *= length_bonus

        difficulty_value *= math.pow(0.986, effective_miss_count)

        if score.mods & Mods.EASY:
            difficulty_value *= 0.985

        if score.mods & Mods.HIDDEN:
            difficulty_value *= 1.025

        if score.mods & Mods.HARDROCK:
            difficulty_value *= 1.050

        if score.mods & Mods.FLASHLIGHT:
            difficulty_value *= 1.050 * length_bonus

        difficulty_value *= math.pow(accuracy, 2.0)
        return difficulty_value

    def _compute_accuracy_value(
        self,
        score: Score,
        total_hits: int,
        accuracy: float,
    ) -> float:
        if self.difficulty_attributes.great_hit_window <= 0:
            return 0

        accuracy_value = (
            math.pow(60.0 / self.difficulty_attributes.great_hit_window, 1.1)
            * math.pow(accuracy, 8.0)
            * math.pow(self.difficulty_attributes.star_rating, 0.4)
            * 27.0
        )

        length_bonus = min(1.15, math.pow(total_hits / 1500.0, 0.3))
        accuracy_value *= length_bonus

        if score.mods & Mods.FLASHLIGHT and score.mods & Mods.HIDDEN:
            accuracy_value *= max(1.050, 1.075 * length_bonus)

        return accuracy_value
