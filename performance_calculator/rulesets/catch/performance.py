from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from performance_calculator.models.mods import Mods
from performance_calculator.models.performance import PerformanceAttributes
from performance_calculator.models.performance import PerformanceCalculator
from performance_calculator.models.score import Score
from performance_calculator.rulesets.catch.difficulty import CatchDifficultyAttributes


@dataclass
class CatchPerformanceAttributes(PerformanceAttributes):
    ...


clamp: Callable[[float, float, float], float] = (
    lambda x, l, u: l if x < l else u if x > u else x
)


class CatchPerformanceCalculator(PerformanceCalculator):
    difficulty_attributes: CatchDifficultyAttributes

    def calculate(self, score: Score) -> CatchPerformanceAttributes:
        fruits_hit = score.num_300s
        ticks_hit = score.num_100s
        tiny_ticks_hit = score.num_50s
        tiny_ticks_missed = score.num_katus
        misses = score.num_misses

        value = (
            math.pow(
                5.0 * max(1.0, self.difficulty_attributes.star_rating / 0.0049) - 4.0,
                2.0,
            )
            / 100000.0
        )

        total_combo_hits = misses + ticks_hit + fruits_hit
        total_hits = (
            tiny_ticks_hit + ticks_hit + fruits_hit + misses + tiny_ticks_missed
        )
        successful_hits = tiny_ticks_hit + ticks_hit + fruits_hit

        length_bonus = (
            0.95
            + 0.3 * min(1.0, total_combo_hits / 2500.0)
            + (
                (math.log10(total_combo_hits / 2500.0) * 0.475)
                * int(total_combo_hits > 2500)
            )
        )
        value *= length_bonus

        value *= math.pow(0.97, misses)

        if self.difficulty_attributes.max_combo > 0:
            value *= min(
                math.pow(score.max_combo, 0.8)
                / math.pow(self.difficulty_attributes.max_combo, 0.8),
                1.0,
            )

        approach_rate = self.difficulty_attributes.approach_rate
        approach_rate_factor = 1.0

        if approach_rate > 9.0:
            approach_rate_factor += 0.1 * (approach_rate - 9.0)

        if approach_rate > 10.0:
            approach_rate_factor += 0.1 * (approach_rate - 10.0)
        elif approach_rate < 8.0:
            approach_rate_factor += 0.025 * (8.0 - approach_rate)

        value *= approach_rate_factor

        if score.mods & Mods.HIDDEN:
            if approach_rate <= 10.0:
                value *= 1.05 + 0.075 * (10.0 - approach_rate)
            elif approach_rate > 10.0:
                value *= 1.01 + 0.04 * (11.0 - min(11.0, approach_rate))

        if score.mods & Mods.FLASHLIGHT:
            value *= 1.35 * length_bonus

        accuracy = 0.0
        if total_hits != 0:
            accuracy = clamp(float(successful_hits) / total_hits, 0.0, 1.0)

        value *= math.pow(accuracy, 5.5)

        if score.mods & Mods.NOFAIL:
            value *= 0.90

        return CatchPerformanceAttributes(total=value)
