from dataclasses import dataclass


@dataclass
class NBAApiObject:
    playerName: str
    position: str
    games: int
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
    personalFouls: int
    points: int
    team: str
    season: int
    playerId: str
