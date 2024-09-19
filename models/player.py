from dataclasses import dataclass
from models.position import Position


@dataclass
class Player:
    name: int
    position: Position
    player_str_id: str
    id: int = None
