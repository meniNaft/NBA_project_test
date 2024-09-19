from dataclasses import dataclass
from typing import List


@dataclass
class SearchPlayerDto:
    player_name: str
    team: str
    position: str
    seasons: List[str]
    points: int
    games: int
    two_percents: float
    three_percents: float
    ATR: float
    PPG_ratio: float
