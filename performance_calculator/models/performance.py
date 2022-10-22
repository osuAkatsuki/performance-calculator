from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from performance_calculator.models.difficulty import DifficultyAttributes
from performance_calculator.models.score import Score


@dataclass
class PerformanceAttributes:
    total: float


class PerformanceCalculator(ABC):
    def __init__(self, difficulty_attributes: DifficultyAttributes) -> None:
        self.difficulty_attributes = difficulty_attributes

    @abstractmethod
    def calculate(self, score: Score) -> PerformanceAttributes:
        ...
