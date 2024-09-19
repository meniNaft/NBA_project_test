import main_repository as main_repo
from models.position import Position

TABLE_NAME = "position"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [Position(**row) for row in res]


def find_one_by_id(position_id):
    query = f"select * from {TABLE_NAME} where id = {position_id}"
    res = main_repo.get_one(query)
    return Position(**res)


def insert(position: Position):
    query = f"INSERT INTO {TABLE_NAME}(type) VALUES (%s)"
    return main_repo.make_data_modify_query(query, (position.type,))

