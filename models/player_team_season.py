from dataclasses import dataclass
from models.player_team import PlayerTeam
from models.season import Season


@dataclass
class PlayerTeamSeason:
    player_team: PlayerTeam
    season: Season
    id: int = None
