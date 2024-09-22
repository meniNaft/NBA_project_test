import repositories.team_repository as team_repo
import repositories.player_repository as players_repo
import repositories.player_team_repository as player_team_repo
from toolz import *
from dto.team_players_details_dto import TeamPlayersDetails

import utils.metrics_utils as utils
from typing import List

from models.team import Team


def delete(team_id: int):
    player_team_repo.delete_by_team(team_id)
    return team_repo.delete(team_id) > 0


def get_team_by_id(team_id: int):
    res = players_repo.get_player_team_details(team_id)
    if res:
        list_points_games_dict = list(map(utils.get_points_games_dict, res))
        return pipe(
            res,
            partial(map, lambda r: TeamPlayersDetails(
                player_name=r["player_name"],
                team=r["team"],
                position=r["position"],
                points=r["points"],
                games=r["games"],
                two_percents=r["two_percents"],
                three_percents=r["three_percents"],
                ATR=utils.get_assists_turnover_ratio(r["assists"], r["turnovers"]),
                PPG_ratio=utils.get_points_per_game(
                    current_player=utils.get_points_games_dict(r),
                    all_players_details=list_points_games_dict
                ),
            )),
            list,
            lambda li: {"player_list": li, "team": li[0].team if li[0] else "unknown"}
        )


def create_new_team(player_ids: List[int], team_name: str):
    team_id = team_repo.insert(Team(name=team_name, is_real=False))
    for p in player_ids:
        player_team_repo.insert(p, team_id)
    return team_id


def update_team_players(player_ids: List[int], team_id):
    row_affected: int = player_team_repo.delete_by_team(team_id)
    if row_affected > 0:
        for p in player_ids:
            player_team_repo.insert(p, team_id)
        return True
    return False
