from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any
from typing import Callable

from performance_calculator.models.mods import Mods
from performance_calculator.models.oppai import OppaiWrapper
from performance_calculator.models.path import Path
from performance_calculator.models.performance import PerformanceAttributes
from performance_calculator.models.performance import PerformanceCalculator
from performance_calculator.models.score import Score
from performance_calculator.rulesets.osu.difficulty import OsuDifficultyAttributes


@dataclass
class OsuPerformanceAttributes(PerformanceAttributes):
    aim: float
    speed: float
    accuracy: float
    flashlight: float
    effective_miss_count: float


PERFORMANCE_BASE_MULTIPLIER = 1.14

clamp: Callable[[float, float, float], float] = (
    lambda x, l, u: l if x < l else u if x > u else x
)


class OsuPerformanceCalculator(PerformanceCalculator):
    difficulty_attributes: OsuDifficultyAttributes

    def calculate(self, score: Score) -> OsuPerformanceAttributes:
        effective_miss_count = self._calculate_effective_miss_count(score)
        total_hits = score.num_300s + score.num_100s + score.num_50s + score.num_misses

        multiplier = PERFORMANCE_BASE_MULTIPLIER

        if score.mods & Mods.NOFAIL:
            multiplier *= max(0.9, 1.0 - 0.02 * effective_miss_count)

        if score.mods & Mods.SPUNOUT and total_hits > 0:
            multiplier *= 1.0 - math.pow(
                (self.difficulty_attributes.spinner_count / total_hits),
                0.85,
            )

        aim_value = self._compute_aim_value(score, effective_miss_count, total_hits)
        speed_value = self._compute_speed_value(score, effective_miss_count, total_hits)
        accuracy_value = self._compute_accuracy_value(score, total_hits)
        flashlight_value = self._compute_flashlight_value(
            score,
            effective_miss_count,
            total_hits,
        )

        total_value = (
            math.pow(
                math.pow(aim_value, 1.1)
                + math.pow(speed_value, 1.1)
                + math.pow(accuracy_value, 1.1)
                + math.pow(flashlight_value, 1.1),
                1.0 / 1.1,
            )
            * multiplier
        )

        return OsuPerformanceAttributes(
            total=total_value,
            aim=aim_value,
            speed=speed_value,
            accuracy=accuracy_value,
            flashlight=flashlight_value,
            effective_miss_count=effective_miss_count,
        )

    def _compute_aim_value(
        self,
        score: Score,
        effective_miss_count: float,
        total_hits: int,
    ) -> float:
        aim_value = (
            math.pow(
                5.0 * max(1.0, self.difficulty_attributes.aim_difficulty / 0.0675)
                - 4.0,
                3.0,
            )
            / 100000.0
        )

        length_bonus = (
            0.95
            + 0.4 * min(1.0, total_hits / 2000.0)
            + ((math.log10(total_hits / 2000.0) * 0.5) * int(total_hits > 2000))
        )
        aim_value *= length_bonus

        if effective_miss_count > 0:
            aim_value *= 0.97 * math.pow(
                1 - math.pow(effective_miss_count / total_hits, 0.775),
                effective_miss_count,
            )

        aim_value *= self._get_combo_scaling_factor(score)

        approach_rate_factor = 0.0
        if self.difficulty_attributes.approach_rate > 10.33:
            approach_rate_factor = 0.3 * (
                self.difficulty_attributes.approach_rate - 10.33
            )
        elif self.difficulty_attributes.approach_rate < 8.0:
            approach_rate_factor = 0.05 * (
                8.0 - self.difficulty_attributes.approach_rate
            )

        aim_value *= 1.0 + approach_rate_factor * length_bonus

        if score.mods & Mods.HIDDEN:
            aim_value *= 1.0 + 0.04 * (12.0 - self.difficulty_attributes.approach_rate)

        if self.difficulty_attributes.slider_count > 0:
            estimate_difficult_sliders = self.difficulty_attributes.slider_count * 0.15

            estimate_slider_ends_dropped = clamp(
                min(
                    score.num_100s + score.num_50s + score.num_misses,
                    self.difficulty_attributes.max_combo - score.max_combo,
                ),
                0,
                estimate_difficult_sliders,
            )

            slider_nerf_factor = (
                1 - self.difficulty_attributes.slider_factor
            ) * math.pow(
                1 - estimate_slider_ends_dropped / estimate_difficult_sliders,
                3,
            ) + self.difficulty_attributes.slider_factor

            aim_value *= slider_nerf_factor

        accuracy = score.accuracy if score.accuracy <= 1.0 else score.accuracy / 100
        aim_value *= accuracy
        aim_value *= (
            0.98 + math.pow(self.difficulty_attributes.overall_difficulty, 2) / 2500
        )

        return aim_value

    def _compute_speed_value(
        self,
        score: Score,
        effective_miss_count: float,
        total_hits: int,
    ) -> float:
        speed_value = (
            math.pow(
                5.0 * max(1.0, self.difficulty_attributes.speed_difficulty / 0.0675)
                - 4.0,
                3.0,
            )
            / 100000.0
        )

        length_bonus = (
            0.95
            + 0.4 * min(1.0, total_hits / 2000.0)
            + ((math.log10(total_hits / 2000.0) * 0.5) * int(total_hits > 2000))
        )
        speed_value *= length_bonus

        if effective_miss_count > 0:
            speed_value *= 0.97 * math.pow(
                1 - math.pow(effective_miss_count / total_hits, 0.775),
                math.pow(effective_miss_count, 0.875),
            )

        speed_value *= self._get_combo_scaling_factor(score)

        approach_rate_factor = 0.0
        if self.difficulty_attributes.approach_rate > 10.33:
            approach_rate_factor = 0.3 * (
                self.difficulty_attributes.approach_rate - 10.33
            )

        speed_value *= 1.0 + approach_rate_factor * length_bonus

        if score.mods & Mods.HIDDEN:
            speed_value *= 1.0 + 0.04 * (
                12.0 - self.difficulty_attributes.approach_rate
            )

        relevant_total_diff = total_hits - self.difficulty_attributes.speed_note_count
        relevant_count_great = max(0, score.num_300s - relevant_total_diff)
        relevant_count_ok = max(
            0,
            score.num_100s - max(0, relevant_total_diff - score.num_300s),
        )
        relevant_count_meh = max(
            0,
            score.num_50s
            - max(0, relevant_total_diff - score.num_300s - score.num_100s),
        )

        relevant_accuracy = 0
        if self.difficulty_attributes.speed_note_count > 0:
            relevant_accuracy = (
                relevant_count_great * 6.0
                + relevant_count_ok * 2.0
                + relevant_count_meh
            ) / (self.difficulty_attributes.speed_note_count * 6.0)

        accuracy = score.accuracy if score.accuracy <= 1.0 else score.accuracy / 100

        speed_value *= (
            0.95 + math.pow(self.difficulty_attributes.overall_difficulty, 2) / 750
        ) * math.pow(
            (accuracy + relevant_accuracy) / 2.0,
            (14.5 - max(self.difficulty_attributes.overall_difficulty, 8)) / 2,
        )

        speed_value *= math.pow(
            0.99,
            (score.num_50s - total_hits / 500.0)
            * int(score.num_50s > total_hits / 500.0),
        )

        return speed_value

    def _compute_accuracy_value(
        self,
        score: Score,
        total_hits: int,
    ) -> float:
        amount_hit_objects_with_accuracy = self.difficulty_attributes.hit_circle_count

        better_accuracy_percentage = 0.0
        if amount_hit_objects_with_accuracy > 0:
            better_accuracy_percentage = max(
                (
                    (score.num_300s - (total_hits - amount_hit_objects_with_accuracy))
                    * 6
                    + score.num_100s * 2
                    + score.num_50s
                )
                / (amount_hit_objects_with_accuracy * 6),
                0,
            )

        accuracy_value = (
            math.pow(1.52163, self.difficulty_attributes.overall_difficulty)
            * math.pow(better_accuracy_percentage, 24)
            * 2.83
        )

        accuracy_value *= min(
            1.15,
            math.pow(amount_hit_objects_with_accuracy / 1000.0, 0.3),
        )

        if score.mods & Mods.HIDDEN:
            accuracy_value *= 1.08

        if score.mods & Mods.FLASHLIGHT:
            accuracy_value *= 1.02

        return accuracy_value

    def _compute_flashlight_value(
        self,
        score: Score,
        effective_miss_count: float,
        total_hits: int,
    ) -> float:
        if not score.mods & Mods.FLASHLIGHT:
            return 0.0

        flashlight_value = (
            math.pow(self.difficulty_attributes.flashlight_difficulty, 2.0) * 25.0
        )

        if effective_miss_count > 0:
            flashlight_value *= 0.97 * math.pow(
                1 - math.pow(effective_miss_count / total_hits, 0.775),
                math.pow(effective_miss_count, 0.875),
            )

        flashlight_value *= self._get_combo_scaling_factor(score)

        flashlight_value *= (
            0.7
            + 0.1 * min(1.0, total_hits / 200.0)
            + 0.2 * (min(1.0, (total_hits - 200) / 200.0) * int(total_hits > 200))
        )

        accuracy = score.accuracy if score.accuracy <= 1.0 else score.accuracy / 100
        flashlight_value *= 0.5 + accuracy / 2.0
        flashlight_value *= (
            0.98 + math.pow(self.difficulty_attributes.overall_difficulty, 2) / 2500.0
        )

        return flashlight_value

    def _calculate_effective_miss_count(self, score: Score) -> float:
        combo_based_miss_count = 0.0

        if self.difficulty_attributes.slider_count > 0:
            full_combo_threshold = (
                self.difficulty_attributes.max_combo
                - 0.1 * self.difficulty_attributes.slider_count
            )

            if score.max_combo < full_combo_threshold:
                combo_based_miss_count = full_combo_threshold / max(
                    1.0,
                    score.max_combo,
                )

        combo_based_miss_count = min(
            combo_based_miss_count,
            score.num_100s + score.num_50s + score.num_misses,
        )

        return max(score.num_misses, combo_based_miss_count)

    def _get_combo_scaling_factor(self, score: Score) -> float:
        if self.difficulty_attributes.max_combo <= 0:
            return 1.0

        return min(
            math.pow(score.max_combo, 0.8)
            / math.pow(self.difficulty_attributes.max_combo, 0.8),
            1.0,
        )
