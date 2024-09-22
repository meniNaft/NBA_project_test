from dto.search_player_dto import SearchPlayerDto
import repositories.player_repository as player_repo
from typing import List
from toolz import *
import utils.metrics_utils as utils


def search_players(position: str, season_year: int = None) -> List[SearchPlayerDto]:
    db_res = player_repo.search_players_by_position_and_season(position, season_year)
    list_points_games_dict = list(map(utils.get_points_games_dict, db_res))

    if season_year is None:
        player_data = {}

        for v in db_res:
            player_id = v["player_id"]
            if player_id not in player_data:
                player_data[player_id] = {
                    "player_name": v["player_name"],
                    "team": v["team"],
                    "position": v["position"],
                    "seasons": [],
                    "total_points": 0,
                    "total_games": 0,
                    "total_assists": 0,
                    "total_turnovers": 0,
                    "two_percents": v["two_percents"],
                    "three_percents": v["three_percents"]
                }

            player_data[player_id]["seasons"].append(v["season"])
            player_data[player_id]["total_points"] += v["points"]
            player_data[player_id]["total_games"] += v["games"]
            player_data[player_id]["total_assists"] += v["assists"]
            player_data[player_id]["total_turnovers"] += v["turnovers"]

        return [
            SearchPlayerDto(
                player_name=data["player_name"],
                team=data["team"],
                position=data["position"],
                seasons=data["seasons"],
                points=data["total_points"],
                games=data["total_games"],
                two_percents=data["two_percents"],
                three_percents=data["three_percents"],
                ATR=utils.get_assists_turnover_ratio(data["total_assists"], data["total_turnovers"]),
                PPG_ratio=utils.get_points_per_game(
                    current_player={"points": data["total_points"], "games": data["total_games"]},
                    all_players_details=list_points_games_dict
                ),
            )
            for data in player_data.values()
        ]

    return list(map(lambda v: SearchPlayerDto(
        player_name=v["player_name"],
        team=v["team"],
        position=v["position"],
        seasons=[v["season"]],
        points=v["points"],
        games=v["games"],
        two_percents=v["two_percents"],
        three_percents=v["three_percents"],
        ATR=utils.get_assists_turnover_ratio(v["assists"], v["turnovers"]),
        PPG_ratio=utils.get_points_per_game(
            current_player=utils.get_points_games_dict(v),
            all_players_details=list_points_games_dict
        ),
    ), db_res))
