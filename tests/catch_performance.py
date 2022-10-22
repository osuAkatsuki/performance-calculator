from __future__ import annotations

from performance_calculator import calculate_performance
from performance_calculator.models.mods import Mods
from performance_calculator.models.score import Score
from performance_calculator.rulesets.catch.difficulty import CatchDifficultyAttributes

# how far the values can be from the real result
TOLERANCE = 0.05

# https://osu.ppy.sh/beatmapsets/1078698#fruits/2257056
def test_yesmydarknesss_embryo() -> None:
    # as of 22/10/2022
    difficulty_attributes = CatchDifficultyAttributes(
        star_rating=9.021864125368943,
        max_combo=1278,
        approach_rate=10,
    )

    # YesMyDarknesss's score
    score = Score(
        mode=2,
        score=53_448_485,
        max_combo=1278,
        mods=Mods.HARDROCK,
        accuracy=99.92,
        num_300s=1_240,
        num_100s=38,
        num_50s=38,
        num_gekis=129,
        num_katus=1,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1023.43

    assert abs(test_result - osu_result) <= TOLERANCE


def test_yesmydarknesss_megalovania() -> None:
    # as of 22/10/2022
    difficulty_attributes = CatchDifficultyAttributes(
        star_rating=8.921611634864426,
        max_combo=3403,
        approach_rate=10,
    )

    # YesMyDarknesss's score
    score = Score(
        mode=2,
        score=381_815_400,
        max_combo=3403,
        mods=Mods.HIDDEN | Mods.HARDROCK,
        accuracy=99.76,
        num_300s=3132,
        num_100s=271,
        num_50s=404,
        num_gekis=470,
        num_katus=9,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1240.11

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/1552869#fruits/3172816
def test_motion_put_and_end() -> None:
    difficulty_attributes = CatchDifficultyAttributes(
        star_rating=9.486280736253358,
        max_combo=3333,
        approach_rate=10,
    )

    # Motion's score
    score = Score(
        mode=2,
        score=263_078_678,
        max_combo=3333,
        mods=0,
        accuracy=100.0,
        num_300s=3293,
        num_100s=40,
        num_50s=191,
        num_gekis=414,
        num_katus=0,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1348.41

    assert abs(test_result - osu_result) <= TOLERANCE
