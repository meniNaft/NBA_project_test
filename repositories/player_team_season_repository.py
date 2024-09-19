import main_repository as main_repo
from models.player_team_season import PlayerTeamSeason
TABLE_NAME = "player_team_season"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [PlayerTeamSeason(**row) for row in res]


def find_one_by_id(player_team_season_id):
    query = f"select * from {TABLE_NAME} where id = {player_team_season_id}"
    res = main_repo.get_one(query)
    return PlayerTeamSeason(**res)


def insert(player_team_season: PlayerTeamSeason):
    query = f"INSERT INTO {TABLE_NAME}(player_team_id, season_id) VALUES (%s, %s)"
    return main_repo.make_data_modify_query(query, (player_team_season.player_team.id, player_team_season.season.id))

