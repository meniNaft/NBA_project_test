import main_repository as main_repo
from models.player import Player
TABLE_NAME = "players"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [Player(**row) for row in res]


def find_one_by_id(player_id):
    query = f"select * from {TABLE_NAME} where id = {player_id}"
    res = main_repo.get_one(query)
    return Player(**res) if res else None


def insert(player: Player):
    query = f"INSERT INTO {TABLE_NAME}(name, player_str_id) VALUES (%s, %s)"
    return main_repo.make_data_modify_query(query, (player.name, player.player_str_id))
