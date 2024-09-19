import repositories.main_repository as main_repo
from models.player_season_details import PlayerSeasonDetails
TABLE_NAME = "player_season_details"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [PlayerSeasonDetails(**row) for row in res]


def find_one_by_id(player_id):
    query = f"select * from {TABLE_NAME} where id = {player_id}"
    res = main_repo.get_one(query)
    return PlayerSeasonDetails(**res) if res else None


def insert(player_season_details: PlayerSeasonDetails):
    query = f'''INSERT INTO {TABLE_NAME}
    (player_team_season_id, fieldGoals, fieldAttempts, fieldPercent, threeFg, threeAttempts, 
    threePercent, twoFg, twoAttempts, twoPercent, assists, turnovers, games, points) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    return main_repo.make_insert_query(query, (
        player_season_details.player_team_season.id,
        player_season_details.fieldGoals,
        player_season_details.fieldAttempts,
        player_season_details.fieldPercent,
        player_season_details.threeFg,
        player_season_details.threeAttempts,
        player_season_details.threePercent,
        player_season_details.twoFg,
        player_season_details.twoAttempts,
        player_season_details.twoPercent,
        player_season_details.assists,
        player_season_details.turnovers,
        player_season_details.games,
        player_season_details.points
    ))
