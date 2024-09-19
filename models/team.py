from dataclasses import dataclass


@dataclass
class Team:
    name: int
    is_real: bool
    id: int = None
