from dataclasses import dataclass


@dataclass
class TeamPlayersDetails:
    player_name: str
    team: str
    position: str
    points: int
    games: int
    two_percents: float
    three_percents: float
    ATR: float
    PPG_ratio: float

