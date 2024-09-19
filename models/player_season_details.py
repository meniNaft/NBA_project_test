from dataclasses import dataclass
from models.player_team_season import PlayerTeamSeason


@dataclass
class PlayerSeasonDetails:
    player_group_season: PlayerTeamSeason
    fieldGoals: int
    fieldAttempts: int
    fieldPercent: float
    threeFg: int
    threeAttempts: int
    threePercent: float
    twoFg: int
    twoAttempts: int
    twoPercent: float
    assists: int
    turnovers: int
    games: int
    points: int
    id: int = None
