from __future__ import annotations

from performance_calculator import calculate_performance
from performance_calculator.models.mods import Mods
from performance_calculator.models.score import Score
from performance_calculator.rulesets.mania.difficulty import ManiaDifficultyAttributes

# how far the values can be from the real result
TOLERANCE = 0.05

# https://osu.ppy.sh/beatmapsets/974689#mania/2220863
def test_jakads_monochrome() -> None:
    # as of 22/10/2022
    difficulty_attributes = ManiaDifficultyAttributes(
        star_rating=10.71588862238911,
        max_combo=13_516,
        great_hit_window=42,
    )

    # Jakads's score
    score = Score(
        mode=3,
        score=975_283,
        max_combo=4_357,
        mods=Mods.DOUBLETIME | Mods.NIGHTCORE,
        accuracy=99.52,
        num_300s=1_180,
        num_100s=2,
        num_50s=0,
        num_gekis=4_288,
        num_katus=57,
        num_misses=6,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1428.44

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/800102#mania/1679790
def test_jakads_last_resort() -> None:
    # as of 22/10/2022
    difficulty_attributes = ManiaDifficultyAttributes(
        star_rating=10.285073250712037,
        max_combo=4_433,
        great_hit_window=38,
    )

    # Jakads's score
    score = Score(
        mode=3,
        score=989_698,
        max_combo=3_679,
        mods=0,
        accuracy=99.84,
        num_300s=608,
        num_100s=0,
        num_50s=0,
        num_gekis=2_747,
        num_katus=13,
        num_misses=1,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1342.96

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/861816#mania/1802831
def test_dressurf_tiefsee() -> None:
    difficulty_attributes = ManiaDifficultyAttributes(
        star_rating=11.433692671697369,
        max_combo=10_406,
        great_hit_window=42,
    )

    # dressurf's score
    score = Score(
        mode=3,
        score=893_539,
        max_combo=1_920,
        mods=Mods.DOUBLETIME | Mods.NIGHTCORE,
        accuracy=97.95,
        num_300s=2_073,
        num_100s=20,
        num_50s=22,
        num_gekis=4_545,
        num_katus=179,
        num_misses=50,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1450.80

    assert abs(test_result - osu_result) <= TOLERANCE
