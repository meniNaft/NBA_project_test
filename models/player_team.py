from dataclasses import dataclass
from models.player import Player
from models.team import Team


@dataclass
class PlayerTeam:
    player: Player
    team: Team
    id: int = None
