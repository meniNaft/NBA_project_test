import repositories.main_repository as main_repo
from models.season import Season
TABLE_NAME = "seasons"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [Season(**row) for row in res]


def find_one_by_id(season_id):
    query = f"select * from {TABLE_NAME} where id = {season_id}"
    res = main_repo.get_one(query)
    return Season(**res)


def find_one_by_year(year: int):
    query = f"select * from {TABLE_NAME} where year = {year}"
    res = main_repo.get_one(query)
    return Season(**res)


def insert(season: Season):
    query = f"INSERT INTO {TABLE_NAME}(year) VALUES (%s)"
    return main_repo.make_insert_query(query, (season.year,))

