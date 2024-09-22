import repositories.team_repository as team_repo
from typing import List
import repositories.player_repository as players_repo
from toolz import *
from operator import itemgetter


def is_team_exist(team_id: int):
    return team_repo.find_one_by_id(team_id) is not None


def is_team_exist_by_name(team_name: str):
    return team_repo.find_team_by_name(team_name) is not None


def is_valid_player_positions(player_ids: List[int]):
    players = players_repo.get_players_by_ids(player_ids)
    if len(players) != 5:
        return False
    unique_positions_count = pipe(
        players,
        partial(map, itemgetter("position")),
        set,
        len
    )
    return unique_positions_count == 5


def is_players_in_other_team(players_ids: List[int], team_id: int):
    res = players_repo.get_players_in_other_team(players_ids, team_id)
    return res["count"] > 0

def is_players_in_other_team_by_team_name(players_ids: List[int], team_name: str):
    team = team_repo.find_team_by_name(team_name)
    if team:
        return is_players_in_other_team(players_ids, team["id"])
    return False
