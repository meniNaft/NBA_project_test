import repositories.main_repository as main_repo
import repositories.player_repository as player_repo
import repositories.team_repository as team_repo
from models.player_team import PlayerTeam
TABLE_NAME = "player_team"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [PlayerTeam(**row) for row in res]


def find_one_by_id(player_team_id):
    query = f"select * from {TABLE_NAME} where id = {player_team_id}"
    res = main_repo.get_one(query)
    return PlayerTeam(**res) if res else None


def insert(player_team: PlayerTeam):
    query = f"INSERT INTO {TABLE_NAME}(player_id, team_id) VALUES (%s, %s)"
    return main_repo.make_insert_query(query, (player_team.player.id, player_team.team.id))


def find_by_player_id_and_team_id(player_id: int, team_id: int):
    query = f"select * from {TABLE_NAME} where player_id = {player_id} and team_id = {team_id}"
    res = main_repo.get_one(query)
    return PlayerTeam(
        id=res["id"],
        player=player_repo.find_one_by_id(res["player_id"]),
        team=team_repo.find_one_by_id(res["team_id"])
    ) if res else None
