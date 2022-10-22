from __future__ import annotations

import math
from typing import Optional

from performance_calculator.models.difficulty import DifficultyAttributes
from performance_calculator.models.mods import Mods
from performance_calculator.models.oppai import OppaiWrapper
from performance_calculator.models.path import Path
from performance_calculator.models.score import Score
from performance_calculator.rulesets.catch.difficulty import CatchDifficultyAttributes
from performance_calculator.rulesets.catch.performance import CatchPerformanceCalculator
from performance_calculator.rulesets.mania.difficulty import ManiaDifficultyAttributes
from performance_calculator.rulesets.mania.performance import ManiaPerformanceCalculator
from performance_calculator.rulesets.osu.difficulty import OsuDifficultyAttributes
from performance_calculator.rulesets.osu.performance import OsuPerformanceCalculator
from performance_calculator.rulesets.taiko.difficulty import TaikoDifficultyAttributes
from performance_calculator.rulesets.taiko.performance import TaikoPerformanceCalculator

__name__ = "performance_calculator"
__author__ = "tsunyoku"
__version__ = "0.1.0"
__all__ = ("calculate_score",)


def _calculate_oppai(
    score: Score, oppai_path: str, osu_file_path: str
) -> tuple[float, float]:
    path = Path(oppai_path)
    if not path.exists():
        raise FileNotFoundError(f"oppai path {oppai_path} does not exist")

    with OppaiWrapper(oppai_path) as ezpp:
        ezpp.configure(
            mode=score.mode,
            acc=score.accuracy,
            mods=score.mods,
            combo=score.max_combo,
            nmiss=score.num_misses,
        )
        ezpp.calculate(Path(osu_file_path))

        pp = ezpp.get_pp()
        sr = ezpp.get_sr()

        if math.isnan(sr) or math.isinf(sr):
            return 0.0, 0.0

        if math.isnan(pp) or math.isinf(pp):
            return 0.0, 0.0

        return sr, pp

    return 0.0, 0.0


def _calculate_std(
    score: Score,
    attributes: Optional[OsuDifficultyAttributes] = None,
    oppai_path: Optional[str] = None,
    osu_file_path: Optional[str] = None,
) -> tuple[float, float]:
    # use lazer pp if not rx/ap
    if not score.mods & Mods.RELAX and not score.mods & Mods.AUTOPILOT:
        if attributes is None:
            raise ValueError("You must provide difficulty attributes")

        calculator = OsuPerformanceCalculator(attributes)
        calculator_result = calculator.calculate(score)
        result = calculator_result.total

        star_rating = attributes.star_rating
    else:
        if osu_file_path is None:
            raise ValueError("You must provide a .osu file path")

        if oppai_path is None:
            raise ValueError("You must provide an oppai path")

        star_rating, result = _calculate_oppai(score, oppai_path, osu_file_path)

    return star_rating, result


def _calculate_taiko(
    score: Score,
    attributes: TaikoDifficultyAttributes,
) -> float:
    calculator = TaikoPerformanceCalculator(attributes)
    calculator_result = calculator.calculate(score)
    result = calculator_result.total

    return result


def _calculate_catch(
    score: Score,
    attributes: CatchDifficultyAttributes,
) -> float:
    calculator = CatchPerformanceCalculator(attributes)
    calculator_result = calculator.calculate(score)
    result = calculator_result.total

    return result


def _calculate_mania(
    score: Score,
    attributes: ManiaDifficultyAttributes,
) -> float:
    calculator = ManiaPerformanceCalculator(attributes)
    calculator_result = calculator.calculate(score)
    result = calculator_result.total

    return result


def calculate_score(
    score: Score,
    attributes: Optional[DifficultyAttributes] = None,  # doesn't exist if oppai is used
    oppai_path: Optional[str] = None,  # doesn't exist unless oppai is used
    osu_file_path: Optional[str] = None,  # doesn't exist unless oppai is used
) -> tuple[float, float]:
    if score.mode == 0:
        if attributes is not None and not isinstance(
            attributes,
            OsuDifficultyAttributes,
        ):
            raise ValueError("attributes must be OsuDifficultyAttributes")

        result, star_rating = _calculate_std(
            score,
            attributes,
            oppai_path,
            osu_file_path,
        )
    elif score.mode == 1:
        if attributes is None or not isinstance(attributes, TaikoDifficultyAttributes):
            raise ValueError("You must provide difficulty attributes")

        result = _calculate_taiko(
            score,
            attributes,
        )

        star_rating = attributes.star_rating
    elif score.mode == 2:
        if attributes is None or not isinstance(attributes, CatchDifficultyAttributes):
            raise ValueError("you must provide difficulty attributes")

        result = _calculate_catch(
            score,
            attributes,
        )

        star_rating = attributes.star_rating
    elif score.mode == 3:
        if attributes is None or not isinstance(attributes, ManiaDifficultyAttributes):
            raise ValueError("you must provide difficulty attributes")

        result = _calculate_mania(
            score,
            attributes,
        )

        star_rating = attributes.star_rating
    else:
        raise NotImplementedError(
            f"no performance calculator found for mode {score.mode}",
        )

    return star_rating, result
