import main_repository as main_repo
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
    return main_repo.make_data_modify_query(query, (player_position.player.id, player_position.position.id))
