from __future__ import annotations

from performance_calculator import calculate_performance
from performance_calculator.models.mods import Mods
from performance_calculator.models.score import Score
from performance_calculator.rulesets.osu.difficulty import OsuDifficultyAttributes

# how far the values can be from the real result
TOLERANCE = 0.05

# https://osu.ppy.sh/beatmapsets/475886#osu/1016701
def test_mrekk_justability() -> None:
    # as of 07/10/2022
    difficulty_attributes = OsuDifficultyAttributes(
        star_rating=8.968903153971592,
        max_combo=2868,
        aim_difficulty=4.6878801020817535,
        speed_difficulty=3.788079493693188,
        speed_note_count=903.8840205050329,
        flashlight_difficulty=6.4283445515991,
        slider_factor=0.9992674688934443,
        approach_rate=10.666666666666668,
        overall_difficulty=10.444444444444445,
        drain_rate=6,
        hit_circle_count=1113,
        slider_count=705,
        spinner_count=3,
    )

    # mrekk score
    score = Score(
        mode=0,
        score=165_764_484,
        max_combo=2685,
        mods=Mods.HIDDEN | Mods.DOUBLETIME,
        accuracy=0.9919,
        num_300s=1_800,
        num_100s=17,
        num_50s=3,
        num_gekis=449,
        num_katus=15,
        num_misses=1,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1145.64

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/1002271#osu/2097898
def test_mrekk_magma() -> None:
    # as of 07/10/2022
    difficulty_attributes = OsuDifficultyAttributes(
        star_rating=9.476473473098002,
        max_combo=428,
        aim_difficulty=5.299074247092309,
        speed_difficulty=3.22604582775375,
        speed_note_count=214.60422058780836,
        flashlight_difficulty=3.9467506470056675,
        slider_factor=0.979793529252011,
        approach_rate=11,
        overall_difficulty=11.111111111111112,
        drain_rate=8.679999351501465,
        hit_circle_count=210,
        slider_count=105,
        spinner_count=1,
    )

    # mrekk score
    score = Score(
        mode=0,
        score=4_988_391,
        max_combo=428,
        mods=Mods.HIDDEN | Mods.DOUBLETIME | Mods.HARDROCK,
        accuracy=1.0,
        num_300s=316,
        num_100s=0,
        num_50s=0,
        num_gekis=94,
        num_katus=0,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 1_215.82

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/145978#osu/620789
def test_mrekk_fake_promise() -> None:
    # as of 07/10/2022
    difficulty_attributes = OsuDifficultyAttributes(
        star_rating=8.618551793057438,
        max_combo=2861,
        aim_difficulty=3.9922197078486046,
        speed_difficulty=4.2487184182887985,
        speed_note_count=246.81000611229842,
        flashlight_difficulty=5.571321054632288,
        slider_factor=0.9819111383683237,
        approach_rate=10.46666653951009,
        overall_difficulty=9.777777777777779,
        drain_rate=6,
        hit_circle_count=958,
        slider_count=703,
        spinner_count=2,
    )

    # mrekk score
    score = Score(
        mode=0,
        score=134_073_146,
        max_combo=2854,
        mods=Mods.HIDDEN | Mods.DOUBLETIME,
        accuracy=0.9932,
        num_300s=1646,
        num_100s=17,
        num_50s=0,
        num_gekis=256,
        num_katus=14,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 967.43

    assert abs(test_result - osu_result) <= TOLERANCE


# https://osu.ppy.sh/beatmapsets/1376308#osu/2844649
def test_criller_oshama() -> None:
    # as of 07/10/2022
    difficulty_attributes = OsuDifficultyAttributes(
        star_rating=10.070061716641963,
        max_combo=1322,
        aim_difficulty=5.758515037673032,
        speed_difficulty=2.935655437054821,
        speed_note_count=298.3779798165621,
        flashlight_difficulty=3.659807292469087,
        slider_factor=0.5887495379987688,
        approach_rate=9.5,
        overall_difficulty=9,
        drain_rate=5.300000190734863,
        hit_circle_count=310,
        slider_count=443,
        spinner_count=1,
    )

    # criller score
    score = Score(
        mode=0,
        score=22_573_780,
        max_combo=1140,
        mods=0,
        accuracy=97.28,
        num_300s=725,
        num_100s=22,
        num_50s=7,
        num_gekis=248,
        num_katus=17,
        num_misses=0,
    )

    test_result = round(
        calculate_performance(score, difficulty_attributes),
        2,
    )
    osu_result = 609.94

    assert abs(test_result - osu_result) <= TOLERANCE
