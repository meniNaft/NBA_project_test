from models.player_season_details import PlayerSeasonDetails
from typing import List
from toolz import *


def get_assists_turnover_ratio(assists: int, turnovers: int):
    return assists / turnovers


def get_points_per_game(current_player: {"points": int, "games": int}, all_players_details: List[{"points": int, "games": int}]):
    current_avg = current_player["points"] / current_player["games"]
    avg = pipe(
        all_players_details,
        partial(map, lambda p: p["points"] / p["games"]),
        list,
        lambda li: sum(li) / len(li)
    )
    return current_avg / avg
