from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Score:
    mode: int

    score: int
    max_combo: int
    mods: int

    accuracy: float
    num_300s: int
    num_100s: int
    num_50s: int
    num_gekis: int
    num_katus: int
    num_misses: int
