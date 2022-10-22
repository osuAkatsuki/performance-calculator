from __future__ import annotations

from performance_calculator import calculate_performance
from performance_calculator.models.mods import Mods
from performance_calculator.models.score import Score
from performance_calculator.rulesets.taiko.difficulty import TaikoDifficultyAttributes

# how far the values can be from the real result
TOLERANCE = 0.3

# https://osu.ppy.sh/beatmapsets/1819997#taiko/3734552
def test_shinchikuhome_yomi_yori() -> None:
    # as of 07/10/2022
    difficulty_attributes = TaikoDifficultyAttributes(
        star_rating=9.74012768474711,
        max_combo=3790,
        stamina_difficulty=5.894611764439881,
        rhythm_difficulty=2.2944574943096203,
        colour_difficulty=5.29230503132103,
        peak_difficulty=8.824591169784876,
        great_hit_window=18.93333371480306,
    )

    # shinchikuhome score
    score = Score(
        mode=1,
        score=5_109_213,
        max_combo=3790,
        mods=Mods.DOUBLETIME,
        accuracy=0.9974,
        num_300s=3_770,
        num_100s=20,
        num_50s=0,
        num_gekis=10,
        num_katus=0,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1101.85

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/1771472#taiko/3626457
def test_shinchikuhome_outer_occult_occupation() -> None:
    # as of 07/10/2022
    difficulty_attributes = TaikoDifficultyAttributes(
        star_rating=9.520615657661391,
        max_combo=2823,
        stamina_difficulty=5.4950436672865415,
        rhythm_difficulty=1.1695027051710607,
        colour_difficulty=5.270879098726863,
        peak_difficulty=8.52180031189024,
        great_hit_window=19.333333333333332,
    )

    score = Score(
        mode=1,
        score=3_381_491,
        max_combo=1622,
        mods=Mods.DOUBLETIME,
        accuracy=0.9945,
        num_300s=2_795,
        num_100s=25,
        num_50s=0,
        num_gekis=3,
        num_katus=0,
        num_misses=3,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1008.27

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/1791178#taiko/3670528
def test_loneyze_augoeides() -> None:
    difficulty_attributes = TaikoDifficultyAttributes(
        star_rating=9.106630223770846,
        max_combo=2885,
        stamina_difficulty=5.256448971084875,
        rhythm_difficulty=1.59424336834311,
        colour_difficulty=4.814127475180076,
        peak_difficulty=7.9678116197803455,
        great_hit_window=19.333333333333332,
    )

    score = Score(
        mode=1,
        score=3_875_231,
        max_combo=2885,
        mods=Mods.HIDDEN | Mods.NIGHTCORE,
        accuracy=0.9941,
        num_300s=2_885,
        num_100s=34,
        num_50s=0,
        num_gekis=2,
        num_katus=0,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1050.44

    assert abs(test_result - osu_result) <= TOLERANCE
