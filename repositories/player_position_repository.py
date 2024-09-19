import repositories.main_repository as main_repo
import repositories.player_repository as player_repo
import repositories.position_repository as position_repo
from models.player_position import PlayerPosition
TABLE_NAME = "player_position"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [PlayerPosition(**row) for row in res]


def find_one_by_id(position_id):
    query = f"select * from {TABLE_NAME} where id = {position_id}"
    res = main_repo.get_one(query)
    return PlayerPosition(**res) if res else None


def find_by_player_id(player_id):
    query = f"select * from {TABLE_NAME} where player_id = {player_id}"
    res = main_repo.get_all(query)
    return [PlayerPosition(**row) for row in res]


def insert(player_position: PlayerPosition):
    query = f"INSERT INTO {TABLE_NAME}(player_id, position_id) VALUES (%s, %s)"
    return main_repo.make_insert_query(query, (player_position.player.id, player_position.position.id))


def find_one_by_player_id_and_position_id(player_id: int, position_id: int):
    query = f"select * from {TABLE_NAME} where player_id = {player_id} and position_id = {position_id}"
    res = main_repo.get_one(query)
    return PlayerPosition(
        id=res["id"],
        player=player_repo.find_one_by_id(res["player_id"]),
        position=position_repo.find_one_by_id(res["position_id"])
    ) if res else None
