import main_repository as main_repo
from models.player_team import PlayerTeam
TABLE_NAME = "player_team"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [PlayerTeam(**row) for row in res]


def find_one_by_id(player_team_id):
    query = f"select * from {TABLE_NAME} where id = {player_team_id}"
    res = main_repo.get_one(query)
    return PlayerTeam(**res)


def insert(player_team: PlayerTeam):
    query = f"INSERT INTO {TABLE_NAME}(player_id, team_id) VALUES (%s, %s)"
    return main_repo.make_data_modify_query(query, (player_team.player.id, player_team.team.id))
