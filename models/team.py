from dataclasses import dataclass


@dataclass
class Team:
    name: str
    is_real: bool
    id: int = None
