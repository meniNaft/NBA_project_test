import repositories.main_repository as main_repo
from models.team import Team

TABLE_NAME = "teams"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [Team(**row) for row in res]


def find_one_by_id(team_id):
    query = f"select * from {TABLE_NAME} where id = {team_id}"
    res = main_repo.get_one(query)
    return Team(**res)


def insert(team: Team):
    query = f"INSERT INTO {TABLE_NAME}(name, is_real) VALUES (%s, %s)"
    return main_repo.make_data_modify_query(query, (team.name, team.is_real))

