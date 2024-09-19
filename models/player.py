from dataclasses import dataclass
from models.position import Position
from typing import List


@dataclass
class Player:
    name: str
    player_str_id: str
    positions: List[Position] = None
    id: int = None
