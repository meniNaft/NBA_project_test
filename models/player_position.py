from dataclasses import dataclass
from models.player import Player
from models.position import Position


@dataclass
class PlayerPosition:
    player: Player = None
    position: Position = None
    id: int = None
